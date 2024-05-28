import csv
import logging
import os
import sys
import re
import shutil
import requests
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from pydriller import Repository, ModificationType
from os.path import dirname, abspath

d = dirname(dirname(abspath(__file__)))
sys.path.append(d)


class Utils:
    @classmethod
    def handle_none(cls, value):
        return "None" if value is None else value


class CSVHandlerCommit:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def reading_repos(self):
        """
        Reads the CSV file containing repository URLs.
        Yields:
            str: The URL of each repository read from the CSV file.
        """
        with open(self.csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                repo_url = row[3]
                yield repo_url


class CSVHandlerRepo:
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
        CSVHandlerRepo.save_to_csv(repos_with_yml, filename)
        print("DataSet Created")

    @staticmethod
    def extract_issue_numbers(commit_msg):
        """Extract the issue number from a commit message"""
        pattern = r"\(#(\d+)\)"
        matches = re.findall(pattern, commit_msg)
        return matches

    @staticmethod
    def commits(repo_url):

        # Logging config
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # getting repo and owner names
        owner = urlparse(repo_url).path.split('/')[1]
        repo_name = urlparse(repo_url).path.split('/')[2]

        extension1 = "yaml"
        extension2 = "yml"
        output_csv = f"commit_{repo_name}.csv"

        # Creating Directory to save files
        base_dir = "generated"
        os.makedirs(base_dir, exist_ok=True)

        dataset_dir = os.path.join(base_dir, "database")
        os.makedirs(dataset_dir, exist_ok=True)

        saved_files_dir = os.path.join(base_dir, "scripts", repo_name)
        os.makedirs(saved_files_dir, exist_ok=True)

        saved_ymls_dir = os.path.join(saved_files_dir, "current_code")
        os.makedirs(saved_ymls_dir, exist_ok=True)

        src_before_dir = os.path.join(saved_files_dir, "files_src_before")
        os.makedirs(src_before_dir, exist_ok=True)

        src_after_dir = os.path.join(saved_files_dir, "files_src_after")
        os.makedirs(src_after_dir, exist_ok=True)

        # CSV
        headers = [
            "Project",
            "Author",
            "Author Acc Type",
            "Author Email",
            "Commiter",
            "Commiter Acc Type",
            "Commiter Email",
            "Commit",
            "Commit Parent",
            "Commit Date",
            "Commit Message",
            "Number of Files Changed by Commit",
            "Release",
            "Files Names",
            "Type Of Commit",
            "Added lines",
            "Deleted lines",
            "Token Count",
            "Issue Tracker",
            "Issue Creator",
            "Issue Creator Acc type",
            "Issue Creator Association",
            "Issue Closer",
            "Issue Closer Acc Type",
            "Issue Created At",
            "Issue Closed At",
            "Issue State",
            "Issue Labels",
            "Issue Reviewers",
            "Issue Reviewers Acc Type",
            "Issue Body",
            "Path Src Code Current",
            "Path Src Code Before",
            "Path Src Code After",
            "DMM_Unit",
            "DMM_Complexity",
            "DMM_Interfacing",
            "Diff"
        ]

        # Updating path of the csv
        output_csv_path = os.path.join(dataset_dir, output_csv)

        with (open(output_csv_path, mode='w', newline='', encoding='utf-8') as csvfile):
            writer = csv.writer(csvfile)
            writer.writerow(headers)

            logging.info("Creating Dataset...")

            for commit in Repository(repo_url, histogram_diff=True).traverse_commits():
                for modification in commit.modified_files:

                    # Creating short commit hash
                    short_hash = commit.hash[:7]

                    # Getting the right path, existing or not
                    filepath = (modification.new_path if modification.change_type != ModificationType.DELETE
                                else modification.old_path)

                    # Verifying is the file is on the right path of the repo
                    if (filepath and filepath.startswith('.github/workflows/') and
                            (filepath.endswith(f'.{extension1}') or filepath.endswith(f'.{extension2}'))):

                        # Checking the files' status
                        if modification.change_type.name == "DELETE":
                            source_path = None
                        else:
                            source_path = os.path.join(commit.project_path, modification.new_path)

                        # Saving files
                        before_filepath = os.path.join(src_before_dir, f"{short_hash}_{modification.filename}")
                        with open(before_filepath, 'w', encoding='utf-8') as file:
                            file.write(modification.source_code_before if modification.source_code_before else "")

                        after_filepath = os.path.join(src_after_dir, f"{short_hash}_{modification.filename}")
                        with open(after_filepath, 'w', encoding='utf-8') as file:
                            file.write(modification.source_code if modification.source_code else "")

                        # Filtering the copy current files
                        if source_path and os.path.exists(source_path):
                            destination_path = os.path.join(saved_ymls_dir, os.path.basename(modification.new_path))
                            shutil.copy2(source_path, destination_path)
                        else:
                            logging.warning(f"File {source_path} not found.")

                        # Getting issue number
                        issue_tracker = Dataset.extract_issue_numbers(commit.msg)

                        for issue_number in issue_tracker:
                            mining_instance = GHm.Mining()
                            # getting commit info
                            commit_gh = mining_instance.fetch_specific_commit(owner, repo_name, commit.hash)

                            # getting issue info
                            issues = mining_instance.fetch_specific_issues(owner, repo_name, issue_number)

                            if modification.source_code is not None:
                                continue

                            if issues:  # checking if that commit is really an issue
                                issue_creator = issues[0]['Creator']
                                issue_creator_association = issues[0]['Creator association']
                                issue_creator_type = issues[0]['Creator type']
                                issue_created_at = issues[0]['Created At']
                                issue_closed_at = issues[0]['Closed At']
                                issue_state = issues[0]['State']
                                issue_body = issues[0]['Body']
                                issue_closer = issues[0]['Closer']
                                issue_closer_type = issues[0]['Closer type']
                                issue_labels = issues[0]['Labels']
                                issue_reviewers = issues[0]['Reviewers/Assignees']
                                issue_reviewers_type = issues[0]['Reviewers/Assignees type']
                                # is_pull_request = issues[0]['Is Pull Request']
                                issue_milestone = issues[0]['Milestone']
                                auth_acc_type = commit_gh[0]['Author Acc']
                                comt_acc_type = commit_gh[0]['Committer Acc']

                                writer.writerow(
                                    [commit.project_name,
                                     commit.author.name,
                                     auth_acc_type,
                                     commit.author.email,
                                     commit.committer.name,
                                     comt_acc_type,
                                     commit.committer.email,
                                     commit.hash,
                                     commit.parents[-1] if commit.parents else None,
                                     commit.committer_date,
                                     commit.msg,
                                     commit.files,
                                     issue_milestone,
                                     modification.filename,
                                     modification.change_type.name,
                                     modification.added_lines,
                                     modification.deleted_lines,
                                     modification.token_count,
                                     ','.join(issue_tracker),
                                     issue_creator,
                                     issue_creator_type,
                                     issue_creator_association,
                                     issue_closer,
                                     issue_closer_type,
                                     issue_created_at,
                                     issue_closed_at,
                                     issue_state,
                                     issue_labels,
                                     issue_reviewers,
                                     issue_reviewers_type,
                                     issue_body,
                                     f'../Mining/{saved_ymls_dir}/{modification.filename}',
                                     f'../Mining/{before_filepath}',
                                     f'../Mining/{after_filepath}',
                                     Utils.handle_none(commit.dmm_unit_size),
                                     Utils.handle_none(commit.dmm_unit_complexity),
                                     Utils.handle_none(commit.dmm_unit_interfacing),
                                     modification.diff
                                     ])

                                logging.info(f"Project: {commit.project_name}")
                                logging.info(f"Author: {commit.author.name}")
                                logging.info(f"Committer: {commit.committer.name}")
                                logging.info(f"File: {modification.filename}")
                                logging.info(f"Message: {commit.msg}")
                                logging.info(f"Modification Type: {modification.change_type.name}")
                                logging.info(f"Issues: {len(issue_tracker)}")
                                logging.info(f"Issue Labels: {issue_labels}")
                                logging.info(f"Created At: {issue_created_at}")
                                logging.info(f"Closed At: {issue_closed_at}")
                                logging.info(f"State: {issue_state}")
                                logging.info(f"Release: {issue_milestone}")
                                logging.info("-" * 40)

                            else:
                                logging.warning(f"No issue generated found for issue numbers: {issue_tracker}")

            logging.info("Dataset Created.")

    @staticmethod
    def getting_repos(csv_path):
        for repo_url in CSVHandlerCommit.reading_repos(csv_path):
            Mining.commits(repo_url)


# actions_mining = 'https://api.github.com/repos/prisma/prisma/actions/workflows'
# runs_mining = 'https://api.github.com/repos/prisma/prisma/actions/runs'
# jobs_mining = 'https://api.github.com/repos/prisma/prisma/actions/runs/6485318535/jobs'
# step_mining = 'https://api.github.com/repos/prisma/prisma/actions/jobs/17611151000'
# check_run_mining = 'https://api.github.com/repos/prisma/prisma/check-runs/17611151000'
# annotation_mining = 'https://api.github.com/repos/prisma/prisma/check-runs/17611151000/annotations'

if __name__ == "__main__":
    repo = "https://github.com/prisma/prisma"
    Mining.main_repo_search()
    Mining.commits(repo)
