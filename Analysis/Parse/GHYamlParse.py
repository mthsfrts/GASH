import yaml
from Analysis.DataStruct import Jobs, Steps, Workflow


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
        Extracts YAML content from a script if not already provided.
        :return: YAML content
        """
        if self.content is None and self.file_path:
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    self.content = file.read()
            except IOError as e:
                print(f"Error reading file: {str(e)}")
                self.content = None
        return self.content

    def parse_yaml(self):
        """
        Parses YAML content and returns a raw data dictionary.
        """
        if self.content is None:
            self.extract_content()

        try:
            return yaml.load(self.content, Loader=yaml.SafeLoader) if self.content else None
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {str(e)}")
            return None

    @staticmethod
    def process_triggers(workflow, on_data):
        """
        Processes the 'on' section of the YAML to extract triggers, branches, and tags.
        """
        if isinstance(on_data, dict):
            for event, event_details in on_data.items():
                workflow.triggers.append(event)
                if isinstance(event_details, dict):
                    workflow.branches.extend(event_details.get('branches', []))
                    workflow.tags.extend(event_details.get('tags', []))
        elif isinstance(on_data, list):
            workflow.triggers.extend(on_data)

    def populate_workflow(self, raw_data):
        """
        Populate and return a Workflow object based on raw data.
        """
        workflow = Workflow.Workflow()
        workflow.name = raw_data.get('name', 'Default Workflow Name')
        workflow.environment_vars = self.parse_env_vars(raw_data.get('env', {}))
        workflow.concurrency = raw_data.get('concurrency', None)
        workflow.raw_content = yaml.dump(raw_data)  # Save the raw YAML for reference

        # Process 'on' events and extract triggers, branches, and tags
        on_data = raw_data.get('on', {})
        YAMLParser.process_triggers(workflow, on_data)

        workflow.jobs = [self.create_job(job_name, job_data) for job_name, job_data in raw_data.get('jobs', {}).items()]
        return workflow

    def create_job(self, job_name, job_data):
        """
        Creates and returns a Job object.
        """
        job = Jobs.Job()
        job.name = job_name
        job.runs_on = job_data.get('runs-on', 'ubuntu-latest')  # Default to 'ubuntu-latest' if not specified
        job.environment_vars = self.parse_env_vars(job_data.get('env', {}))
        job.condition = job_data.get('if', None)
        job.steps = [self.create_step(step_data) for step_data in job_data.get('steps', [])]
        return job

    def create_step(self, step_data):
        """
        Creates and returns a Step object.
        """
        step = Steps.Step()
        step.name = step_data.get('name', 'Unnamed Step')
        step.uses = step_data.get('uses', None)
        step.run = step_data.get('run', None)
        step.with_args = step_data.get('with', {})
        step.env = self.parse_env_vars(step_data.get('env', {}))
        step.condition = step_data.get('if', None)
        return step

    def prepare_for_analysis(self):
        """
        Converts YAML content to a Workflow object.
        """
        raw_data = self.parse_yaml()
        if not raw_data:
            return None

        return self.populate_workflow(raw_data)

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