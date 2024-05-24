import re
from Mining.Analysis.DataStruct.Smells import Smells, SEVERITIES
from Mining.Analysis.Utils.Utilities import Utility
from Mining.Analysis.Smells.Strategies.ConditionalST import (ComplexConditionCheckStrategy,
                                                             UnnecessaryConditionCheckStrategy,
                                                             InvalidReferenceCheckStrategy)


class ConditionsDetector:
    def __init__(self, workflow):
        self.workflow = workflow
        self.severity = SEVERITIES
        self.strategies = {
            "ComplexCondition": ComplexConditionCheckStrategy(),
            "UnnecessaryCondition": UnnecessaryConditionCheckStrategy(),
            "InvalidReference": InvalidReferenceCheckStrategy()
        }

    def detect(self):
        smells = []

        for job in self.workflow.jobs:
            if job.condition:
                self._check_conditions(job.condition, job.name, smells)

            for step in job.steps:
                if step.condition:
                    self._check_conditions(step.condition, f"{job.name} step: {step.name}", smells)

        return smells

    def _check_conditions(self, condition, location_description, smells):
        for issue_type, strategy in self.strategies.items():
            issues = strategy.check(condition)
            for issue in issues:
                line_numbers = Utility.find_pattern(self.workflow.raw_content, re.escape(issue))
                smell = Smells()
                smell.type = issue_type
                smell.description = f"Condition found at '{location_description}': {issue}"
                smell.location = f"{line_numbers[0] if line_numbers else 'Unknown'}"
                smell.severity = self.severity["Conditionals"]["severity"]
                smell.additional_info = {
                    "justification": self.severity["Conditionals"]["justification"]
                }
                smells.append(smell)
