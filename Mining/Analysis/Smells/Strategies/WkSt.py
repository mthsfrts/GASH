from abc import ABC, abstractmethod
from Mining.Analysis.DataStruct import Smells
from Mining.Analysis.Utils.Utilities import Utility


class WorkFlowDispatchCheckStrategy(ABC):
    @abstractmethod
    def check(self, workflow):
        pass


class DefaultWorkFlowDispatchCheckStrategy(WorkFlowDispatchCheckStrategy):
    def __init__(self):
        self.severity = Smells.SEVERITIES

    def check(self, workflow):
        anti_patterns = []

        if 'workflow_dispatch' in workflow.raw_content:
            line_numbers = Utility.find_pattern(workflow.raw_content, r'workflow_dispatch:')
            anti_pattern = Smells.Smells()
            if workflow.events.get('workflow_dispatch') is None:
                anti_pattern.description = (f"Workflow `{workflow.name}` has a workflow_dispatch "
                                            "with no parameters which is not recommended.")
            else:
                anti_pattern.description = f"Workflow: {workflow.name}, can be triggered manually."
            anti_pattern.location = f"{line_numbers[0] if line_numbers else 'Unknown'}"
            anti_pattern.severity = self.severity["WorkflowDispatch"]["severity"]
            anti_pattern.additional_info = {
                "justification": self.severity["WorkflowDispatch"]["justification"]
            }
            anti_pattern.is_critical = Utility.is_critical_branch(workflow.events)
            anti_patterns.append(anti_pattern)

        return anti_patterns
