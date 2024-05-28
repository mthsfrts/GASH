import csv
import logging
import os
import sys
import re
import shutil
from urllib.parse import urlparse
from pydriller import Repository, ModificationType
import GHMining as GHm
from os.path import dirname, abspath

d = dirname(dirname(abspath(__file__)))
sys.path.append(d)

import Analysis.Parse.GHYamlParse as GHYamlParse
from Analysis.Smells.Detectors import WorkflowDispatchDetector as Wd, ContinuesOnErrorDetector as CoE, \
    GlobalsDetector as Globals, RetriesDetectors as Retries, CodeQualityDetector as Cq, \
    ConditionsDetector as Conditionals, VulnerabilityDetector as Vulnerability


class Utils:
    @classmethod
    def handle_none(cls, value):
        return "None" if value is None else value


class GASH:
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
        output_csv = f"gash_{repo_name}.csv"

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
            "Diff",
            "vul",
            "glb",
            "retries",
            "coe",
            "cq",
            "conditions",
            "wd"
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
                        issue_tracker = GASH.extract_issue_numbers(commit.msg)

                        for issue_number in issue_tracker:
                            mining_instance = GHm.Mining()
                            # getting commit info
                            commit_gh = mining_instance.fetch_specific_commit(owner, repo_name, commit.hash)

                            # getting issue info
                            issues = mining_instance.fetch_specific_issues(owner, repo_name, issue_number)

                            if modification.source_code is not None:
                                anti_patterns_detector = SmellsDetector(modification.source_code)
                                vul, glb, retries, coe, cq, conditions, wd = anti_patterns_detector.analyses()

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
                                     modification.diff,
                                     vul,
                                     glb,
                                     retries,
                                     coe,
                                     cq,
                                     conditions,
                                     wd
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
        for repo_url in CSVHandler.reading_repos(csv_path):
            GASH.commits(repo_url)


class SmellsDetector:
    def __init__(self, diff):
        self.diff = diff

    def analyses(self):
        parser = GHYamlParse.YAMLParser(content=self.diff)
        workflow_obj = parser.prepare_for_analysis()

        vul_detector_result = Vulnerability.VulnerabilityDetector(workflow=workflow_obj).detect()
        global_detector_issue, global_detector_result = Globals.GlobalVariableDetector(
            content=workflow_obj.raw_content).detect()
        retries_detector_result = Retries.RetryDetector(content=workflow_obj.raw_content).detect()
        coe_detector_result = CoE.ContinueOnErrorDetector(content=workflow_obj.raw_content).detect()
        cq_detector_result = Cq.CodeQualityDetector(workflow=workflow_obj).detect()
        conditions_detector_result = Conditionals.ConditionsDetector(workflow=workflow_obj).detect()
        wd_detector_result = Wd.WorkFlowDispatchDetector(workflow=workflow_obj).detect()

        vul_detector = True if vul_detector_result else False
        global_detector = global_detector_issue
        retries_detector = True if retries_detector_result else False
        coe_detector = True if coe_detector_result else False
        cq_detector = True if cq_detector_result else False
        conditions_detector = True if conditions_detector_result else False
        wd_detector = True if wd_detector_result else False

        return (vul_detector, global_detector, retries_detector, coe_detector,
                cq_detector, conditions_detector, wd_detector)


class CSVHandler:
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


if __name__ == "__main__":
    repo = "https://github.com/prisma/prisma"
    GASH.commits(repo)
