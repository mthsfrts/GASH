from abc import ABC, abstractmethod
import re
from Mining.Analysis.DataStruct.Smells import GENERIC_NAMES, KEYWORDS
from Mining.Analysis.Utils.LLMs import LLMAnalyzer


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
    def __init__(self, llm_analyzer):
        self.llm_analyzer = llm_analyzer

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

    def check_llms(self, script):
        issues = []
        conditions = script.split('\n')

        for condition in conditions:
            llm_issues = self.llm_analyzer.analyze_conditions(condition)
            issues.extend(llm_issues)

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
    def __init__(self, llm_analyzer):
        self.llm_analyzer = llm_analyzer

    def check(self, script):
        issues = []
        conditions = script.split('\n')

        for condition in conditions:
            variables = re.findall(r'\${{\s*([^}\s]+)\s*}}', condition)
            for variable in variables:
                if any(re.fullmatch(pattern, variable) for pattern in GENERIC_NAMES):
                    issues.append(f"Generic variable name: {variable} in condition: {condition}")
                if any(re.fullmatch(pattern, variable) for pattern in KEYWORDS):
                    issues.append(f"Sensitive keyword in variable name: {variable} in condition: {condition}")
                else:
                    continue
        return issues

    def check_llms(self, script):
        issues = []
        conditions = script.split('\n')

        for condition in conditions:
            llm_issues = self.llm_analyzer.analyze_conditions(condition)
            for issue in llm_issues:
                issue_score = self.llm_analyzer.extract_gpt2_score(issue['response'])
                issues.append({'issue': issue, 'score': issue_score})

        return issues
