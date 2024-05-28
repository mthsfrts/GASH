import yaml
from Analysis.Smells.Strategies.CoESt import DefaultContinueOnErrorCheckStrategy


class ContinueOnErrorDetector:
    def __init__(self, content):
        if isinstance(content, str):
            self.raw_content = content
            self.content = yaml.safe_load(content)
        elif isinstance(content, dict):
            self.content = content
            self.raw_content = yaml.dump(content)
        else:
            raise TypeError("Content must be a string or dictionary.")

        self.check_strategy = DefaultContinueOnErrorCheckStrategy()
        self.continue_on_errors = []

    def detect(self):
        """
        Detects the use of continue-on-error in the workflow.
        :return: A list of dictionaries containing jobs/steps that use continue-on-error.
        """
        self.continue_on_errors = self.check_strategy.check(self.content, self.raw_content)
        return self.continue_on_errors
