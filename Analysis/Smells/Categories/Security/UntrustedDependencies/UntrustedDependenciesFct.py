from Analysis.Smells.Categories.Security.UntrustedDependencies.UntrustedDependenciesSt import \
    MainUntrustedDependenciesCheck


class UntrustedDependenciesFct:
    def __init__(self, content=None):
        if not content:
            raise ValueError("No workflow provided.")
        self.content = content
        self.findings = []
        self.strategy = MainUntrustedDependenciesCheck()

    def detect(self):
        """
        Detects untrusted dependencies in the workflow.
        """
        self.findings = self.strategy.check(self.content)
        return self.findings
