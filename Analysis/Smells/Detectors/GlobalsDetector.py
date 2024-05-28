import yaml
from Analysis.Smells.Strategies.GlobalsSt import (
    DetectGlobalVariablesStrategy,
    ExcessiveUseStrategy,
    GenericNamesStrategy,
    SensitiveValuesStrategy,
    VariableRedefinitionStrategy,
    ComplexLogicStrategy
)


class GlobalVariableDetector:
    def __init__(self, content, max_global_vars=10):
        if isinstance(content, str):
            self.raw_content = content
            self.content = yaml.safe_load(content)
        elif isinstance(content, dict):
            self.content = content
            self.raw_content = yaml.dump(content)
        else:
            raise TypeError("Content must be a string or dictionary.")

        self.global_vars = []
        self.check_strategies = {
            "detect_globals": DetectGlobalVariablesStrategy(),
            "excessive_use": ExcessiveUseStrategy(max_global_vars),
            "generic_names": GenericNamesStrategy(),
            "sensitive_values": SensitiveValuesStrategy(),
            "variable_redefinition": VariableRedefinitionStrategy(),
            "complex_logic": ComplexLogicStrategy()
        }

    def detect(self):
        """
        Main function to detect global variables and related patterns.
        Returns True if any sub-method finds issues of concern.
        """
        has_issues = False
        results = {}

        # Run detection for global variables
        self.global_vars = self.check_strategies["detect_globals"].check(self.content, self.raw_content)

        # Examine excessive use of global variables
        excessive_use_flag, total_vars = self.check_strategies["excessive_use"].check(self.content, self.raw_content,
                                                                                      global_vars=self.global_vars)
        if total_vars > 0:
            has_issues = excessive_use_flag
        results["excessive_use"] = excessive_use_flag

        # Check for generic names
        generic_names = self.check_strategies["generic_names"].check(self.content, self.raw_content,
                                                                     global_vars=self.global_vars)
        if generic_names:
            has_issues = True
        results["generic_names"] = generic_names

        # Check for sensitive values
        sensitive_values = self.check_strategies["sensitive_values"].check(self.content, self.raw_content,
                                                                           global_vars=self.global_vars)
        if sensitive_values:
            has_issues = True
        results["sensitive_values"] = sensitive_values

        # Check for variable redefinition
        redefined_vars = self.check_strategies["variable_redefinition"].check(self.content, self.raw_content,
                                                                              global_vars=self.global_vars)
        if redefined_vars:
            has_issues = True
        results["variable_redefinition"] = redefined_vars

        # Check for complex logic based on variables
        complex_logic_vars = self.check_strategies["complex_logic"].check(self.content, self.raw_content,
                                                                          global_vars=self.global_vars)
        if complex_logic_vars:
            has_issues = True
        results["complex_logic"] = complex_logic_vars

        return has_issues, results
