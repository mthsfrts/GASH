import logging


class MainAdminByDefaultCheck:
    """
    Strategy to check for elevated permissions in the GitHub Actions workflow.

    Attributes:
        permissions: List of elevated permissions.
    """

    def __init__(self):
        self.permissions = ["write", "write-all"]
        self.findings = []

    def check(self, content=None):
        """
        Method to check elevated permissions in the GitHub Actions workflow.

        Attributes:
            content: Workflow content.

        Return:
            findings: List of found elevated permissions.
        """

        # Verify permissions at the workflow level
        self.findings.extend(self._check_permissions(content.permissions, 'workflow'))

        # Verify permissions at job level
        for job_name, job in content.jobs.items():
            self.findings.extend(self._check_permissions(job.permissions, f'job {job_name}'))

        return self.findings

    def _check_permissions(self, permissions, level):
        self.findings = []
        if permissions is not None:
            logging.debug(f"Verifying permissions {level}: {permissions}")

            if isinstance(permissions, dict):
                for perm_key, perm_value in permissions.items():
                    if perm_value in self.permissions:
                        self.findings.append(f"Elevate permission found at {level}: {perm_key} = {perm_value}. "
                                             f"Review the permission and check if the user is qualified for that. "
                                             f"Use the least privilege principle.")

            if isinstance(permissions, str):
                if permissions in self.permissions:
                    self.findings.append(
                        "Workflow call trigger is set with a higher permission. "
                        "Consider the add best security protocol for it. "
                        "This trigger might harm your pipeline if it is not "
                        "configure correctly."
                    )

        return self.findings
