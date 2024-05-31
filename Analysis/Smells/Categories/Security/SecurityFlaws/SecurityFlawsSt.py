import logging
from Analysis.Utils.Utilities import Lists


class MainSecurityFlawsCheck:
    """
    Strategy to check for security flaws in Actions scripts.

    Attributes:
        permissions : List of permissions

    Returns:
        findings: List of permissions found
    """

    def __init__(self):
        self.permissions = Lists.permissions

    def check(self, content=None):
        """
        Checking for security flaws.

        Attributes:
            content: Content of the file to check

        Returns:
            findings: List of findings
        """
        findings = []

        findings.extend(self._check_permissions(content.permissions, 'workflow'))

        # Check jobs level
        for job_name, job in content.jobs.items():
            findings.extend(self._check_permissions(job.permissions, f'job {job_name}'))

        return findings

    def _check_permissions(self, permissions, level):
        findings = []
        if permissions is not None:
            logging.debug(f"Checking {level} permissions: {permissions}")
            if any(permission in self.permissions for permission in permissions.values()):
                if level == 'workflow':
                    findings.append(f"Permissions found in {level}: {permissions}, a top level may harm your pipeline. "
                                    f"Make sure to grant the right level for GitHub Token permissions.")
                else:
                    findings.append(f"Permissions found in {level}: {permissions}. "
                                    f"Make sure to grant the right level for GitHub Token permissions.")
        return findings
