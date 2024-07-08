import re
import logging
from Utils.Utilities import Lists


class MainHardCodedCheck:
    """
    Strategy to check for hard-coded secrets in Actions scripts

    Attributes:
        content: Content of the file to check
        keywords: List of keywords to search for in the scripts
        regex: List of regex patterns to search for in the scripts
        safe Pattern: Pattern to search for safe secrets

    Returns:
        Findings: List of Hard-Coded secrets found
    """

    def __init__(self):
        self.keywords = Lists.keywords
        self.regex = [re.compile(pattern, re.IGNORECASE) for pattern in Lists.regex_patterns]
        self.safe_pattern = re.compile(r'\${{\s*secrets\.\w+\s*}}')

    def check(self, content=None):
        """
        Method to check hard-coded secrets

        Attributes:
            content: Content of the file to check

        Returns:
            findings: List of findings
        """
        findings = []

        # Check workflow level
        logging.debug(f"Checking workflow level: {content.env}")
        findings.extend(self._check_env(content.env, 'workflow'))

        # Check jobs level
        for job_name, job in content.jobs.items():
            logging.debug(f"Checking job level: {job_name}, env: {job.env}")
            findings.extend(self._check_env(job.env, f'job {job_name}'))

            # Check services level
            if job.services:
                for service_name, service in job.services.items():
                    logging.debug(f"Checking service level: {service_name}")
                    if 'env' in service:
                        findings.extend(self._check_env(service['env'], f'service {service_name} in job {job_name}'))
                    if 'credentials' in service:
                        findings.extend(
                            self._check_env(service['credentials'], f'service {service_name} in job {job_name}'))

            # Check steps level
            for step in job.steps:
                logging.debug(f"Checking step level: {step.env}")
                findings.extend(self._check_env(step.env, f'step in job {job_name}'))

                if step.run:
                    logging.debug(f"Checking run command: {step.run}")
                    findings.extend(self._check_run(step.run, f'step in job {job_name}'))

        return findings

    def _check_env(self, env, level):
        findings = []
        for key, value in env.items():
            value_str = str(value).lower()
            key_str = str(key).lower()
            if (any(pattern.search(key_str) for pattern in self.regex)
                    and not self.safe_pattern.search(value_str)):
                findings.append(f"Hard-coded secret in {level} env '{key}'")
            elif (any(
                    keyword.lower() in key_str for keyword in self.keywords)
                  and not self.safe_pattern.search(value_str)):
                findings.append(f"Hard-coded secret in {level} env '{key}'")
        return findings

    def _check_run(self, run, level):
        findings = []
        run_str = str(run)
        if any(pattern.search(run_str) for pattern in self.regex):
            findings.append(f"Hard-coded secret in {level} run command '{run}'")
        elif any(keyword.lower() in run_str.lower() for keyword in self.keywords):
            findings.append(f"Hard-coded secret in {level} run command '{run}'")
        return findings
