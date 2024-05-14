import yaml
from Mining.Analysis.Utils.Utilities import Utility


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

        self.retries = []
        self.MAX_RETRIES = max_retries

    def detect(self):
        """
        Detects the use of retries in the workflow.
        :return: A list of dictionaries containing jobs/steps that use retries.
        """

        if 'jobs' in self.content:
            for job_name, job_data in self.content['jobs'].items():
                # Check if the job itself has a retry
                if 'retry' in job_data and job_data['retry'] > self.MAX_RETRIES:
                    line_numbers = Utility.find_pattern(self.raw_content, f"retry:")
                    self.retries.append({
                        'scope': f'job: {job_name}',
                        'retry_value': job_data['retry'],
                        'line': line_numbers[0] if line_numbers else None
                    })

                # Check for retries within the job's steps
                if 'steps' in job_data:
                    for step_data in job_data['steps']:
                        if 'retry' in step_data and step_data['retry'] > self.MAX_RETRIES:
                            line_numbers = Utility.find_pattern(self.raw_content, f"retry:")
                            self.retries.append({
                                'scope': f'step name: {step_data["name"]}',
                                'retry_value': step_data['retry'],
                                'line': line_numbers[0] if line_numbers else None
                            })

        return self.retries
