class Workflow:
    """
    A class to represent a GitHub Actions workflow.\n
    Parameter that will be used in the workflow structure:\n
    - name: The name of the workflow.\n
    - trigger_events: The events that will trigger the workflow.\n
    - jobs: The jobs that will be executed in the workflow.\n
    - environment_vars: The environment variables that will be used in the workflow.\n
    - concurrency: The concurrency that the workflow will be associated with.\n
    - branches: The branches that the workflow will be associated with.\n
    - tags: The tags that the workflow will be associated with.\n
    - raw_content: The raw content of the workflow.\n
    """
    def __init__(self):
        self.name = None
        self.events = {}
        self.triggers = []
        self.jobs = []
        self.environment_vars = []
        self.concurrency = []
        self.branches = []
        self.tags = []
        self.raw_content = None
