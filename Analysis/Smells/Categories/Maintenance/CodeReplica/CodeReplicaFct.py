from Analysis.Smells.Categories.Maintenance.CodeReplica.CodeReplicaSt import MainCodeReplicaCheck


class CodeReplicaFct:
    """
    Factory classe to create Code Replica smell detection object.
    """

    def __init__(self, content=None):
        if not content:
            raise ValueError("No workflow provided.")
        self.content = content
        self.findings = []
        self.strategy = MainCodeReplicaCheck()

    def detect(self):
        """
        Detects code replicas on the workflow.
        """
        self.findings = self.strategy.check(self.content)
        return self.findings
