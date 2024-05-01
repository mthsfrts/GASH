from Mining.Analysis.DataStruct import AntiPattern
from Mining.Analysis.Utils.Utilities import Utility


class WorkFlowDispatchDetector:

    def __init__(self, workflow):
        self.workflow = workflow
        self.severity = AntiPattern.SEVERITIES
        if not hasattr(self.workflow, 'events') or not isinstance(self.workflow.events, dict):
            self.workflow.events = {}

    def detect(self):
        anti_patterns = []

        if 'workflow_dispatch' in self.workflow.raw_content:
            line_numbers = Utility.find_pattern(self.workflow.raw_content, r'workflow_dispatch:')
            anti_pattern = AntiPattern.AntiPattern()
            if self.workflow.events.get('workflow_dispatch') is None:
                anti_pattern.description = (f"Workflow `{self.workflow.name}` has a workflow_dispatch "
                                            "with no parameters which is not recommended.")
            else:
                anti_pattern.description = f"Workflow: {self.workflow.name}, can be triggered manually."
            anti_pattern.location = f"{line_numbers[0] if line_numbers else 'Unknown'}"
            anti_pattern.severity = self.severity["WorkflowDispatch"]["severity"]
            anti_pattern.additional_info = {
                "justification": self.severity["WorkflowDispatch"]["justification"]
            }
            anti_patterns.append(anti_pattern)

        return anti_patterns
