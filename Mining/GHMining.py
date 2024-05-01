import os
import csv
import requests
import logging
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor


class GitHubAPI:

    def __init__(self):
        self.token = os.environ.get('GITHUB_TOKEN')
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    @classmethod
    def get_rate_limit(cls):
        url = "https://api.github.com/rate_limit"
        response = requests.get(url, headers=cls().headers)
        if response.status_code == 200:
            data = response.json()
            limit = data['resources']['core']['limit']
            used = data['resources']['core']['used']
            remaining = data['resources']['core']['remaining']
            logging.info(f"Limite de requisições: {limit}. Usado: {used}. Restante: {remaining}.")
        else:
            logging.error("Error getting the rate limit.")


class CSVHandler:
    def __init__(self):
        pass

    @staticmethod
    def save_to_csv(repos, filename):
        base_dir = "generated"
        os.makedirs(base_dir, exist_ok=True)

        dataset_dir = os.path.join(base_dir, "database")
        os.makedirs(dataset_dir, exist_ok=True)

        file_path = os.path.join(dataset_dir, filename)

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            headers = ["Owner", "Repo", "Description", "URL", "Language", "Stars", "Open Issues Count",
                       "Created At", "Updated At", "Size", "Has Downloads", "YML Count", "YML Files"]
            writer.writerow(headers)
            for repo in repos:
                writer.writerow([
                    repo['Owner'], repo["Name"], repo["Description"], repo["Url"], repo["Language"], repo["Stars"],
                    repo["Issue Count"], repo["Created At"], repo["Updated At"], repo["Size"], repo["Downloads"],
                    repo["YML Count"], repo["YML Files"]
                ])


class Mining:
    def __init__(self):
        self.github_api = GitHubAPI()

    def has_workflow_files(self, repo_full_name):
        """Returns the names of the .yml or .yaml files in the
        .GitHub/workflows folder, or None if there are no files."""
        workflows_url = f"https://api.github.com/repos/{repo_full_name}/contents/.github/workflows"
        response = requests.get(workflows_url, headers=self.github_api.headers)
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
            response = requests.get(url, headers=self.github_api.headers)
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
            response = requests.get(url, headers=self.github_api.headers)
            response.raise_for_status()

            commit = response.json()

            commit_author_type = commit['author']['type'] if commit['author'] else None
            commit_committer_type = commit['committer']['type'] if commit['committer'] else None
            commit_tree = commit['commit']['tree']['sha']
            commit_files = [files['filename'] for files in commit['files']]

            logging.info(f"Getting Additional Info From Commit: {commit_sha}")

            # logging.info("-" * 40)

            # retornando uma lista contendo um dicionário com alguns campos.
            filtered_commits.append({
                "Author Acc": commit_author_type,
                "Committer Acc": commit_committer_type,
                "Tree": commit_tree,
                "Files": ", ".join(commit_files)

            })

            # print(json.dumps(commit, indent=4))
            # print("-" * 40)
            # print(filtered_commits)

        except requests.RequestException as e:
            logging.error(f"Erro ao buscar o commit {commit_sha}. Error: {e}")

        return filtered_commits

    def fetch_specific_issues(self, owner, repo_name, issue_number):
        """Fetch information about specific issues based on your Issue list."""
        filtered_issues = []

        try:
            url = f'https://api.github.com/repos/{owner}/{repo_name}/issues/{issue_number}'
            response = requests.get(url, headers=self.github_api.headers)
            response.raise_for_status()

            issue = response.json()
            if 'pull_request' not in issue:  # Ignora pull requests, considera apenas issues
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
            # print(json.dumps(issue, indent=4))
            # print("-" * 40)
            # print(filtered_issues)

        except requests.RequestException as e:
            logging.error(f"Error when searching for issue #{issue_number}. Error: {e}")

        return filtered_issues

    @staticmethod
    def threaded_analyses(query, sort='stars', order='desc', max_pages=10):
        """Search and filter repositories that have the desired files in a single function."""
        filtered_repos = []

        with ThreadPoolExecutor(max_workers=20) as executor:
            mining_instance = Mining()
            futures = [
                executor.submit(mining_instance.fetch_repo, query, sort, order, page) for page in
                range(1, max_pages + 1)
            ]
            for future in futures:
                filtered_repos.extend(future.result())

        return filtered_repos

    @staticmethod
    def main_repo_search():
        """ Search for repos using filters to qualify them. """
        # logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        print("Creating DataSet")
        GitHubAPI.get_rate_limit()

        date_cutoff = (datetime.now() - timedelta(days=5 * 365)).strftime('%Y-%m-%d')
        stars = 3000

        all_repos = []

        query = (
            "is:public "
            f"created:<{date_cutoff} "
            f"stars:>{stars} "
        )

        repos_for_this_extension = Mining.threaded_analyses(query)
        all_repos.extend(repos_for_this_extension)

        repos_with_yml = [repo for repo in all_repos if repo.get("hasYml", False)]

        filename = "repos_dataset.csv"
        CSVHandler.save_to_csv(repos_with_yml, filename)
        print("DataSet Created")


# actions_mining = 'https://api.github.com/repos/prisma/prisma/actions/workflows'
# runs_mining = 'https://api.github.com/repos/prisma/prisma/actions/runs'
# jobs_mining = 'https://api.github.com/repos/prisma/prisma/actions/runs/6485318535/jobs'
# step_mining = 'https://api.github.com/repos/prisma/prisma/actions/jobs/17611151000'
# check_run_mining = 'https://api.github.com/repos/prisma/prisma/check-runs/17611151000'
# annotation_mining = 'https://api.github.com/repos/prisma/prisma/check-runs/17611151000/annotations'

if __name__ == "__main__":
    Mining.main_repo_search()
    # fetch_specific_issues("prisma", "prisma", "6066")
    # fetch_specific_commit("prisma", "prisma", "5e23e88e083c6f9bd942fb119e29e69c72777799")
