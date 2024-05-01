class Job:
    """
    A class to represent a job in a workflow.\n
    Parameter thar will be used struct the class.\n
    - name: The name of the job.\n
    - machine_type: The machine type that the job will run.\n
    - steps: The steps that the job will run.\n
    - environment_vars: The environment variables that the job will use.\n
    - condition: The condition that the job will run.\n
    - smells: The smells that the job will use.\n
    """
    def __init__(self):
        self.name = None
        self.machine_type = None  # 'runs-on' field
        self.steps = []  # List of Step objects
        self.environment_vars = {}  # 'env' field for the job
        self.condition = None  # 'if' field
        self.smells = []  # List of AntiPattern objects
