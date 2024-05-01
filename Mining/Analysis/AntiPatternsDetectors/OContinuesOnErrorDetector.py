import yaml
from Mining.Analysis.Utils.Utilities import Utility


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

        self.continue_on_errors = []

    def is_critical_branch(self):
        """
        Check if the workflow is configured for critical branches like master or main.
        :return: Boolean indicating if it's a critical branch.
        """
        critical_branches = ["master", "main", "production"]
        try:
            push_branches = self.content.get("on", {}).get("push", {}).get("branches", [])
        except AttributeError:
            push_branches = []
        for branch in critical_branches:
            if branch in push_branches:
                return True
        return False

    def detect(self):
        """
        Detects the use of continue-on-error in the workflow.
        :return: A list of dictionaries containing jobs/steps that use continue-on-error.
        """

        # Check if it's a critical branch
        is_critical = self.is_critical_branch()

        if 'jobs' in self.content:
            for job_name, job_data in self.content['jobs'].items():
                # Check if the job itself has a continue-on-error
                if job_data.get('continue-on-error', False):
                    line_numbers = Utility.find_pattern(self.raw_content, f"continue-on-error:")
                    self.continue_on_errors.append({
                        'scope': f'job: {job_name}',
                        'line': line_numbers[0] if line_numbers else None,
                        'is_critical': is_critical
                    })

                # Check for continue-on-error within the job's steps
                if 'steps' in job_data:
                    for step_data in job_data['steps']:
                        if step_data.get('continue-on-error', False):
                            line_numbers = Utility.find_pattern(self.raw_content, f"continue-on-error:")
                            self.continue_on_errors.append({
                                'scope': f'step in job: {job_name}',
                                'line': line_numbers[0] if line_numbers else None,
                                'is_critical': is_critical
                            })

        return self.continue_on_errors
