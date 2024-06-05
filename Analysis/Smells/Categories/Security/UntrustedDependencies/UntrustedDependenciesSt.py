import logging
import re
from Mining.Mining import Mining


class MainUntrustedDependenciesCheck:
    """
    Strategy to check for untrusted dependencies in Actions scripts.
    """

    def __init__(self):
        self.mining = Mining()

    def check(self, content=None):
        """
        Strategy to check for untrusted dependencies in Actions scripts.

        Attributes:
            content: Content of the workflow file

        Returns:
            findings: List of findings
        """
        findings = []

        # Check jobs level
        for job_name, job in content.jobs.items():
            logging.debug(f"Checking job level: {job_name}, uses: {job.uses}")
            findings.extend(self._check_uses(job.uses, f'job {job_name}'))

            # Check steps level
            for step in job.steps:
                logging.debug(f"Checking step level: {step.uses}")
                findings.extend(self._check_uses(step.uses, f'step in job {job_name}'))

        return findings

    def _check_uses(self, uses, level):
        findings = []
        if uses:
            match = re.match(r'([^/]+)/([^@]+)@(.+)', uses)
            if match:
                user, repo, version = match.groups()
                logging.debug(f"Checking {level} uses: user={user}, repo={repo}, version={version}")
                owner_verified, verification_badge = self.mining.fetch_action_verification(user, repo)
                if not owner_verified and not verification_badge:
                    findings.append(f"Untrusted dependency found in {level}: {uses}. "
                                    f"Consider using actions from verified creators.")
                vulnerabilities = self.mining.get_repository_vulnerabilities(user, repo)
                if vulnerabilities:
                    findings.append(f"Vulnerabilities found in {level}: {uses}. "
                                    f"Details: {vulnerabilities}")
        return findings
