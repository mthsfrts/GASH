import logging
import re
import sys
from os.path import dirname, abspath

d = dirname(dirname(abspath(__file__)))
sys.path.append(d)

from APIs import GitHub


class MainUntrustedDependenciesCheck:
    """
    Strategy to check for untrusted dependencies in Actions scripts.
    """

    def __init__(self, token):
        self.api = GitHub
        self.token = token

    def check(self, content=None):
        """
        Method to check untrusted dependencies.

        Attributes:
            content: Content of the workflow file

        Returns:
            findings: List of findings
        """
        findings = []

        # Check jobs level
        for job_name, job in content.jobs.items():
            logging.debug(f"Checking job level: {job_name}, uses: {job.uses}")
            findings.extend(self._check_uses(job.uses, f'job {job_name}', self.token))

            # Check steps level
            for step in job.steps:
                logging.debug(f"Checking step level: {step.uses}")
                findings.extend(self._check_uses(step.uses, f'step in job {job_name}', self.token))

        return findings

    def _check_uses(self, uses, level, token):
        findings = []
        call = self.api.GitHubAPI(token)

        if uses:
            match = re.match(r'([^/]+)/([^@]+)@(.+)', uses)
            if match:
                user, repo, version = match.groups()
                logging.debug(f"Checking {level} uses: user={user}, repo={repo}, version={version}")
                owner_verified, verification_badge = call.fetch_action_verification(user, repo)
                if not owner_verified and not verification_badge:
                    findings.append(f"Unverified dependency found in {level}: {uses}. "
                                    f"Consider using actions from verified creators.")
                vulnerabilities = call.get_repository_vulnerabilities(user, repo)
                if vulnerabilities:
                    findings.append(f"Vulnerabilities found in {level}: {uses}. "
                                    f"Details: {vulnerabilities}")
        return findings
