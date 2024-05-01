import re
from Mining.Analysis.DataStruct import AntiPattern
from Mining.Analysis.Utils.Utilities import Utility


class CodeQualityDetector:

    def __init__(self, workflow):
        self.workflow = workflow
        self.severity = AntiPattern.SEVERITIES

    def detect(self):
        anti_patterns = []

        for job in self.workflow.jobs:
            for step in job.steps:
                if step.command is None:
                    continue

                code_quality_issues = self.check_code_quality(step.command)

                for issue_type, issues in code_quality_issues.items():
                    for issue in issues:
                        line_numbers = Utility.find_pattern(self.workflow.raw_content, re.escape(issue))
                        anti_pattern = AntiPattern.AntiPattern()
                        anti_pattern.type = issue_type
                        anti_pattern.description = issue
                        anti_pattern.location = f"{job.name}:{line_numbers[0] if line_numbers else 'Unknown'}"
                        anti_pattern.additional_info = {
                            "justification": self.severity[issue_type]["justification"]
                        }
                        anti_patterns.append(anti_pattern)

        return anti_patterns

    @staticmethod
    def check_code_quality(script):
        code_quality_issues = {
            "CodeDuplicity": [],
            "LongCodeBlock": [],
            "Globals": []
        }

        # Check for duplicated code
        prev_line = None
        for line in script.split('\n'):
            if line == prev_line:
                code_quality_issues["CodeDuplicity"].append(line)
            prev_line = line

        # Check for large code blocks
        lines = script.split('\n')
        if len(lines) > 10:
            code_quality_issues["LongCodeBlock"].append(script)

        # Check for global variables
        for line in lines:
            if line.startswith("global "):
                variable_name = line.split(" ")[1]
                code_quality_issues["Globals"].append(variable_name)

        return code_quality_issues
