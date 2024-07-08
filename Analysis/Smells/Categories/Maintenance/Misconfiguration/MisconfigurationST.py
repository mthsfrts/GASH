import re


class MainMisconfigurationCheck:
    """
    Strategy to check for misconfigurations in GitHub Actions workflows.

    Attributes:
        self.findings: A list containing the misconfiguration self.findings.
    """

    def __init__(self):
        self.findings = []

    def check(self, workflow):
        """
        Check for various misconfigurations in the workflow.

        Args:
            workflow: A Workflow object representing the GitHub Actions workflows.

        Returns:
            A list containing the misconfiguration self.findings.
        """

        self.check_missing_parameters(workflow)
        self.check_fuzzy_versions(workflow)
        self.check_unnecessary_complexity(workflow)
        self.check_concurrency(workflow)

        return self.findings

    def check_missing_parameters(self, workflow):
        """
        Check for missing parameters in the workflow.

        Args:
            workflow: A Workflow object representing the GitHub Actions workflows.
        """

        # Checking for missing parameters in the Workflow level
        if not workflow.name:
            self.findings.append(
                "No 'name' were set for the workflow. "
                "Consider providing an 'alias' for the workflow for better maintenance.")

        if not workflow.on:
            self.findings.append(
                "Workflow is missing the 'on' parameter. "
                "You need to provide a trigger event."
            )

        if not workflow.defaults:
            self.findings.append(
                "No 'defaults' values were set on the workflow. Consider using the 'defaults' "
                "parameter to set the common values for all your jobs."
            )

        # Check for missing parameters in the Job and Step level
        for job_name, job in workflow.jobs.items():

            if not job.environment:
                self.findings.append(
                    f"Job '{job_name}' has no 'environment' parameter set. "
                    "Consider create environments for better security and maintenance. "
                    "You can find all the info about it at "
                    "https://docs.github.com/en/actions/deployment/targeting-different-environments"
                )

            if not job.runs_on:
                self.findings.append(
                    f"Job '{job_name}' do not have a runner specified, "
                    f"it will be use the default runner 'ubuntu-latest'. "
                    f"Consider specifying 'runs-on' explicitly.")

            for step in job.steps:
                if not step.uses:
                    self.findings.append(
                        f"Step '{step.name}' in job '{job_name}' is missing the 'uses' parameter. "
                        f"Consider specify an action for it.")

                if not step.run:
                    self.findings.append(
                        f"Step '{step.name}' in job '{job_name}' is missing the 'run' parameter. "
                        f"Consider specifying the command to run.")

            return self.findings

    def check_fuzzy_versions(self, workflow):
        """
        Check for fuzzy or unspecified versions in the 'uses' declaration.

        Args:
            workflow: A Workflow object representing the GitHub Actions workflows.
        """
        fuzzy_version_pattern = re.compile(r'@v?\d+\.(?:x|\*|\d+\.x|\d+\.\*|latest|\d+\.\d+\.\*)')

        for job_name, job in workflow.jobs.items():
            for step in job.steps:
                uses = step.uses
                if uses and fuzzy_version_pattern.search(uses):
                    version = uses.split('@')[1] if '@' in uses else 'unknown'
                    self.findings.append(
                        f"Job '{job_name}' has a step with an unspecified or fuzzy version {version}. "
                        f"Consider specifying a more precise version or use the Matrix parameter."
                    )
        return self.findings

    def check_unnecessary_complexity(self, workflow):
        """
        Check for unnecessary complexity conditions in the workflow.

        Args:
            workflow: A Workflow object representing the GitHub Actions workflows.
        """

        for job_name, job in workflow.jobs.items():
            for step in job.steps:
                if step._if:
                    conditions = step._if.split("&&")
                    if len(conditions) > 2:
                        self.findings.append(
                            f"Job '{job_name}' has a step '{step.name}' "
                            f"with an unnecessary complexity on 'if' condition. "
                            f"Consider simplifying the condition ou separating into different steps ou jobs."
                        )

                    # Check for nested conditions
                    nested_conditions = re.findall(r'\(([^)]+)\)', step._if)
                    if nested_conditions:
                        self.findings.append(
                            f"Step '{step.name}' in job '{job_name}' has nested 'if' conditions: '{step._if}'. "
                            f"Consider simplifying the condition ou separating into different steps ou jobs."
                        )

                    # Check for multiple logical operators
                    logical_operator_count = len(re.findall(r'(\|\||&&)', step._if))
                    if logical_operator_count > 1:
                        self.findings.append(
                            f"Step '{step.name}' in job '{job_name}' has multiple logical operators in 'if' condition: '{step._if}'. "
                            f"Consider simplifying the condition ou separating into different steps ou jobs."
                        )

        return self.findings

    def check_concurrency(self, workflow):
        """
        Check for concurrency issues in the workflow.

        Args:
            workflow: A Workflow object representing the GitHub Actions workflows.
        """

        concurrency = workflow.concurrency

        def is_valid_expression(expression):
            # Simple regex to check for GitHub expression syntax
            return re.match(r"\$\{\{.*\}\}", expression.strip()) is not None

        if concurrency:
            if 'group' not in concurrency or not isinstance(concurrency['group'], str):
                self.findings.append(
                    f"Concurrency configuration is missing the 'group' parameter or it is not a string: "
                    f"{concurrency.get('group')}. "
                    f"Ensure 'group' is specified and is a string.")

            if 'cancel-in-progress' not in concurrency:
                self.findings.append(
                    f"Concurrency configuration is missing the cancel-in-progress. "
                    f"Ensure 'cancel-in-progress' is specified and is a boolean.")

            if 'cancel-in-progress' in concurrency:
                cancel = concurrency.get('cancel-in-progress')
                if cancel not in ['True', 'true', True] and not is_valid_expression(cancel):
                    self.findings.append(
                        f"Concurrency configuration for cancel-in-progress is not a boolean, valid GitHub "
                        f"expression or is not set to True. (cancel-in-progress: {cancel}). "
                        f"Ensure cancel-in-progress has the right configuration.")

        else:
            return self.findings
