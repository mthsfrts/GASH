from abc import ABC, abstractmethod
from Mining.Analysis.Utils.Utilities import Utility
from Mining.Analysis.DataStruct.Smells import GENERIC_NAMES, KEYWORDS


class GlobalVariableCheckStrategy(ABC):
    @abstractmethod
    def check(self, content, raw_content, **kwargs):
        pass


class DetectGlobalVariablesStrategy(GlobalVariableCheckStrategy):
    def check(self, content, raw_content, **kwargs):
        global_vars = []

        if 'env' in content:
            env = content['env']
            if isinstance(env, dict):
                for var_name, var_value in env.items():
                    line_numbers = Utility.find_pattern(raw_content, f"^{var_name}:")
                    global_vars.append({
                        'variable_name': var_name,
                        'variable_value': var_value,
                        'scope': 'workflow',
                        'line': line_numbers[0] if line_numbers else None
                    })

        if 'jobs' in content:
            for job_name, job_data in content['jobs'].items():
                if 'env' in job_data:
                    env = job_data['env']
                    if isinstance(env, dict):
                        for var_name, var_value in env.items():
                            line_numbers = Utility.find_pattern(raw_content, f"^{var_name}:")
                            global_vars.append({
                                'variable_name': var_name,
                                'variable_value': var_value,
                                'scope': f'job: {job_name}',
                                'line': line_numbers[0] if line_numbers else None
                            })
                if 'steps' in job_data:
                    for step_data in job_data['steps']:
                        if 'env' in step_data:
                            env = step_data['env']
                            if isinstance(env, dict):
                                for var_name, var_value in env.items():
                                    line_numbers = Utility.find_pattern(raw_content, f"^{var_name}:")
                                    global_vars.append({
                                        'variable_name': var_name,
                                        'variable_value': var_value,
                                        'scope': f'step in job: {job_name}',
                                        'line': line_numbers[0] if line_numbers else None
                                    })

        return global_vars


class ExcessiveUseStrategy(GlobalVariableCheckStrategy):
    def __init__(self, max_global_vars=10):
        self.MAX_GLOBAL_VARS = max_global_vars

    def check(self, content, raw_content, **kwargs):
        global_vars = kwargs.get('global_vars', [])
        total_vars = len(global_vars)
        return total_vars > self.MAX_GLOBAL_VARS, total_vars


class GenericNamesStrategy(GlobalVariableCheckStrategy):
    def check(self, content, raw_content, **kwargs):
        global_vars = kwargs.get('global_vars', [])
        generic_named_vars = [var for var in global_vars if var['variable_name'] in GENERIC_NAMES]
        return generic_named_vars


class SensitiveValuesStrategy(GlobalVariableCheckStrategy):
    def __init__(self):
        self.sensitive_keywords = KEYWORDS

    def check(self, content, raw_content, **kwargs):
        global_vars = kwargs.get('global_vars', [])
        sensitive_vars = []
        for var in global_vars:
            for keyword in self.sensitive_keywords:
                if isinstance(var['variable_value'], str) and keyword in var['variable_value'].lower():
                    sensitive_vars.append(var)
                    break
        return sensitive_vars


class VariableRedefinitionStrategy(GlobalVariableCheckStrategy):
    def check(self, content, raw_content, **kwargs):
        redefined_vars = []

        global_env_vars = content.get('env', {})

        jobs = content.get('jobs', {})
        for job_name, job_data in jobs.items():
            job_env_vars = job_data.get('env', {})
            for var_name, var_value in job_env_vars.items():
                if var_name in global_env_vars:
                    line_numbers = Utility.find_pattern(raw_content, f"^{var_name}:")
                    redefined_vars.append({
                        'variable_name': var_name,
                        'original_value': global_env_vars[var_name],
                        'redefined_value': var_value,
                        'scope': f'job: {job_name}',
                        'line': line_numbers[0] if line_numbers else None
                    })

            steps = job_data.get('steps', [])
            for step_data in steps:
                step_env_vars = step_data.get('env', {})
                for var_name, var_value in step_env_vars.items():
                    if var_name in global_env_vars or var_name in job_env_vars:
                        line_numbers = Utility.find_pattern(raw_content, f"^{var_name}:")
                        redefined_vars.append({
                            'variable_name': var_name,
                            'original_value': global_env_vars.get(var_name, job_env_vars.get(var_name)),
                            'redefined_value': var_value,
                            'scope': f'step in job: {job_name}',
                            'line': line_numbers[0] if line_numbers else None
                        })

        return redefined_vars


class ComplexLogicStrategy(GlobalVariableCheckStrategy):
    def check(self, content, raw_content, **kwargs):
        global_vars = kwargs.get('global_vars', [])
        complex_logic_vars = []

        added_vars_set = set()
        jobs = content.get('jobs', {})
        for job_name, job_data in jobs.items():
            job_condition = job_data.get('if')
            if job_condition:
                for var in global_vars:
                    if var['variable_name'] in job_condition and var['variable_name'] not in added_vars_set:
                        complex_logic_vars.append({
                            'variable_name': var['variable_name'],
                            'scope': f'job condition: {job_name}',
                            'line': var['line']
                        })
                        added_vars_set.add(var['variable_name'])

            steps = job_data.get('steps', [])
            for step_data in steps:
                step_condition = step_data.get('if')
                if step_condition:
                    for var in global_vars:
                        if var['variable_name'] in step_condition and var['variable_name'] not in added_vars_set:
                            complex_logic_vars.append({
                                'variable_name': var['variable_name'],
                                'scope': f'step condition in job: {job_name}',
                                'line': var['line']
                            })
                            added_vars_set.add(var['variable_name'])

        return complex_logic_vars
