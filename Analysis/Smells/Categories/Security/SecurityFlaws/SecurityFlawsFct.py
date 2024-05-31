from Analysis.Smells.Categories.Security.SecurityFlaws.SecurityFlawsSt import MainSecurityFlawsCheck


class SecurityFlawsFct:
    def __init__(self, content=None):
        if not content:
            raise ValueError("No workflow provided.")
        self.content = content
        self.findings = []
        self.strategy = MainSecurityFlawsCheck()

    def detect(self):
        """
        Detects security flaws in the Action.
        """
        self.findings = self.strategy.check(self.content)
        return self.findings
