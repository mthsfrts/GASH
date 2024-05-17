from Mining.Analysis.Smells.Strategies.WkSt import DefaultWorkFlowDispatchCheckStrategy


class WorkFlowDispatchDetector:
    def __init__(self, workflow):
        if not workflow:
            raise ValueError("No workflow provided.")
        self.workflow = workflow
        self.check_strategy = DefaultWorkFlowDispatchCheckStrategy()
        self.anti_patterns = []

    def detect(self):
        self.anti_patterns = self.check_strategy.check(self.workflow)
        return self.anti_patterns
