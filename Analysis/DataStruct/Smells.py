class Smells:
    """
    A class to represent a smell struct.
    Parameters that will be used in the smell structure:
        - category: The category of the smell
        - name: The type of the smell
        - description: A description of the smell
        - strategy: The strategy to detect the smell
        - mitigation: The mitigation strategy for the smell
        - severity_level: The severity level of the smell
        - severity_justification: The justification for the severity level
    """

    def __init__(self, category, name, description, strategy, mitigation, severity_level, severity_justification):
        self.category = category
        self.name = name
        self.description = description
        self.strategy = strategy
        self.mitigation = mitigation
        self.severity_level = severity_level
        self.severity_justification = severity_justification

    def __str__(self):
        return (f"Category: {self.category}\n"
                f"Name: {self.name}\n"
                f"Description: {self.description}\n"
                f"Strategy: {self.strategy}\n"
                f"Mitigation: {self.mitigation}\n"
                f"Severity Level: {self.severity_level}\n"
                f"Severity Justification: {self.severity_justification}")


def create_smells_from_dict(severities):
    smells_list = []
    for category, data in severities["Categories"].items():
        for smell_name, smell_data in data["Smells"].items():
            smellier = Smells(
                category=category,
                name=smell_name,
                description=smell_data["Description"],
                strategy=smell_data["Strategy"],
                mitigation=smell_data["Mitigation"],
                severity_level=smell_data["Vulnerability"]["Level"],
                severity_justification=smell_data["Vulnerability"]["Justification"]
            )
            smells_list.append(smellier)
    return smells_list

