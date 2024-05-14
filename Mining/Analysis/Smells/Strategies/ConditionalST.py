from abc import ABC, abstractmethod
import re
from Mining.Analysis.DataStruct.AntiPattern import GENERIC_NAMES, KEYWORDS


class ConditionCheckStrategy(ABC):
    @abstractmethod
    def check(self, condition):
        pass


class AlwaysTrueConditionCheckStrategy(ConditionCheckStrategy):
    def check(self, condition):
        if 'true' in condition:
            return True
        return False


class AlwaysFalseConditionCheckStrategy(ConditionCheckStrategy):
    def check(self, condition):
        if 'false' in condition:
            return True
        return False


class ComplexConditionCheckStrategy(ConditionCheckStrategy):
    def check(self, script):
        issues = []
        conditions = script.split('\n')

        for i, condition in enumerate(conditions):

            if '&&' in condition or '||' in condition:
                issues.append(f"Complex logical operation in condition: {condition}")

            if 'if' in condition and i > 0:
                prev_condition = conditions[i - 1]
                if 'if' in prev_condition:
                    issues.append(f"Nested conditions found: {prev_condition} -> {condition}")

        return issues


class UnnecessaryConditionCheckStrategy(ConditionCheckStrategy):
    def check(self, script):
        issues = []
        conditions = script.split('\n')

        for condition in conditions:
            if 'true == true' in condition or 'false == false' in condition:
                issues.append(condition)

        return issues


class InvalidReferenceCheckStrategy(ConditionCheckStrategy):
    def __init__(self, valid_variables):
        self.valid_variables = valid_variables

    def check(self, script):
        issues = []
        conditions = script.split('\n')

        for condition in conditions:
            variables = re.findall(r'\${{\s*([^}\s]+)\s*}}', condition)
            for variable in variables:
                if variable not in self.valid_variables:
                    issues.append(f"Invalid variable reference: {variable} in condition: {condition}")
                if any(re.fullmatch(pattern, variable) for pattern in GENERIC_NAMES):
                    issues.append(f"Generic variable name: {variable} in condition: {condition}")
                if any(re.fullmatch(pattern, variable) for pattern in KEYWORDS):
                    issues.append(f"Sensitive keyword in variable name: {variable} in condition: {condition}")

        return issues
