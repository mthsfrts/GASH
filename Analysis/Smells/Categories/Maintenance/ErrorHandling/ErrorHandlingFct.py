from Analysis.Smells.Categories.Maintenance.ErrorHandling.ErrorHandlingSt import MainErrorHandlingCheck


class ErrorHandlingFct:
    """
    Factory classe to create ErrorHandling smell detection object
    """

    def __init__(self, content=None):
        if not content:
            raise ValueError("No workflow provided.")
        self.content = content
        self.findings = []
        self.strategy = MainErrorHandlingCheck()

    def detect(self):
        """
        Detects ErrorHandling smell in the provided workflow
        """
        self.findings = self.strategy.check(self.content)
        return self.findings
