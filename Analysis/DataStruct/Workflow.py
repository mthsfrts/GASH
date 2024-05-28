class Workflow:
    """
    A class to represent a GitHub Actions workflow.

    Attributes:
        name (str): The name of the workflow.
        on (dict): The events that will trigger the workflow.
        jobs (dict): The jobs that will be executed in the workflow.
        env (dict): The environment variables that will be used in the workflow.
        concurrency (dict): The concurrency settings of the workflow.
        permissions (dict): The permissions of the workflow.
        defaults (dict): The default settings for the workflow.
    """

    def __init__(self):
        self.name = None
        self.on = {}
        self.jobs = {}
        self.env = {}
        self.concurrency = None
        self.permissions = {}
        self.defaults = {}

    def __str__(self):
        return (f"Workflow :"
                f"Name = {self.name},\n"
                f"On = {self.on},\n"
                f"Jobs = {self.jobs},\n"
                f"Env = {self.env},\n"
                f"Concurrency = {self.concurrency},\n"
                f"Permissions = {self.permissions},\n"
                f"Defaults = {self.defaults}")
