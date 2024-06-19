import requests
import logging
import json
from bs4 import BeautifulSoup


class GitHubAPI:
    def __init__(self, tk):
        self.token = tk
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def get_rate_limit(self):
        url = "https://api.github.com/rate_limit"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        if response.status_code == 200:
            limit = data['resources']['core']['limit']
            used = data['resources']['core']['used']
            remaining = data['resources']['core']['remaining']
            print("\nGitHub API successfully Authenticated!\n"
                  "Here is the rate limit information:\n"
                  f"Rate Limit: {limit}. Used: {used}. Left: {remaining}.\n\n")
            return response.status_code

        else:
            print(f"I could not validate your token please provide a valid one.\n"
                  f"Error: {response.status_code} - {data['message']}\n")
            return response.status_code

    def has_workflow_files(self, repo_full_name):
        """Returns the names of the .yml or .yaml Parser in the
        .GitHub/workflows folder, or None if there are no Parser."""
        workflows_url = f"https://api.github.com/repos/{repo_full_name}/contents/.github/workflows"
        response = requests.get(workflows_url, headers=self.headers)
        if response.status_code == 200:
            files = response.json()
            yml_files = [file['name'] for file in files if file['name'].endswith(('.yml', '.yaml'))]
            return len(yml_files), yml_files if yml_files else []
        return 0, []

    def fetch_repo(self, query, sort, order, page):
        """Search and filter repositories for a specific page."""
        filtered_repos_for_page = []

        try:
            url = (f'https://api.github.com/search/repositories?'
                   f'q={query}&sort={sort}&order={order}&per_page=100&page={page}')
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            for repo in response.json()['items']:
                repo_name = repo['full_name']
                repo_description = repo['description']
                repo_url = repo['html_url']
                language = repo['language'] if repo['language'] else 'Unknown'
                stars = repo['stargazers_count']
                open_issue_count = repo['open_issues_count']
                owner = repo['owner']['login']
                owner_acc_type = repo['owner']['type']
                created_at = repo['created_at']
                updated_at = repo['updated_at']
                size = repo['size']
                downloads = repo['has_downloads']

                yml_file_count, yml_files = self.has_workflow_files(repo_name)
                has_yml = bool(yml_files)

                logging.info(f"Verifying Repository: {repo_name} - URL: {repo_url} - YML File Count: {yml_file_count}")
                logging.info("-" * 40 + "\n")

                filtered_repos_for_page.append({
                    "Owner": owner,
                    "Acc type": owner_acc_type,
                    "Name": repo_name,
                    "Url": repo_url,
                    "Description": repo_description,
                    "Language": language,
                    "Stars": stars,
                    "Issue Count": open_issue_count,
                    "Created At": created_at,
                    "Updated At": updated_at,
                    "Size": size,
                    "Downloads": downloads,
                    "hasYml": has_yml,
                    "YML Count": yml_file_count,
                    "YML Files": "; ".join(yml_files) if yml_files else "No .yml or .yaml scripts"
                })

        except requests.RequestException as e:
            logging.error(f"Error when searching for the {page}. Error: {e}")

        return filtered_repos_for_page

    def fetch_specific_commit(self, owner, repo_name, commit_sha):
        """Fetch information about a specific commit based on its SHA."""
        filtered_commits = []

        try:
            url = f'https://api.github.com/repos/{owner}/{repo_name}/commits/{commit_sha}'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            commit = response.json()

            commit_author_type = commit['author']['type'] if commit['author'] else None
            commit_committer_type = commit['committer']['type'] if commit['committer'] else None
            commit_tree = commit['commit']['tree']['sha']
            commit_files = [files['filename'] for files in commit['Parser']]

            logging.info(f"Getting Additional Info From Commit: {commit_sha}")

            filtered_commits.append({
                "Author Acc": commit_author_type,
                "Committer Acc": commit_committer_type,
                "Tree": commit_tree,
                "Files": ", ".join(commit_files)

            })

        except requests.RequestException as e:
            logging.error(f"Error on search commit {commit_sha}. Error: {e}")

        return filtered_commits

    def fetch_specific_issues(self, owner, repo_name, issue_number):
        """Fetch information about specific issues based on your Issue list."""
        filtered_issues = []

        try:
            url = f'https://api.github.com/repos/{owner}/{repo_name}/issues/{issue_number}'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            issue = response.json()
            if 'pull_request' not in issue:
                is_pull_request = False
            else:
                is_pull_request = True

            issue_title = issue['title']
            issue_creator = issue['user']['login']
            issue_creator_type = issue['user']['type']
            issue_creator_association = issue['author_association']
            issue_created_at = issue['created_at']
            issue_closed_at = issue['closed_at']
            issue_state = issue['state']
            issue_body = issue['body']
            issue_labels = [label['name'] for label in issue['labels']]
            issue_reviewers = [assignee['login'] for assignee in issue['assignees']]
            issue_reviewers_type = [assignee['type'] for assignee in issue['assignees']]
            issue_closer = issue['closed_by']['login'] if issue['closed_by'] else None
            issue_closer_acc = issue['closed_by']['type'] if issue['closed_by'] else None
            issue_milestone = issue['milestone']['title'] if issue['milestone'] else None

            logging.info(f"Getting Info From Issue: #{issue_number} - Title: {issue_title}")

            filtered_issues.append({
                "Creator": issue_creator,
                "Creator association": issue_creator_association,
                "Creator type": issue_creator_type,
                "Created At": issue_created_at,
                "Closed At": issue_closed_at,
                "State": issue_state,
                "Body": issue_body,
                "Closer": issue_closer,
                "Closer type": issue_closer_acc,
                "Labels": ", ".join(issue_labels),
                "Reviewers/Assignees": ", ".join(issue_reviewers),
                "Reviewers/Assignees type": ", ".join(issue_reviewers_type),
                "Is Pull Request": is_pull_request,
                "Milestone": issue_milestone,
            })

        except requests.RequestException as e:
            logging.error(f"Error when searching for issue #{issue_number}. Error: {e}")

        return filtered_issues

    def fetch_action_verification(self, user_name, action_name):
        """
        Fetch information about a specific app based on its name.
        """
        try:
            # Step 1: Attempt to fetch organization details
            url_org = f'https://api.github.com/orgs/{user_name}'
            response = requests.get(url_org, headers=self.headers)

            if response.status_code == 404:
                # If organization is not found, attempt to fetch user details
                url_user = f'https://api.github.com/users/{user_name}'
                response = requests.get(url_user, headers=self.headers)
                response.raise_for_status()  # Raise an exception if user is not found

            response.raise_for_status()  # Raise an exception for any other HTTP errors
            user_data = response.json()

            owner_verified = user_data.get('is_verified', False)

            # Step 2: Scrape the GitHub Action marketplace page for verification badge
            url_bs = f"https://github.com/marketplace/actions/{action_name}"
            response_bs = requests.get(url_bs)
            if response_bs.status_code == 404:
                # logging.warning(f"GitHub Action marketplace page not found for action: {action_name}")
                verification_badge = False
            else:
                response_bs.raise_for_status()
                soup = BeautifulSoup(response_bs.text, 'html.parser')
                verification_badge = soup.find('svg', class_='octicon-verified') is not None

            return owner_verified, verification_badge

        except requests.RequestException:
            # logging.error(f"Error when searching for the {user_name} and {action_name.upper()} actions. Error: {e}")
            return False, False

    def get_repository_vulnerabilities(self, owner, name):
        """Fetch the vulnerabilities of a repository."""

        url = f'https://api.github.com/repos/{owner}/{name}/security-advisories'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        if response.status_code == 200:
            return json.dumps(response.json(), indent=4)
        else:
            logging.error(f"Error fetching vulnerabilities: {response.text}")
            return None
