import yaml
from Mining.Analysis.DataStruct import Steps, Workflow, Jobs


def no_boolean_constructor(loader, node):
    return loader.construct_scalar(node)


yaml.SafeLoader.add_constructor('tag:yaml.org,2002:bool', no_boolean_constructor)
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:omap', no_boolean_constructor)
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:pairs', no_boolean_constructor)
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:set', no_boolean_constructor)
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:timestamp', no_boolean_constructor)


class YAMLParser:
    """
    A class to parse YAML scripts.\n
    - file_path: (str) Path to the YAML scripts.\n
    - content: (str) YAML content.\n
    """

    def __init__(self, file_path=None, content=None):
        self.file_path = file_path
        self.content = content
        self.workflow = Workflow.Workflow()

    def extract_content(self):
        """
        Extracts YAML content from a scripts
        :return: YAML content
        """
        if self.file_path:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.content = file.read()
        return self.content

    def prepare_for_analysis(self):
        """
        Converts YAML content to parts of Workflow object
        :return: Populated Workflow object
        """
        self.extract_content()
        raw_data = yaml.load(self.content, Loader=yaml.SafeLoader)

        # Populating Workflow properties
        self.workflow.name = raw_data.get('name')
        self.workflow.environment_vars = self.parse_env_vars(raw_data.get('env'))
        self.workflow.raw_content = self.content
        self.workflow.concurrency = raw_data.get('concurrency')
        self.workflow.events = raw_data.get('on', {})

        # Extract 'on' events and branches/tags
        on_data = raw_data.get('on', {})
        if isinstance(on_data, dict):
            for event, event_details in on_data.items():
                self.workflow.triggers.append(event)

                if isinstance(event_details, dict) and 'branches' in event_details:
                    self.workflow.branches.extend(event_details['branches'])

                if isinstance(event_details, dict) and 'tags' in event_details:
                    self.workflow.tags.extend(event_details['tags'])

        elif isinstance(on_data, list):
            self.workflow.triggers.extend(on_data)

        # Populate Jobs within the Workflow
        for job_name, job_data in raw_data.get('jobs', {}).items():
            job = Jobs.Job()
            job.name = job_name
            job.machine_type = job_data.get('runs-on')
            job.environment_vars = self.parse_env_vars(job_data.get('env'))
            job.condition = job_data.get('if')

            # Populate Steps within the Job
            for step_data in job_data.get('steps', []):
                step = Steps.Step()
                step.name = step_data.get('name')
                step.action = step_data.get('uses')
                step.command = step_data.get('run')
                step.arguments = step_data.get('with', {})
                step.environment_vars = self.parse_env_vars(step_data.get('env'))
                step.condition = step_data.get('if')
                job.steps.append(step)

            self.workflow.jobs.append(job)

        return self.workflow

    @staticmethod
    def parse_env_vars(env):
        # Check if env is None
        if env is None:
            return []

        # If env is a dictionary, process normally
        if isinstance(env, dict):
            try:
                return [{'key': k, 'value': v} for k, v in env.items()]
            except AttributeError as e:
                print(f"Error processing environment variables from dict: {str(e)}")
                return []

        # If env is a list, handle each element
        elif isinstance(env, list):
            result = []
            for item in env:
                if isinstance(item, tuple) and len(item) == 2:
                    result.append({'key': item[0], 'value': item[1]})
                elif isinstance(item, dict):
                    # This handles list of single-entry dictionaries
                    for k, v in item.items():
                        result.append({'key': k, 'value': v})
                else:
                    print(f"Unsupported type for environment variable in list: {type(item)}")
            return result

        else:
            print(f"Expected a dictionary or list for environment variables, got {type(env)} instead.")
            return []

