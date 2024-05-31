import re
import logging


class MainUnsecureProtocolCheck:
    """
    Strategy to check for unsecure protocols in Actions scripts.

    Attributes:
        pattern : Regex pattern to identify HTTP URLs

    Returns:
        findings: List of unsecure protocol findings
    """

    def __init__(self):
        self.pattern = re.compile(r'\bhttp://\S+', re.IGNORECASE)

    def check(self, content=None):
        """
        Checking for unsecure protocols.

        Attributes:
            content: Content of the file to check

        Returns:
            findings: List of findings
        """
        findings = []

        # Check workflow level
        logging.debug(f"Checking workflow level: {content.env}")
        findings.extend(self._check_urls(content.env, 'workflow'))

        # Check jobs level
        for job_name, job in content.jobs.items():
            logging.debug(f"Checking job level: {job_name}, env: {job.env}")
            findings.extend(self._check_urls(job.env, f'job {job_name}'))

            # Check steps level
            for step in job.steps:
                logging.debug(f"Checking step level: {step.env}")
                findings.extend(self._check_urls(step.env, f'step in job {job_name}'))
                if step.run:
                    logging.debug(f"Checking run command: {step.run}")
                    findings.extend(self._check_run(step.run, f'step in job {job_name}'))

        return findings

    def _check_urls(self, env, level):
        findings = []
        for key, value in env.items():
            value_str = str(value)
            if self.pattern.search(value_str):
                findings.append(f"Unsecure protocol found in {level} env '{key}': {value_str}. "
                                f"Try use HTTPS instead of HTTP. If you need to use HTTP, "
                                f"please provide certain level of security.")
        return findings

    def _check_run(self, run, level):
        findings = []
        run_str = str(run)
        if self.pattern.search(run_str):
            findings.append(f"Unsecure protocol found in {level} run command '{run_str}'. "
                            f"Try use HTTPS instead of HTTP. If you need to use HTTP, "
                            f"please provide certain level of security.")
        return findings
