class Step:
    """
    A class to represent a step in a job.

    Attributes:
        name (str): The name of the step.
        _id (str): The identifier for the step.
        uses (str): The action to be used in the step.
        run (str): The command to be executed in the step.
        working_directory (str): The working directory for the step.
        env (dict): The environment variables that the step will use.
        _if (str): The condition that the step will run.
        continue_on_error (bool): Whether the step should continue on error.
        timeout_minutes (int): Timeout setting for the step.
        _id (str): The identifier for the step.
        uses (list): List of actions to be used in the step.
        with_params (dict): Parameters for the action.
        raw (dict): The raw dictionary of the step.
    """

    def __init__(self):
        self.name = None
        self._id = None
        self.uses = None
        self.run = None
        self.working_directory = None
        self.env = {}
        self._if = None
        self.continue_on_error = None
        self.timeout_minutes = None
        self.uses = None
        self.with_params = {}
        self.raw = {}

    def __str__(self):
        return (f"Step("
                f"Name = {self.name},\n"
                f"ID = {self._id},\n"
                f"Uses = {self.uses},\n"
                f"Run = {self.run},\n"
                f"Env = {self.env},\n"
                f"If = {self._if},\n"
                f"Continue_on_Error = {self.continue_on_error},\n"
                f"Timeout_Minutes = {self.timeout_minutes},\n"
                f"Uses = {self.uses},\n"
                f"With = {self.with_params},\n"
                f"Raw = {self.raw})")
