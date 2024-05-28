class Job:
    """
    A class to represent a job in a workflow.

    Attributes:
        name (str): The name of the job.
        _id (str): The ID of the job.
        runs_on (str): The type of machine to run the job on.
        steps (dict): The steps that the job will run.
        env (dict): The environment variables that the job will use.
        _if (str): The condition that the job will run.
        concurrency (dict): The concurrency setting for the job.
        container (dict): The container configuration for the job.
        continue_on_error (bool): Whether the job should continue on error.
        defaults (dict): The default settings for the job.
        outputs (dict): The outputs of the job.
        permissions (dict): The permissions required for the job.
        services (dict): Services required by the job.
        strategy (dict): The strategy for running the job.
        secrets (dict): The secrets required by the job.
        timeout_minutes (int): Timeout setting for the job.
        needs (list): Dependencies of the job.
        uses (list): Actions that the job uses.
        with_params (dict): Parameters for the job.
        raw (dict): The raw representation of the job.
    """

    def __init__(self):
        self.name = None
        self._id = None
        self.runs_on = None
        self.steps = {}
        self.env = {}
        self._if = None
        self.concurrency = None
        self.container = None
        self.continue_on_error = None
        self.defaults = {}
        self.outputs = {}
        self.permissions = {}
        self.services = {}
        self.strategy = {}
        self.secrets = {}
        self.timeout_minutes = None
        self.needs = []
        self.uses = None
        self.with_params = {}
        self.raw = {}

    def __str__(self):
        return (f"Job("
                f"Name = {self.name},\n"
                f"Id = {self._id},\n"
                f"Runs_on = {self.runs_on},\n"
                f"Steps = {self.steps},\n"
                f"Rnv = {self.env},\n"
                f"If = {self._if},\n"
                f"Concurrency = {self.concurrency},\n"
                f"Container = {self.container},\n"
                f"Continue_on_Error = {self.continue_on_error},\n"
                f"Defaults = {self.defaults},\n"
                f"Outputs = {self.outputs},\n"
                f"Permissions = {self.permissions},\n"
                f"Services = {self.services},"
                f"Strategy = {self.strategy},\n"
                f"Secrets = {self.secrets},\n"
                f"Timeout_Minutes = {self.timeout_minutes},\n"
                f"Needs = {self.needs},\n"
                f"Uses = {self.uses},\n"
                f"With = {self.with_params},\n"
                f"Raw = {self.raw})")
