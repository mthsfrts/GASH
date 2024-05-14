class Step:
    """
    A class to represent a step in a workflow.\n
    Parameters that will be used in the step structure:
    - name: The name of the step.\n
    - action: The action to use.\n
    - command: The command to run.\n
    - arguments: The arguments to use.\n
    - environment_vars: The environment variables to use.\n
    - condition: The condition to use.\n
    - smells: The smells to use.\n

    """
    def __init__(self):
        self.name = None
        self.action = None
        self.command = None
        self.arguments = {}
        self.environment_vars = {}
        self.condition = None
        self.smells = []
