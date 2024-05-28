import yaml
from Analysis.DataStruct import Jobs, Steps, Workflow


def no_boolean_constructor(loader, node):
    return loader.construct_scalar(node)


yaml.SafeLoader.add_constructor('tag:yaml.org,2002:bool', no_boolean_constructor)
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:omap', no_boolean_constructor)
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:pairs', no_boolean_constructor)
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:set', no_boolean_constructor)
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:timestamp', no_boolean_constructor)


class Action:
    """
    A class to parse YAML scripts.
    - file_path: (str) Path to the YAML scripts.
    - content: (str) YAML content.
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
                with open(self.file_path, 'r') as file:
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

    def prepare_for_analysis(self):
        """
        Converts YAML content to a Workflow object.
        """
        raw_data = self.parse_yaml()
        if not raw_data:
            return None

        return self.populate_workflow(raw_data)

    def populate_workflow(self, raw_data):
        """
        Populates and returns a Workflow object based on raw data.
        """
        workflow = Workflow.Workflow()
        workflow.name = raw_data.get('name', 'Default Workflow Name')
        workflow.env = raw_data.get('env', {})
        workflow.on = raw_data.get('on', {})
        workflow.jobs = {job_name: self.populate_job(job_name, job_data)
                         for job_name, job_data in raw_data.get('jobs', {}).items()}
        workflow.concurrency = raw_data.get('concurrency', None)
        workflow.permissions = raw_data.get('permissions', None)
        workflow.defaults = raw_data.get('defaults', {})

        return workflow

    def populate_job(self, job_name, job_data):
        """
        Populates and returns a Job object.
        """
        job = Jobs.Job()
        job.name = job_name
        job._id = job_data.get('id', None)
        job.runs_on = job_data.get('runs-on', None)
        job.steps = [self.populate_step(step_data) for step_data in job_data.get('steps', [])]
        job.env = job_data.get('env', {})
        job._if = job_data.get('if', None)
        job.concurrency = job_data.get('concurrency', None)
        job.container = job_data.get('container', None)
        job.continue_on_error = job_data.get('continue-on-error', None)
        job.defaults = job_data.get('defaults', {})
        job.outputs = job_data.get('outputs', {})
        job.permissions = job_data.get('permissions', None)
        job.services = job_data.get('services', {})
        job.strategy = job_data.get('strategy', {})
        job.secrets = job_data.get('secrets', {})
        job.timeout_minutes = job_data.get('timeout-minutes', None)
        job.needs = job_data.get('needs', [])
        job.uses = job_data.get('uses', None)
        job.with_params = job_data.get('with', {})

        return job

    @staticmethod
    def populate_step(step_data):
        """
        Populates and returns a Step object.
        """
        step = Steps.Step()
        step.name = step_data.get('name', None)
        step._id = step_data.get('id', None)
        step.uses = step_data.get('uses', None)
        step.run = step_data.get('run', None)
        step.working_directory = step_data.get('working-directory', None)
        step.env = step_data.get('env', {})
        step._if = step_data.get('if', None)
        step.continue_on_error = step_data.get('continue-on-error', None)
        step.timeout_minutes = step_data.get('timeout-minutes', None)
        step.uses = step_data.get('uses', None)
        step.with_params = step_data.get('with', {})
        return step
