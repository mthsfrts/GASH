from Analysis.Smells.Categories.Security.RemoteTriggers.RemoteTriggersSt import MainRemoteRunCheck


class RemoteRunFct:
    """
    Factory class for creating instances of the RemoteTriggers strategy.
    """
    def __init__(self, content=None):
        if not content:
            raise ValueError("No workflow provided.")
        self.content = content
        self.findings = []
        self.strategy = MainRemoteRunCheck()

    def detect(self):
        """
        Detects Remote Run Triggers in the workflow.
        """
        self.findings = self.strategy.check(self.content)

        return self.findings
