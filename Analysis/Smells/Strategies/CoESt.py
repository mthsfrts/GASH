from abc import ABC, abstractmethod
from Analysis.Utils.Utilities import Utility


class ContinueOnErrorCheckStrategy(ABC):
    @abstractmethod
    def check(self, content, raw_content, **kwargs):
        pass


class DefaultContinueOnErrorCheckStrategy(ContinueOnErrorCheckStrategy):
    def __init__(self, max_retries=2):
        self.MAX_RETRIES = max_retries

    def check(self, content, raw_content, **kwargs):
        continue_on_errors = []
        is_critical = Utility.is_critical_branch(content)

        if 'jobs' in content:
            for job_name, job_data in content['jobs'].items():
                # Check if the job itself has a continue-on-error
                if job_data.get('continue-on-error', False):
                    line_numbers = Utility.find_pattern(raw_content, f"continue-on-error:")
                    continue_on_errors.append({
                        'scope': f'job: {job_name}',
                        'line': line_numbers[0] if line_numbers else None,
                        'is_critical': is_critical
                    })

                # Check for continue-on-error within the job's steps
                if 'steps' in job_data:
                    for step_data in job_data['steps']:
                        if step_data.get('continue-on-error', False):
                            line_numbers = Utility.find_pattern(raw_content, f"continue-on-error:")
                            continue_on_errors.append({
                                'scope': f'step in job: {job_name}',
                                'line': line_numbers[0] if line_numbers else None,
                                'is_critical': is_critical
                            })

        return continue_on_errors
