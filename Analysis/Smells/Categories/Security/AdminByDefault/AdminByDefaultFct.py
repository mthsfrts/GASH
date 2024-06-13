from Analysis.Smells.Categories.Security.AdminByDefault.AdminByDefaultSt import MainAdminByDefaultCheck


class AdminByDefaultFct:
    def __init__(self, content=None):
        if not content:
            raise ValueError("No workflow provided.")
        self.content = content
        self.findings = []
        self.strategy = MainAdminByDefaultCheck()

    def detect(self):
        """
        Detects elevate permissions on the workflow.
        """

        self.findings = self.strategy.check(self.content)
        return self.findings
