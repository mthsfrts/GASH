from abc import ABC, abstractmethod
import re


class CodeQualityCheckStrategy(ABC):
    @abstractmethod
    def check(self, script):
        pass


class DuplicatedCodeCheckStrategy(CodeQualityCheckStrategy):
    def check(self, script):
        issues = []
        prev_line = None
        for line in script.split('\n'):
            if line == prev_line:
                issues.append(line)
            prev_line = line
        return issues


class LongCodeBlockCheckStrategy(CodeQualityCheckStrategy):
    def check(self, script):
        issues = []
        lines = script.split('\n')
        if len(lines) > 20:
            issues.append(script)
        return issues


class DuplicatedStepsCheckStrategy(CodeQualityCheckStrategy):
    def check(self, workflow):
        issues = []
        step_signatures = set()
        for job in workflow.jobs:
            for step in job.steps:
                step_signature = (step.name, step.command)
                if step_signature in step_signatures:
                    issues.append(f"Duplicated step: {step.name} with command: {step.command}")
                step_signatures.add(step_signature)
        return issues
