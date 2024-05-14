from abc import ABC, abstractmethod


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


class GlobalsCheckStrategy(CodeQualityCheckStrategy):
    def check(self, script):
        issues = []
        for line in script.split('\n'):
            if line.startswith("global "):
                variable_name = line.split(" ")[1]
                issues.append(variable_name)
        return issues
