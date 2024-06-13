from Analysis.Smells.Categories.Quality.LongBlocks.LongBlockSt import MainLongBlockCheck
from Analysis.Parse.ActionParser import Action


class LongBlockFct:
    """
    Factory to detect long blocks in a workflow.
    """

    def __init__(self, content=None):
        if not content:
            raise ValueError("No workflow provided.")
        self.content = content
        self.findings = []
        self.strategy = MainLongBlockCheck()

    def detect(self):
        """
        Detect long blocks in the workflow.
        """

        self.findings = self.strategy.check(self.content)
        return self.findings