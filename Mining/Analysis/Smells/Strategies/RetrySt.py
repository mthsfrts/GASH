from abc import ABC, abstractmethod
from Mining.Analysis.Utils.Utilities import Utility


class RetryCheckStrategy(ABC):
    @abstractmethod
    def check(self, content, raw_content, **kwargs):
        pass


class DefaultRetryCheckStrategy(RetryCheckStrategy):
    def __init__(self, max_retries=2):
        self.MAX_RETRIES = max_retries

    def check(self, content, raw_content, **kwargs):
        retries = []
        is_critical = Utility.is_critical_branch(content)

        if 'jobs' in content:
            for job_name, job_data in content['jobs'].items():
                # Check if the job itself has a retry
                if 'retry' in job_data and job_data['retry'] > self.MAX_RETRIES:
                    line_numbers = Utility.find_pattern(raw_content, f"retry:")
                    retries.append({
                        'scope': f'job: {job_name}',
                        'retry_value': job_data['retry'],
                        'line': line_numbers[0] if line_numbers else None,
                        'is_critical': is_critical
                    })

                # Check for retries within the job's steps
                if 'steps' in job_data:
                    for step_data in job_data['steps']:
                        if 'retry' in step_data and step_data['retry'] > self.MAX_RETRIES:
                            line_numbers = Utility.find_pattern(raw_content, f"retry:")
                            retries.append({
                                'scope': f'step name: {step_data["name"]}',
                                'retry_value': step_data['retry'],
                                'line': line_numbers[0] if line_numbers else None,
                                'is_critical': is_critical
                            })

        return retries
