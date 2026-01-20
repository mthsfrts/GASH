import requests
import logging
import json
import math
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
        response = requests.get(url, headers=self.headers, timeout=10)
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

    def has_workflow_files(self, owner, repo_name):
        """Returns the names of the .yml or .yaml files in the
        .GitHub/workflows folder, or None if there are no files."""
        workflows_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/.github/workflows"
        response = requests.get(workflows_url, headers=self.headers)

        if response.status_code == 200:
            try:
                files = response.json()
                if isinstance(files, list):
                    yml_files = [file['name'] for file in files if file['name'].endswith(('.yml', '.yaml'))]
                    return len(yml_files), yml_files
                else:
                    logging.info(f"Unexpected response format: {files}")
                    return 0, []
            except ValueError as e:
                logging.info(f"Error processing JSON response: {e}")
                return 0, []
        elif response.status_code == 404:
            return 0, []
        else:
            logging.info(f"API error: {response.status_code}, {response.text}")
            return 0, []

    def fetch_repo(self, query, sort, order, page):
        """Search and filter repositories for a specific page."""
        filtered_repos_for_page = []

        try:
            url = (f'https://api.github.com/search/repositories?'
                   f'q={query}&sort={sort}&order={order}&per_page=100&page={page}')
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            for repo in response.json()['items']:
                repo_name = repo['name']
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

                yml_file_count, yml_files = self.has_workflow_files(owner, repo_name)
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

    def get_contents(self, owner, repo_name):
        """Fetch the content of the .github/workflows directory in a repository."""
        try:
            url = f'https://api.github.com/repos/{owner}/{repo_name}/contents/.github/workflows'
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            content = response.json()
            return content

        except requests.RequestException as e:
            logging.error(f"Error fetching workflows' content for {owner}/{repo_name}. Error: {e}")
            return []

    def fetch_specific_commit(self, owner, repo_name, commit_sha):
        """Fetch information about a specific commit based on its SHA."""
        filtered_commits = []

        try:
            url = f'https://api.github.com/repos/{owner}/{repo_name}/commits/{commit_sha}'
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            commit = response.json()

            commit_author_type = commit['author']['type'] if commit['author'] else None
            commit_committer_type = commit['committer']['type'] if commit['committer'] else None
            commit_tree = commit['commit']['tree']['sha']
            commit_files = [files['filename'] for files in commit['files']]

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
            response = requests.get(url, headers=self.headers, timeout=10)
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
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            if response.status_code == 200:
                vulnerabilities = response.json()
                if vulnerabilities:
                    return json.dumps(vulnerabilities, indent=4)
                else:
                    return None

        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return None
            else:
                logging.error(f"Error fetching vulnerabilities for {owner}/{name}: {e}")
                return None

        except requests.exceptions.RequestException as e:
            logging.error(f"Error connecting to GitHub API for {owner}/{name}: {e}")
            return None

    def get_workflow_ids(self, owner, name):
        """
        Fetch and filter workflows of a repository.

        Args:
            owner (str): The owner of the repository.
            name (str): The name of the repository.

        Returns:
            list: A list of dictionaries containing workflow details.
        """
        workflow_details = []

        try:
            url = f'https://api.github.com/repos/{owner}/{name}/actions/workflows'
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            workflows = response.json().get("workflows", [])

            for workflow in workflows:
                workflow_id = workflow["id"]
                workflow_name = workflow["name"]
                workflow_state = workflow["state"]
                created_at = workflow["created_at"]
                updated_at = workflow["updated_at"]
                path = workflow["path"]

                logging.info(f"Found Workflow: {workflow_name} - ID: {workflow_id} - State: {workflow_state}")
                logging.info("-" * 40 + "\n")

                workflow_details.append({
                    "ID": workflow_id,
                    "Name": workflow_name,
                    "State": workflow_state,
                    "Created At": created_at,
                    "Updated At": updated_at,
                    "Path": path
                })

        except requests.RequestException as e:
            logging.error(f"Error fetching workflows for {owner}/{name}. Error: {e}")

        return workflow_details

    def get_all_runs(self, owner, repo):
        """
        Fetch and filter all the runs of a repository, handling pagination.

        Args:
            owner (str): The owner of the repository.
            repo (str): The name of the repository.

        Returns:
            list: A list of dictionaries containing run details.
        """
        runs_details = []
        page = 1
        per_page = 100
        url = f'https://api.github.com/repos/{owner}/{repo}/actions/runs'

        try:
            while True:
                params = {'page': page, 'per_page': per_page}
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()

                workflow_runs = response.json().get("workflow_runs", [])
                total_count = response.json().get("total_count", 0)
                total_pages = math.ceil(total_count / per_page)
                logging.info(f"Writing details from page {page} of {total_pages}.")

                for run in workflow_runs:
                    runs_details.append({
                        "ID": run["id"],
                        "Name": run["name"],
                        "Head Branch": run["head_branch"],
                        "Path": run["path"],
                        "Display Title": run["display_title"],
                        "Run Number": run["run_number"],
                        "Event": run["event"],
                        "Status": run["status"],
                        "Conclusion": run["conclusion"],
                        "Workflow ID": run["workflow_id"],
                        "Pull Requests": [
                            {"ID": pr.get("id"), "Title": pr.get("title"), "URL": pr.get("url")}
                            for pr in run.get("pull_requests", [])
                        ],
                        "Created At": run["created_at"],
                        "Updated At": run["updated_at"],
                        "Run Attempt": run["run_attempt"],
                        "Reference Workflow": run["workflow_url"],
                        "Actor": {
                            "Login": run["actor"]["login"],
                            "ID": run["actor"]["id"],
                            "HTML URL": run["actor"]["html_url"],
                            "Type": run["actor"]["type"],
                            "Site Admin": run["actor"]["site_admin"]
                        },
                        "Triggering Actor": {
                            "Login": run["triggering_actor"]["login"],
                            "ID": run["triggering_actor"]["id"],
                            "HTML URL": run["triggering_actor"]["html_url"],
                            "Type": run["triggering_actor"]["type"],
                            "Site Admin": run["triggering_actor"]["site_admin"]
                        },
                        "Head Commit": {
                            "ID": run["head_commit"]["id"],
                            "Message": run["head_commit"]["message"],
                            "Timestamp": run["head_commit"]["timestamp"],
                            "Author": {
                                "Name": run["head_commit"]["author"]["name"],
                                "Email": run["head_commit"]["author"]["email"]
                            },
                            "Committer": {
                                "Name": run["head_commit"]["committer"]["name"],
                                "Email": run["head_commit"]["committer"]["email"]
                            }
                        },
                    })

                if len(workflow_runs) < per_page:
                    break

                page += 1

        except requests.RequestException as e:
            logging.error(f"Error fetching runs for {owner}/{repo}. Error: {e}")

        return runs_details

    def get_workflow_jobs(self, owner, repo, run_id):
        """
        Fetch and filter jobs for a specific workflow run, handling pagination.

        Args:
            owner (str): The owner of the repository.
            repo (str): The name of the repository.
            run_id (int): The ID of the workflow run.

        Returns:
            list: A list of dictionaries containing job details and associated steps.
        """
        jobs_details = []
        page = 1
        per_page = 100
        url = f'https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/jobs'
        total_count_logged = False

        try:
            while True:
                params = {'page': page, 'per_page': per_page}
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()

                jobs = response.json().get("jobs", [])
                total_count = response.json().get("total_count", 0)
                total_pages = math.ceil(total_count / per_page)

                if not total_count_logged:
                    logging.info(f"Found {total_count} jobs for run ID {run_id}.")
                    total_count_logged = True
                logging.info(f"Processing page {page} of {total_pages} for run ID {run_id}.")

                for job in jobs:
                    jobs_details.append({
                        "ID": job["id"],
                        "Workflow Name": job["workflow_name"],
                        "Head Branch": job["head_branch"],
                        "Run Attempt": job["run_attempt"],
                        "Status": job["status"],
                        "Conclusion": job["conclusion"],
                        "Started At": job["started_at"],
                        "Completed At": job["completed_at"],
                        "Name": job["name"],
                        "Steps": [
                            {
                                "Name": step["name"],
                                "Status": step["status"],
                                "Conclusion": step.get("conclusion"),
                                "Number": step["number"],
                                "Started At": step["started_at"],
                                "Completed At": step["completed_at"]
                            }
                            for step in job.get("steps", [])
                        ]
                    })

                if len(jobs) < per_page:
                    break

                page += 1

        except requests.RequestException as e:
            logging.error(f"Error fetching jobs for run {run_id} on page {page}: {e}")

        return jobs_details

    def get_log_download_url(self, owner, repo, run_id):
        """
        Fetches the download URL for the logs of a specific workflow run.

        Args:
            owner (str): The owner of the repository.
            repo (str): The name of the repository.
            run_id (int): The ID of the workflow run.

        Returns:
            str: The URL to download the logs.
            None: If an error occurs or the URL is not available.
        """
        try:
            # Step 1: Call the API to get the logs
            url = f'https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/logs'
            response = requests.get(url, headers=self.headers, allow_redirects=False)
            response.raise_for_status()

            # Step 2: Extract the log download URL from the "Location" header
            log_download_url = response.headers.get("Location")
            if log_download_url:
                logging.info(f"Log's download URL for run {run_id} obtained successfully.")
                return log_download_url
            else:
                logging.error(f"No download URL found for logs of run {run_id}.")
                return None

        except requests.RequestException as e:
            logging.error(f"Error fetching log download URL for run {run_id}: {e}")
            return None

