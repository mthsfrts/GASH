import csv
import logging
import os
import sys
import re
import shutil
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from pydriller import Repository, ModificationType
from os.path import dirname, abspath

d = dirname(dirname(abspath(__file__)))
sys.path.append(d)

from APIs.GitHub import GitHubAPI
from Utils import Utilities
from Analysis.Parse import ActionParser
from Analysis.Smells.Categories.Maintenance.CodeReplica.CodeReplicaFct import CodeReplicaFct
from Analysis.Smells.Categories.Maintenance.ErrorHandling.ErrorHandlingFct import ErrorHandlingFct
from Analysis.Smells.Categories.Maintenance.Misconfiguration.MisconfigurationFct import MisconfigurationFct
from Analysis.Smells.Categories.Quality.LongBlocks.LongBlockFct import LongBlockFct
from Analysis.Smells.Categories.Security.AdminByDefault.AdminByDefaultFct import AdminByDefaultFct
from Analysis.Smells.Categories.Security.HardCoded.HardCodedFct import HardCodedFct
from Analysis.Smells.Categories.Security.RemoteTriggers.RemoteTriggersFct import RemoteRunFct
from Analysis.Smells.Categories.Security.UnsecureProtocol.UnsecureProtocolFct import UnsecureProtocolFct
from Analysis.Smells.Categories.Security.UntrustedDependencies.UntrustedDependenciesFct import UntrustedDependenciesFct


