import re
from Mining.Analysis.DataStruct import AntiPattern
from Mining.Analysis.Smells.Strategies.CodeQualitiesSt import DuplicatedCodeCheckStrategy, LongCodeBlockCheckStrategy, \
    GlobalsCheckStrategy
from Mining.Analysis.Utils.Utilities import Utility


class CodeQualityDetector:
    def __init__(self, workflow):
        self.workflow = workflow
        self.severity = AntiPattern.SEVERITIES
        self.strategies = {
            "CodeDuplicity": DuplicatedCodeCheckStrategy(),
            "LongCodeBlock": LongCodeBlockCheckStrategy(),
            "Globals": GlobalsCheckStrategy()
        }

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

    def check_code_quality(self, script):
        code_quality_issues = {issue_type: strategy.check(script) for issue_type, strategy in self.strategies.items()}
        return code_quality_issues
