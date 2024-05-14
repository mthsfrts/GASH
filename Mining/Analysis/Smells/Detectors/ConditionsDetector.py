import re
from Mining.Analysis.DataStruct import AntiPattern
from Mining.Analysis.Utils.Utilities import Utility
from Mining.Analysis.Smells.Strategies.ConditionalST import AlwaysTrueConditionCheckStrategy, \
    AlwaysFalseConditionCheckStrategy, ComplexConditionCheckStrategy, UnnecessaryConditionCheckStrategy, \
    InvalidReferenceCheckStrategy


class ConditionsDetector:
    def __init__(self, workflow, valid_variables):
        self.workflow = workflow
        self.severity = AntiPattern.SEVERITIES
        self.strategies = {
            "AlwaysTrue": AlwaysTrueConditionCheckStrategy(),
            "AlwaysFalse": AlwaysFalseConditionCheckStrategy(),
            "ComplexCondition": ComplexConditionCheckStrategy(),
            "UnnecessaryCondition": UnnecessaryConditionCheckStrategy(),
            "InvalidReference": InvalidReferenceCheckStrategy(valid_variables)
        }

    def detect(self):
        anti_patterns = []

        for job in self.workflow.jobs:
            if job.condition:
                self._check_conditions(job.condition, job.name, anti_patterns)

            for step in job.steps:
                if step.condition:
                    self._check_conditions(step.condition, f"{job.name} step: {step.name}", anti_patterns)

        return anti_patterns

    def _check_conditions(self, condition, location_description, anti_patterns):
        for issue_type, strategy in self.strategies.items():
            issues = strategy.check(condition)
            for issue in issues:
                line_numbers = Utility.find_pattern(self.workflow.raw_content, re.escape(issue))
                anti_pattern = AntiPattern.AntiPattern()
                anti_pattern.type = issue_type
                anti_pattern.description = f"Condition found at '{location_description}': {issue}"
                anti_pattern.location = f"{line_numbers[0] if line_numbers else 'Unknown'}"
                anti_pattern.severity = self.severity["Conditionals"]["severity"]
                anti_pattern.additional_info = {
                    "justification": self.severity["Conditionals"]["justification"]
                }
                anti_patterns.append(anti_pattern)
