import argparse
import configparser
import glob
import readline
import re
import sys
from os.path import abspath, dirname, expanduser, join
from urllib.parse import urlparse
import os

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
from Analysis.Smells.Categories.Security.SecurityFlaws.SecurityFlawsFct import SecurityFlawsFct
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
    def __init__(self, gh_token):
        self.api = GitHub.GitHubAPI(gh_token)
        self.parser = ActionParser
        self.utils = Utilities
        self.miner = Mining
        self.gh_token = gh_token
        self.detectors = {}

    def initialize_detectors(self, workflow):
        self.detectors = {
            'CodeReplica': CodeReplicaFct(workflow),
            'ErrorHandling': ErrorHandlingFct(workflow),
            'Misconfiguration': MisconfigurationFct(workflow),
            'LongBlock': LongBlockFct(workflow),
            'AdminByDefault': AdminByDefaultFct(workflow),
            'HardCoded': HardCodedFct(workflow),
            'RemoteRun': RemoteRunFct(workflow),
            'SecurityFlaws': SecurityFlawsFct(workflow),
            'UnsecureProtocol': UnsecureProtocolFct(workflow),
            'UntrustedDependencies': UntrustedDependenciesFct(workflow, self.gh_token)
        }

    def main(self):
        parser = argparse.ArgumentParser(
            description='GASH - GitHub Actions Smells and Miner CLI',
            epilog='For more information, visit https://yourprojectdocs.example.com',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage='%(prog)s <command> [subcommand]',
        )

        subparsers = parser.add_subparsers(dest='command', help='subcommand, description')

        # Subcommand for mining
        parser_repo = subparsers.add_parser(
            'repo',
            help='--age: Age in years --stars: Total of stars, Mine GitHub repositories.',
            description='Mine GitHub repositories based on age and stars.'
        )
        parser_repo.add_argument('--age', type=int, help='The age of the repository in years.')
        parser_repo.add_argument('--stars', type=str, help='The number of stars the repository has.')

        parser_mine = subparsers.add_parser(
            'commits',
            help='--url, Mine GitHub commits from a specified repository URL.',
            description='Mine GitHub commits from a specified repository URL.'
        )
        parser_mine.add_argument('--url', type=str, help='GitHub repository URL to mine.')

        parser_batch = subparsers.add_parser(
            'batch',
            help='--file: File Path --column: Column Number, '
                 'Mine GitHub repositories commits in batches from a CSV file.',
            description='Mine GitHub repositories commits in batches from a CSV file.'
        )
        parser_batch.add_argument('--file', type=str, help='CSV file path containing GitHub repositories URL to mine.')
        parser_batch.add_argument('--column', type=int, help='Column number of the contain the URLs.')

        # Subcommand for analyzing smells
        parser_analyze = subparsers.add_parser(
            'analyze',
            help='--file: File Path, Analyze GitHub Actions file for smells.',
            description='Analyze GitHub Actions file for smells.'
        )
        parser_analyze.add_argument('--file', type=str, help='GitHub Actions file path to analyze.')

        args = parser.parse_args()

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

        if args.command == 'commits':
            url = args.url

            if not url:
                url = input("Please enter the GitHub repository URL to mine: ")

            repo_name = urlparse(url).path.split('/')[2]
            print(f"Mining GitHub repository: {repo_name}")
            worker = self.miner.Mining(_token)
            worker.commits(url)

        elif args.command == 'repo':
            age = args.age
            stars = args.stars

            if not age or not stars:
                print("I need you to fill out some information to mine the GitHub repository.")
                age = input("Please enter the age of the repository in years: ")
                stars = input("Please enter the number of stars the repository has: ")

            print(f"Mining that match the filters age +{age} and stars +{stars}...")
            worker = self.miner.Mining(_token)
            worker.repo(age, stars)

        elif args.command == 'batch':
            _file = args.file
            column = args.column

            if _file is None or column is None:
                readline.set_completer_delims(' \t\n;')
                readline.parse_and_bind("tab: complete")
                readline.set_completer(complete_path)
                _file = input('Please provide a csv file path: ')
                column = input('Please provide a column number that contains the URLs: ')

            print(f'Mining repositories listed in the file: {_file}')
            worker = self.miner.Mining(_token)
            worker.batch(f'{_file}', column)

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

            self.initialize_detectors(workflow)

            for detector_name, detector in self.detectors.items():
                findings = detector.detect()
                print(f"\nFindings for {detector_name}:")
                if findings:
                    for finding in findings:
                        for line in re.split(r',\s*(?![^{}]*})', finding):
                            print(f"- {line.strip()}")
                else:
                    print("No findings detected.")

        else:
            parser.print_help()


if __name__ == '__main__':
    gash = GASH(gh_token=None)
    gash.main()
