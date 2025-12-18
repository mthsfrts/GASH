import logging


class MainAdminByDefaultCheck:
    """
    Strategy to check for elevated permissions in the GitHub Actions workflow.

    Attributes:
        permissions: List of elevated permissions.
    """

    def __init__(self):
        self.permissions = ["write", "write-all"]
        # No shared findings state here; methods return local lists

    def check(self, content=None):
        """
        Method to check elevated permissions in the GitHub Actions workflow.

        Attributes:
            content: Workflow content.

        Return:
            findings: List of found elevated permissions.
        """

        findings = []

        if content is None:
            return findings

        # Verify permissions at the workflow level
        workflow_perms = getattr(content, 'permissions', None)
        findings.extend(self._check_permissions(workflow_perms, 'workflow'))

        # Verify permissions at job level (safely)
        jobs = getattr(content, 'jobs', None)
        if isinstance(jobs, dict):
            for job_name, job in jobs.items():
                job_perms = getattr(job, 'permissions', None)
                findings.extend(self._check_permissions(job_perms, f'job {job_name}'))

        return findings

    def _check_permissions(self, permissions, level):
        findings = []
        if permissions is None:
            return findings

        logging.debug(f"Verifying permissions {level}: {permissions}")

        # dict mapping: check each permission value (normalize strings)
        if isinstance(permissions, dict):
            for perm_key, perm_value in permissions.items():
                val = perm_value
                if isinstance(perm_value, str):
                    val = perm_value.lower()
                if val in self.permissions:
                    findings.append(
                        f"Elevated permission found at {level}: {perm_key} = {perm_value}."
                        f" Review and apply least-privilege principle."
                    )

        # string shorthand like 'write' at this level
        elif isinstance(permissions, str):
            if permissions.lower() in self.permissions:
                findings.append(
                    f"Elevated permission '{permissions}' found at {level}."
                    f" Review and apply least-privilege principle."
                )

        return findings
