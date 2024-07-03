import argparse
import configparser
import glob
import readline
import re
import sys
from os.path import abspath, dirname, expanduser, join
from urllib.parse import urlparse
import os
import time

d = dirname(dirname(abspath(__file__)))
sys.path.append(d)

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

from APIs import GitHub
from Miner import Mining
from Utils import Utilities

# Define the path to the configuration file in the user's home directory
CONFIG_DIR = join(expanduser("~"), ".gash")
CONFIG_FILE = join(CONFIG_DIR, 'config.ini')


def save_token(token):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    config = configparser.ConfigParser()
    config['github'] = {'token': token}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def load_token():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        print(f"Config file found: {CONFIG_FILE}")
        config.read(CONFIG_FILE)
        if 'github' in config and 'token' in config['github']:
            return config['github']['token']
    print("No valid token found in config file")
    return None


def complete_path(text, state):
    return [x for x in glob.glob(text + '*')][state]


class GASH:
    def __init__(self, token):
        self.token = token
        self.api = GitHub.GitHubAPI(self.token)
        self.parser = ActionParser
        self.utils = Utilities
        self.miner = Mining
        self.detectors = {}

    def initialize_detectors(self, workflow, token):
        self.detectors = {
            'CodeReplica': CodeReplicaFct(workflow),
            'ErrorHandling': ErrorHandlingFct(workflow),
            'Misconfiguration': MisconfigurationFct(workflow),
            'LongBlock': LongBlockFct(workflow),
            'AdminByDefault': AdminByDefaultFct(workflow),
            'HardCoded': HardCodedFct(workflow),
            'RemoteRun': RemoteRunFct(workflow),
            'UnsecureProtocol': UnsecureProtocolFct(workflow),
            'UntrustedDependencies': UntrustedDependenciesFct(workflow, token)
        }

    def main(self):
        parser = argparse.ArgumentParser(
            description='GASH - GitHub Actions Smells Hunter',
            epilog='For more information, visit https://yourprojectdocs.example.com',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage='%(prog)s [-h] [-d] <command> [subcommand]',
        )

        subparsers = parser.add_subparsers(dest='command', help='subcommands, descriptions')

        # Subcommand for mining
        parser_repo = subparsers.add_parser(
            'repo',
            help='--age: Age in years --min: Minimum of stars --max: Maximum of stars, Mine GitHub repositories.',
            description='Mine GitHub repositories based on age and stars.'
        )
        parser_repo.add_argument('--age', type=int, help='The age of the repository in years.')
        parser_repo.add_argument('--min', type=str, help='The minimum number of stars to search.')
        parser_repo.add_argument('--max', type=str, help='The maximum number of stars to search.')

        parser_mine = subparsers.add_parser(
            'commits',
            help="--url: The repository's URL, Mine GitHub commits from a specified repository URL.",
            description='Mine GitHub commits from a specified repository URL.'
        )
        parser_mine.add_argument('--url', type=str, help='GitHub repository URL to mine.')

        parser_batch = subparsers.add_parser(
            'batch-commit',
            help='--file: CSV File Path '
                 '--url: Column Number '
                 'Mine GitHub repositories commits in batches from a CSV file.',
            description='Mine all commits in GitHub repositories from a list of URLs.'
        )
        parser_batch.add_argument('--file', type=str, help='CSV file path containing GitHub repositories URL to mine.')
        parser_batch.add_argument('--url', type=int, help='Column number containing the URLs.')

        # Subcommand for analyzing smells
        parser_analyze = subparsers.add_parser(
            'analyze',
            help='--file: File Path Analyze GitHub Actions file for smells.',

            description='Analyze GitHub Actions file for smells.'
        )
        parser_analyze.add_argument('--file', type=str, help='GitHub Actions file path to analyze.')

        parser_batch_analyze = subparsers.add_parser(
            'batch-analyze',
            help='--dir: Root Directory Path, Analyze all GitHub Actions files in the specified directory for smells.',
            description='Analyze all GitHub Actions files in the specified directory for smells.'
        )
        parser_batch_analyze.add_argument('--dir', type=str,
                                          help='Directory path containing GitHub Actions files to analyze.')

        parser.add_argument('-d', '--daemon', action='store_true', help='Run as a daemon in the background')

        args = parser.parse_args()

        if args.daemon:
            pid = os.fork()
            if pid > 0:
                sys.exit()
            os.setsid()
            pid = os.fork()
            if pid > 0:
                sys.exit()

            sys.stdout = open('/dev/null', 'w')
            sys.stderr = open('/dev/null', 'w')
            sys.stdin = open('/dev/null', 'r')

        if not args.command:
            parser.print_help()
            return

        _token = load_token()
        if not _token:
            print("\nHey there! I'm GASH, your friendly GitHub Actions Helper. 😊")
            print("Before we get started, I'll need your GitHub API token to work my magic.")
            print("Don't worry, if you already have it saved as an environment variable in your OS, you're all set!")
            print("Just let me know by typing 'yes'.")
            print("If you prefer to enter it manually, type 'no' and I'll store it securely for future use.")
            print(f"Your token will be safely stored in: {CONFIG_FILE}. You won't have to enter it again next time!")
            print("Let's get started and make your GitHub Actions awesome! 🚀\n\n")
            while True:
                answer1 = input("Enter 'yes' or 'no': ").strip().lower()
                if answer1 == 'yes':
                    env_name = input("Please enter your OS ENV name: ")
                    _token = os.environ.get(env_name)
                    if not _token:
                        print(f"No token found in environment variable {env_name}. Please try again.")
                        continue
                elif answer1 == 'no':
                    _token = input("Please enter your GitHub API token: ")
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
                    continue

        print("\nHey there! I'm GASH, your friendly GitHub Actions Helper. 😊")
        print("I will be using your stored GitHub API token.")
        print("Let's get started and make your GitHub Actions awesome! 🚀\n\n")

        api = GitHub.GitHubAPI(_token)
        status_code = api.get_rate_limit()

        if status_code == 200:
            save_token(_token)
            print("Proceeding with the operations...\n\n")
        else:
            print("Invalid token. Please try again.")
            return

        if args.command == 'repo':
            age = args.age
            _min = args.min
            _max = args.max

            if not age or not _min or not max:
                print("I need you to fill out some information to mine the GitHub repository.")
                age = input("Please enter the age of the repository in years: ")
                _min = input("Please enter the min number for the stars: ")
                _max = input("Please enter the max number for the stars: ")

            print(f"Mining that match the filters age max {age} and stars between {_min} and {_max}...")
            worker = self.miner.Mining(_token)
            worker.repo(age, _min, _max)

        elif args.command == 'commits':
            url = args.url

            if not url:
                url = input("Please enter the GitHub repository URL to mine: ")

            repo_name = urlparse(url).path.split('/')[2]
            print(f"Mining GitHub repository: {repo_name}")
            worker = self.miner.Mining(_token)
            worker.commits(url)

        elif args.command == 'batch-commit':
            _file = args.file
            url_column = args.url

            if _file is None or url_column is None:
                readline.set_completer_delims(' \t\n;')
                readline.parse_and_bind("tab: complete")
                readline.set_completer(complete_path)
                _file = input('Please provide a csv file path: ')
                url_column = input('Please provide a column number that contains the URLs: ')

            if not os.path.exists(_file):
                print(f"File not found: {_file}")
                return

            print(f'Mining repositories listed in the file: {_file}')
            worker = self.miner.Mining(_token)
            worker.batch(f'{_file}', url_column)

        elif args.command == 'analyze':
            _file = args.file

            if not _file:
                readline.set_completer_delims(' \t\n;')
                readline.parse_and_bind("tab: complete")
                readline.set_completer(complete_path)
                _file = input("Please enter the path to the GitHub Actions file: ")

            print(f"Analyzing GitHub Actions file: {_file}")
            action = self.parser.Action(file_path=f'{_file}')
            workflow = action.prepare_for_analysis()

            self.initialize_detectors(workflow, _token)

            for detector_name, detector in self.detectors.items():
                findings = detector.detect()
                print(f"\nFindings for {detector_name}:")
                if findings:
                    for finding in findings:
                        for line in re.split(r',\s*(?![^{}]*})', finding):
                            print(f"- {line.strip()}")
                else:
                    print("No findings detected.")

        elif args.command == 'batch-analyze':
            _dir = args.dir

            repo_dirs = glob.glob(_dir, recursive=True)

            if not repo_dirs:
                print(f"No repositories found in directory: {_dir}")
                return

            for repo_dir in repo_dirs:
                yaml_files = glob.glob(os.path.join(repo_dir, '**/*.yaml'), recursive=True)
                yaml_files.extend(glob.glob(os.path.join(repo_dir, '**/*.yml'), recursive=True))

                if not yaml_files:
                    print(f"No YAML files found in directory: {repo_dir}")
                    continue

                analysis_dir = os.path.join(os.path.dirname(repo_dir), 'GashAnalyses')
                os.makedirs(analysis_dir, exist_ok=True)
                print(f"Starting analysis for {len(yaml_files)} "
                      f"GitHub Actions files in directory: {repo_dir}\n")

                for file_path in yaml_files:
                    file_root, file_ext = os.path.splitext(os.path.basename(file_path))
                    log_file_path = os.path.join(analysis_dir, f'{file_root}.log')
                    print(f"Analyzing GitHub Actions file: {file_path}\n")
                    with open(log_file_path, 'w') as log_file:
                        action = self.parser.Action(file_path=file_path)
                        workflow = action.prepare_for_analysis()

                        attempts = 0
                        while attempts < 3:
                            try:
                                self.initialize_detectors(workflow, _token)
                                break
                            except Exception as e:
                                print(f"Error initializing detectors: {e}")
                                attempts += 1
                                if attempts < 3:
                                    print(f"Retrying in {3 * attempts} seconds...")
                                    time.sleep(3 * attempts)
                                else:
                                    print(f"Failed to initialize detectors after {attempts} attempts. Skipping file.")
                                    log_file.write(
                                        f"Failed to initialize detectors after {attempts} attempts. Skipping file.\n")
                                    break

                        if attempts < 3:
                            for detector_name, detector in self.detectors.items():
                                detection_attempts = 0
                                while detection_attempts < 5:
                                    try:
                                        findings = detector.detect()
                                        break
                                    except Exception as e:
                                        print(f"Error detecting with {detector_name}: {e}")
                                        detection_attempts += 1
                                        if detection_attempts < 3:
                                            print(f"Retrying detection in {10 * detection_attempts} seconds...")
                                            time.sleep(3 * detection_attempts)
                                        else:
                                            print(
                                                f"Failed to detect with {detector_name} after {detection_attempts} "
                                                f"attempts. Skipping detector.")
                                            log_file.write(
                                                f"Failed to detect with {detector_name} after {detection_attempts} "
                                                f"attempts.\n")
                                            findings = []

                                log_file.write(f"\nFindings for {detector_name} in {file_path}:\n")
                                if findings:
                                    for finding in findings:
                                        for line in re.split(r',\s*(?![^{}]*})', finding):
                                            log_file.write(f"- {line.strip()}\n")
                                else:
                                    log_file.write("No findings detected.\n")

                    print(f"Analysis complete for {file_path}.\n"
                          f"Log written to {log_file_path}.\n\n")
                    time.sleep(5)

        else:
            parser.print_help()


if __name__ == '__main__':
    gash = GASH(None)
    gash.main()
