class MainCodeReplicaCheck:
    """
    Strategy to check for replicated code snippets and variable values in GitHub Actions workflows.

    Args:
        threshold: The number of replicas to consider as an issue.
    """

    def __init__(self, threshold=2):
        self.threshold = threshold
        self.value_counts = {}
        self.findings = []

    def check(self, workflow):
        """
        Get the replicated code snippets and variable values in GitHub Actions workflows.

        Args:
            workflow: A Workflow object representing the GitHub Actions workflows.

        Returns:
            A list containing the replicated code snippets and variable values.
        """

        self.check_duplicate_values(workflow)
        self.check_duplicate_jobs(workflow)
        return self.findings

    def check_duplicate_values(self, workflow):
        """
        Check for replicated values across workflow, jobs, and steps.

        Args:
            workflow: A Workflow object.
        """
        self.value_counts = {}

        # Check global env values
        # for key, value in workflow.env.items():
        #     self.add_to_counts(value, f"Global env variable '{key}'. "
        #                               f"Consider define different names for Globals", findings)

        # Check jobs and steps
        for job_name, job in workflow.jobs.items():
            for key, value in job.env.items():
                self.add_to_counts(value, f"Job '{job_name}' env variable '{key}'")

            for step in job.steps:
                for key, value in step.env.items():
                    self.add_to_counts(value, f"Step '{step.name}' env variable '{key}' in job '{job_name}' "
                                              f"is replicated. Consider use Global Env variables: Ex: Env: '{key}': "
                                              f"'{value}'")

                for key, value in step.with_params.items():
                    self.add_to_counts(value, f"Step '{step.name}' parameter '{key}' in job '{job_name}' "
                                              f"is replicated. Consider use Defaults params. Ex: Defaults: '{key}': "
                                              f"'{value}'")

    def add_to_counts(self, value, context):
        """
        Add the value to the count dictionary and check if it exceeds the threshold.

        Args:
            value: The value to check.
            context: The context where the value was found.
        """
        if value not in self.value_counts:
            self.value_counts[value] = []
        self.value_counts[value].append(context)

        if len(self.value_counts[value]) == self.threshold:
            contexts = ', '.join(self.value_counts[value])
            self.findings.append(f"Value '{value}' is replicated in contexts: {contexts}. If not an Env consider use "
                                 f"Matrix to define versions. Ex: 'strategy: matrix: {{'python': ['3.6', '3.7', "
                                 f"'3.8']}}'")

    def check_duplicate_jobs(self, workflow):
        """
        Check for replicated jobs based on their steps.

        Args:
            workflow: A Workflow object.
        """
        job_signatures = {}
        for job_name, job in workflow.jobs.items():
            job_signature = self.create_job_signature(job)
            if job_signature in job_signatures:
                self.findings.append(f"Job '{job_name}' is replicated with job '{job_signatures[job_signature]}'. "
                                     f"Consider use reusable actions. You can find examples in the documentation: "
                                     f"https://docs.github.com/en/actions/using-workflows/reusing-workflows")
            else:
                job_signatures[job_signature] = job_name

    @staticmethod
    def create_job_signature(job):
        """
        Create a unique signature for a job based on its steps.

        Args:
            job: A Job object.

        Returns:
            A string representing the unique signature of the job.
        """
        step_signatures = []
        for step in job.steps:
            step_signature = (f"{step.name}-{step.run}-{step.uses}-{sorted(step.env.items())}"
                              f"{sorted(step.with_params.items())}")
            step_signatures.append(step_signature)
        return "|".join(step_signatures)
