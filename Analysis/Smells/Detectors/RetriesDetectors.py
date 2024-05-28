import yaml
from Analysis.Smells.Strategies.RetrySt import DefaultRetryCheckStrategy


class RetryDetector:
    def __init__(self, content, max_retries=2):
        if isinstance(content, str):
            self.raw_content = content
            self.content = yaml.safe_load(content)
        elif isinstance(content, dict):
            self.content = content
            self.raw_content = yaml.dump(content)
        else:
            raise TypeError("Content must be a string or dictionary.")

        self.check_strategy = DefaultRetryCheckStrategy(max_retries)
        self.retries = []

    def detect(self):
        """
        Detects the use of retries in the workflow.
        :return: A list of dictionaries containing jobs/steps that use retries.
        """
        self.retries = self.check_strategy.check(self.content, self.raw_content)
        return self.retries
