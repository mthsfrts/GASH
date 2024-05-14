class AntiPattern:
    """
    A class to represent a smell struct.
    Parameters that will be used in the smell structure:
        - type: The type of the smell
        - description: A description of the smell
        - location: The location of the smell
        - severity: The severity of the smell
        - additional_info: Additional information about the smell
    """

    def __init__(self):
        self.type = None
        self.description = None
        self.location = None
        self.severity = None
        self.additional_info = {}


# Dictionaries and Lists params for the smells
SEVERITIES = {
    "CodeDuplicity": {
        "severity": "Medium",
        "justification": "Duplicated code can make maintenance more challenging and introduce inconsistencies."
    },
    "LongCodeBlock": {
        "severity": "Low",
        "justification": "While it might affect readability, it's not directly harmful. However, extremely lengthy "
                         "code might be a sign of overly complex functions or logic."
    },
    "Globals": {
        "severity": "Medium",
        "justification": "They can lead to unexpected behaviors and make the code less modular."
    },
    "Conditionals": {
        "severity": "Medium",
        "justification": "Numerous conditionals or complex logic can make the code hard to understand and maintain."
    },
    "ContinueOnError": {
        "severity": "Critical",
        "justification": "Ignoring errors can lead to unexpected behaviors, security breaches, or generated corruption."
    },
    "CodeReuse": {
        "severity": "Low to Medium",
        "justification": "Reuse can be beneficial, but if done incorrectly or without proper modularization, "
                         "it can lead to maintenance issues."
    },
    "Retries": {
        "severity": "Medium",
        "justification": "Excessive retries might mask underlying issues."
    },
    "WorkflowDispatch": {
        "severity": "Critical",
        "justification": "Running external scripts can introduce security vulnerabilities, especially if the origin "
                         "or integrity of the script isn't verified."
    },
    "Vulnerabilities": {
        "severity": "Critical",
        "justification": "Exposure of sensitive information or potential entry points for attacks."
    }
}

GENERIC_NAMES = ["generated",
                 "info",
                 "value",
                 "var",
                 "item",
                 "array",
                 "list",
                 "object"]

KEYWORDS = [
    "creds?",
    "tokens?",
    "\w*secret\w*?",
    "\w*login\w*",
    "\w*secure\w*",
    "o?auth0?",
    "\w*key\w*",
    "\w*password\w*",
    "pwd?",
    "pass(wd|phrase)?",
    "\w*registry\w*",
    "ssh_connect",
    "encryption",
    "api_key",
    "secret_key",
    "private_key",
    "access_key",
    "auth_key",
    "credential",
    "signature",
    "signing_key",
    "admin",
    "root",
    "sudo",
    "\w*token\w*",
    "db_password",
    "database_url",
    "connection_string",
    "\w*cert\w*",
    "\w*rsa\w*",
    "\w*dsa\w*",
    "\w*ecdsa\w*",
    "\w*pgp\w*",
    "\w*ssh\w*",
    "\w*ssl\w*",
    "database",
    "db_user",
    "db_name",
    "host",
    "port",
    "aws",
    "s3",
    "azure",
    "gcp",
    "salt",
    "iv",
    "cipher"
]
