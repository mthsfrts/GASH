from Mining.Analysis.Utils.Utilities import Utility
from Mining.Analysis.DataStruct.AntiPattern import GENERIC_NAMES, KEYWORDS
import yaml


class GlobalVariableDetector:
    """
    Class to detect global variables in a workflow.\n
    Parameters that will be pass to the class:\n
    - content: (str or dict) Content of the workflow scripts.\n
    - keyword: (list) List of keywords that might indicate sensitive information.\n
    - max_global_vars: number of global variables allowed in the workflow.
    """

    def __init__(self, content, max_global_vars=10):

        if isinstance(content, str):
            self.raw_content = content
            self.content = yaml.safe_load(content)
        elif isinstance(content, dict):
            self.content = content
            self.raw_content = yaml.dump(content)
        else:
            raise TypeError("Content must be a string or dictionary.")

        self.sensitive_keywords = KEYWORDS
        self.global_vars = []
        self.sensitive_vars = []
        self.redefined_vars = []
        self.complex_logic_vars = []
        self.MAX_GLOBAL_VARS = max_global_vars

    def detect_global_variables(self):
        """
        Detects global variables in the workflow.
        :return: A list of global variables in the workflow.
        """

        # Detecting global variables at workflow level
        if 'env' in self.content:
            env = self.content['env']
            if isinstance(env, dict):
                for var_name, var_value in env.items():
                    line_numbers = Utility.find_pattern(self.raw_content, f"^{var_name}:")
                    self.global_vars.append({
                        'variable_name': var_name,
                        'variable_value': var_value,
                        'scope': 'workflow',
                        'line': line_numbers[0] if line_numbers else None
                    })
            elif isinstance(env, list):
                # Handle list if necessary or log an error
                print("Unsupported type for environment variable in list: Expected dict, got list.")

        # Detecting global variables at job level
        if 'jobs' in self.content:
            for job_name, job_data in self.content['jobs'].items():
                if 'env' in job_data:
                    env = job_data['env']
                    if isinstance(env, dict):
                        for var_name, var_value in env.items():
                            line_numbers = Utility.find_pattern(self.raw_content, f"^{var_name}:")
                            self.global_vars.append({
                                'variable_name': var_name,
                                'variable_value': var_value,
                                'scope': f'job: {job_name}',
                                'line': line_numbers[0] if line_numbers else None
                            })
                    elif isinstance(env, list):
                        print("Unsupported type for environment variable in list at job level.")

                # Detecting global variables at step level
                if 'steps' in job_data:
                    for step_data in job_data['steps']:
                        if 'env' in step_data:
                            env = step_data['env']
                            if isinstance(env, dict):
                                for var_name, var_value in env.items():
                                    line_numbers = Utility.find_pattern(self.raw_content, f"^{var_name}:")
                                    self.global_vars.append({
                                        'variable_name': var_name,
                                        'variable_value': var_value,
                                        'scope': f'step in job: {job_name}',
                                        'line': line_numbers[0] if line_numbers else None
                                    })
                            elif isinstance(env, list):
                                print("Unsupported type for environment variable in list at step level.")

        return self.global_vars

    def excessive_use(self):
        """
        Detects excessive use of global variables.
        :return: Tuple of (boolean, total number of global variables)
        """

        # Verify excessive use of global variables
        total_vars = len(self.global_vars)
        return total_vars > self.MAX_GLOBAL_VARS, total_vars

    def generic_names(self):
        """
        Detects generic names for global variables.
        :return: A list of global variables with generic names.
        """
        # Verify if generic names are used for global variables
        generic_named_vars = [var for var in self.global_vars if var in GENERIC_NAMES]
        return generic_named_vars

    def sensitive_values(self):
        """
        Detects global variables that might contain sensitive information.
        :return: A list of global variables that might contain sensitive information.
        """
        # Keywords that might indicate sensitive information
        for var in self.global_vars:
            for keyword in self.sensitive_keywords:
                if isinstance(var['variable_value'], str) and keyword in var['variable_value'].lower():
                    self.sensitive_vars.append({
                        'variable_name': var['variable_name'],
                        'variable_value': var['variable_value'],
                        'line': var['line']
                    })
                    break  # Break out of the inner loop once a sensitive keyword is found

        return self.sensitive_vars

    def variable_redefinition(self):
        """
        Detects redefinition of environment variables in jobs or steps.
        :return: A list of redefined variables.
        """
        # Get global environment variables
        global_env_vars = self.content.get('env', {})

        # Check jobs for redefinitions
        jobs = self.content.get('jobs', {})
        for job_name, job_data in jobs.items():
            job_env_vars = job_data.get('env', {})
            for var_name, var_value in job_env_vars.items():
                if var_name in global_env_vars:
                    line_numbers = Utility.find_pattern(self.raw_content, f"^{var_name}:")
                    self.redefined_vars.append({
                        'variable_name': var_name,
                        'original_value': global_env_vars[var_name],
                        'redefined_value': var_value,
                        'scope': f'job: {job_name}',
                        'line': line_numbers[0] if line_numbers else None
                    })

            # Check steps within the job for redefinitions
            steps = job_data.get('steps', [])
            for step_data in steps:
                step_env_vars = step_data.get('env', {})
                for var_name, var_value in step_env_vars.items():
                    if var_name in global_env_vars or var_name in job_env_vars:
                        line_numbers = Utility.find_pattern(self.raw_content, f"^{var_name}:")
                        self.redefined_vars.append({
                            'variable_name': var_name,
                            'original_value': global_env_vars.get(var_name, job_env_vars.get(var_name)),
                            'redefined_value': var_value,
                            'scope': f'step in job: {job_name}',
                            'line': line_numbers[0] if line_numbers else None
                        })

        return self.redefined_vars

    def complex_logic_based_on_variables(self):
        """
        Detects complex logic based on global variables.
        :return: A list of global variables that are used in complex logic.
        """

        # Set to track added variables
        added_vars_set = set()

        # Verify conditions in the workflow
        jobs = self.content.get('jobs', {})
        for job_name, job_data in jobs.items():

            # Verify conditions in the workflow
            job_condition = job_data.get('if')
            if job_condition:
                for var in self.global_vars:
                    if var['variable_name'] in job_condition and var['variable_name'] not in added_vars_set:
                        self.complex_logic_vars.append({
                            'variable_name': var['variable_name'],
                            'scope': f'job condition: {job_name}',
                            'line': var['line']
                        })
                        added_vars_set.add(var['variable_name'])

            # Verify conditions in the steps
            steps = job_data.get('steps', [])
            for step_data in steps:
                step_condition = step_data.get('if')
                if step_condition:
                    for var in self.global_vars:
                        if var['variable_name'] in step_condition and var['variable_name'] not in added_vars_set:
                            self.complex_logic_vars.append({
                                'variable_name': var['variable_name'],
                                'scope': f'step condition in job: {job_name}',
                                'line': var['line']
                            })
                            added_vars_set.add(var['variable_name'])

        return self.complex_logic_vars

    def detect(self):
        """
        Main function to detect global variables and related patterns.
        Returns True if any sub-method finds issues of concern.
        """
        has_issues = False  # Flag to indicate if there are issues

        # Run detection for global variables and store results
        # global_vars = self.detect_global_variables()

        # Examine excessive use of global variables
        excessive_use_flag, total_vars = self.excessive_use()
        if total_vars > 0:  # Check if there are any global variables at all
            has_issues = excessive_use_flag  # Update flag based on excessive use

        # Check for generic names, sensitive values, redefinitions, and complex logic
        if len(self.generic_names()) > 0:
            has_issues = True
        if len(self.sensitive_values()) > 0:
            has_issues = True
        if len(self.variable_redefinition()) > 0:
            has_issues = True
        if len(self.complex_logic_based_on_variables()) > 0:
            has_issues = True

        results = {
            # 'global_variables': global_vars,
            'excessive_use': excessive_use_flag,
            'generic_names': self.generic_names(),
            'sensitive_values': self.sensitive_values(),
            'variable_redefinition': self.variable_redefinition(),
            'complex_logic': self.complex_logic_based_on_variables()
        }

        return has_issues, results
