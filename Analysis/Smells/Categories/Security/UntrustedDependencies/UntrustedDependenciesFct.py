from Analysis.Smells.Categories.Security.UntrustedDependencies.UntrustedDependenciesSt import (
    MainUntrustedDependenciesCheck)


class UntrustedDependenciesFct:
    def __init__(self, content=None, token=None):
        if not content:
            raise ValueError("No workflow provided.")
        self.content = content
        if not token:
            raise ValueError("No token provided")
        self.token = token
        self.findings = []
        self.strategy = MainUntrustedDependenciesCheck(self.token)

    def detect(self):
        """
        Detects untrusted dependencies in the workflow.
        """
        self.findings = self.strategy.check(self.content)
        return self.findings