class Mining:
    def __init__(self, token):
        self.token = token
        self.github_api = GitHubAPI(self.token)
        self.handler = Utilities.Config
        self.parser = ActionParser

    def threaded_analyses(self, query, sort='stars', order='desc', max_pages=10):
        """Search and filter repositories that have the desired Parser in a single function."""
        filtered_repos = []

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [
                executor.submit(self.github_api.fetch_repo, query, sort, order, page) for page in
                range(1, max_pages + 1)
            ]
            for future in futures:
                filtered_repos.extend(future.result())

        return filtered_repos

    @staticmethod
    def extract_issue_numbers(commit_msg):
        """Extract the issue number from a commit message"""
        pattern = r"\(#(\d+)\)"
        matches = re.findall(pattern, commit_msg)
        return matches

    def repo(self, years, _min, _max):
        """ Search for repos using filters to qualify them.
            Attributes:
                years: Age of the repositories you want mining.
                stars: Number of stars to filter the repositories.

            Returns: CSV file with the repositories infos.
        """
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        print("Creating DataSet")
        self.github_api.get_rate_limit()

        date_cutoff = (datetime.now() - timedelta(days=years * 365)).strftime('%Y-%m-%d')

        all_repos = []

        query = (
            "is:public "
            f"created:>={date_cutoff} "
            f"stars:{_min}..{_max} "
        )

        repos_for_this_extension = self.threaded_analyses(query)
        all_repos.extend(repos_for_this_extension)

        repos_with_yml = [repo for repo in all_repos if repo.get("hasYml", False)]

        filename = "repos_dataset.csv"

        base_dir = self.handler.get_base_directory()
        os.makedirs(base_dir, exist_ok=True)

        dataset_dir = os.path.join(base_dir, "DataSets")
        os.makedirs(dataset_dir, exist_ok=True)

        file_path = os.path.join(dataset_dir, filename)

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            headers = ["Owner", "Repo", "Description", "URL", "Language", "Stars", "Open Issues count",
                       "Created At", "Updated At", "Size", "Has Downloads", "YML count", "YML Files"]
            writer.writerow(headers)

            for repo in repos_with_yml:
                writer.writerow([
                    repo['Owner'], repo["Name"], repo["Description"], repo["Url"], repo["Language"], repo["Stars"],
                    repo["Issue Count"], repo["Created At"], repo["Updated At"], repo["Size"], repo["Downloads"],
                    repo["YML Count"], repo["YML Files"]
                ])

        print("DataSet Created")

    def commits(self, repo_url):
        """
        Extract commits from a repository and save them to a CSV file.
        Attributes:
            repo_url: URL of the repository to be mined.

        Returns: CSV file with the commits infos.
        """

        # Logging config
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # getting repo and owner names
        owner = urlparse(repo_url).path.split('/')[1]
        repo_name = urlparse(repo_url).path.split('/')[2]

        extension1 = "yaml"
        extension2 = "yml"
        output_csv = f"commits_{repo_name}.csv"

        # Creating Directory to save Parser
        base_dir = self.handler.get_base_directory()
        os.makedirs(base_dir, exist_ok=True)

        dataset_dir = os.path.join(base_dir, "DataSets")
        os.makedirs(dataset_dir, exist_ok=True)

        saved_files_dir = os.path.join(base_dir, "Scripts", repo_name)
        os.makedirs(saved_files_dir, exist_ok=True)

        saved_ymls_dir = os.path.join(saved_files_dir, "CurrentCode")
        os.makedirs(saved_ymls_dir, exist_ok=True)

        src_before_dir = os.path.join(saved_files_dir, "FilesBefore")
        os.makedirs(src_before_dir, exist_ok=True)

        src_after_dir = os.path.join(saved_files_dir, "FilesAfter")
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
            "Token count",
            "Pull Request",
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
            "CodeReplica",
            "ErrorHandling",
            "Misconfiguration",
            "LongBlock",
            "AdminByDefault",
            "HardCoded",
            "RemoteTriggers",
            "UnsecureProtocol",
            "UntrustedDependencies",
            "Diff"
        ]

        # Updating path of the csv
        output_csv_path = os.path.join(dataset_dir, output_csv)

        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
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

                        # Checking the Parser status
                        if modification.change_type.name == "DELETE":
                            source_path = None
                        else:
                            source_path = os.path.join(commit.project_path, modification.new_path)

                        # Saving Parser
                        current_filepath = os.path.join(saved_ymls_dir, f"{modification.filename}")

                        before_filepath = os.path.join(src_before_dir, f"{short_hash}_{modification.filename}")
                        with open(before_filepath, 'w', encoding='utf-8') as file:
                            file.write(modification.source_code_before if modification.source_code_before else "")

                        after_filepath = os.path.join(src_after_dir, f"{short_hash}_{modification.filename}")
                        with open(after_filepath, 'w', encoding='utf-8') as file:
                            file.write(modification.source_code if modification.source_code else "")

                        # Filtering the copy current Parser
                        if source_path and os.path.exists(source_path):
                            destination_path = os.path.join(saved_ymls_dir, os.path.basename(modification.new_path))
                            shutil.copy2(source_path, destination_path)
                        else:
                            logging.warning(f"File {source_path} not found.")

                        # Getting issue number
                        issue_tracker = Mining.extract_issue_numbers(commit.msg)

                        # getting commit info
                        commit_gh = self.github_api.fetch_specific_commit(owner, repo_name, commit.hash)

                        # Getting issue info if available
                        issues = None
                        if issue_tracker:
                            issues = [self.github_api.fetch_specific_issues(owner, repo_name, issue_number) for
                                      issue_number in issue_tracker]

                        # Smell analysis
                        if modification.change_type.name != "DELETE":
                            file_path = current_filepath
                            if os.path.exists(file_path):
                                action = self.parser.Action(file_path=file_path)
                            else:
                                with open(after_filepath, 'r', encoding='utf-8') as file:
                                    file_content = file.read()
                                action = self.parser.Action(content=file_content)

                            workflow = action.prepare_for_analysis()

                            if workflow:
                                codereplica = bool(CodeReplicaFct(workflow).detect())
                                errorhandling = bool(ErrorHandlingFct(workflow).detect())
                                misconfiguration = bool(MisconfigurationFct(workflow).detect())
                                longblock = bool(LongBlockFct(workflow).detect())
                                adminbydefault = bool(AdminByDefaultFct(workflow).detect())
                                hardcoded = bool(HardCodedFct(workflow).detect())
                                triggers = bool(RemoteRunFct(workflow).detect())
                                unsecureprotocol = bool(UnsecureProtocolFct(workflow).detect())

                                # Retrying untrusted dependencies
                                attempts = 0
                                while attempts < 3:
                                    try:
                                        untrusteddependencies = bool(
                                            UntrustedDependenciesFct(workflow, self.token).detect())
                                        break
                                    except Exception as e:
                                        logging.error(f"Error processing untrusted dependencies detector. "
                                                      f"Attempt {attempts + 1} of 3. Error: {e}")
                                        attempts += 1
                                        if attempts < 3:
                                            logging.info(f"Retrying in {10 * attempts} seconds...")
                                            time.sleep(10 * attempts)
                                        else:
                                            if e == 404:
                                                logging.error(f"Failed to process the {modification.filename} "
                                                              f"file for untrusted dependencies. "
                                                              f"Dependency were not found, "
                                                              f"check if the name of dependency is right.")
                                                untrusteddependencies = True
                                            else:
                                                logging.error(f"Failed to process the {modification.filename} "
                                                              f"file for untrusted dependencies after 3 attempts. "
                                                              f"The dependency will be considered as untrusted."
                                                              f"Moving to the next one.")
                                                untrusteddependencies = True
                            else:
                                logging.error(f"Failed to prepare workflow for analysis from file: {file_path}")
                                continue

                        if commit_gh:
                            auth_acc_type = commit_gh[0]['Author Acc']
                            comt_acc_type = commit_gh[0]['Committer Acc']
                        else:
                            auth_acc_type = None
                            comt_acc_type = None

                        if issues:
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
                            is_pull_request = issues[0]['Is Pull Request']
                            issue_milestone = issues[0]['Milestone']
                        else:
                            issue_creator = None
                            issue_creator_association = None
                            issue_creator_type = None
                            issue_created_at = None
                            issue_closed_at = None
                            issue_state = None
                            issue_body = None
                            issue_closer = None
                            issue_closer_type = None
                            issue_labels = None
                            issue_reviewers = None
                            issue_reviewers_type = None
                            is_pull_request = None
                            issue_milestone = None

                        writer.writerow([
                            commit.project_name,
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
                            is_pull_request,
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
                            os.path.join(base_dir, current_filepath),
                            os.path.join(base_dir, before_filepath),
                            os.path.join(base_dir, after_filepath),
                            self.handler.handle_none(commit.dmm_unit_size),
                            self.handler.handle_none(commit.dmm_unit_complexity),
                            self.handler.handle_none(commit.dmm_unit_interfacing),
                            codereplica,
                            errorhandling,
                            misconfiguration,
                            longblock,
                            adminbydefault,
                            hardcoded,
                            triggers,
                            unsecureprotocol,
                            untrusteddependencies,
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

            logging.info("Dataset Created.")

    def batch(self, file, url, count, desired):
        """
        Responsible for mining commits from a batch of repositories.

        Attributes:
            file: CSV file with the repositories URLs.
            url: Column number with the repositories URLs.
            count: Column number with the total of yaml files.
            desired: The total number of files that will filter the repositories to be mined.

        Returns: CSV file with the commit info.
        """
        csv_file = self.handler(file)
        for repo_url in self.handler.reading_repos(csv_file, url, count, desired):
            attempts = 0
            while attempts < 3:
                try:
                    self.commits(repo_url)
                    break
                except Exception as e:
                    logging.error(f"Error processing repository {repo_url}. Attempt {attempts + 1} of 3. Error: {e}")
                    attempts += 1
                    if attempts < 3:
                        logging.info(f"Retrying in {10 * attempts} seconds...")
                        time.sleep(10 * attempts)
                    else:
                        logging.error(f"Failed to process repository {repo_url} "
                                      f"after 3 attempts. Moving to the next one.")
            time.sleep(30)
