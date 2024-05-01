from Mining.Analysis.DataStruct import AntiPattern
from Mining.Analysis.Utils.Utilities import Utility
import re


class ConditionsDetector:

    def __init__(self, workflow):
        self.workflow = workflow
        self.severity = AntiPattern.SEVERITIES

    def detect(self):
        anti_patterns = []

        for job in self.workflow.jobs:
            if job.condition:
                self._add_condition_anti_pattern(job.condition, job.name, anti_patterns)

            for step in job.steps:
                if step.condition:
                    self._add_condition_anti_pattern(step.condition, f"{job.name} step: {step.name}", anti_patterns)

        return anti_patterns

    def _add_condition_anti_pattern(self, condition, location_description, anti_patterns):
        line_numbers = Utility.find_pattern(self.workflow.raw_content, re.escape(condition))
        anti_pattern = AntiPattern.AntiPattern()
        anti_pattern.description = f"Condition found at '{location_description}': {condition}"
        anti_pattern.location = f"{line_numbers[0] if line_numbers else 'Unknown'}"
        anti_pattern.severity = self.severity["Conditionals"]["severity"]
        anti_pattern.additional_info = {
            "justification": self.severity["Conditionals"]["justification"]
        }
        anti_patterns.append(anti_pattern)
