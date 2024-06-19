class MainLongBlockCheck:
    """
    Strategy for checking long blocks of code on the workflow.
    """

    def __init__(self):
        self.findings = []
        self.max_job_per_workflow = 10
        self.max_steps_per_job = 10
        self.max_commands_per_step = 20

    def check(self, workflow):
        """
        Check the long blocks of code.

        Args:
            workflow: A Workflow object representing the GitHub Actions workflows.

        Returns:
            findings: List of long code blocks.
        """

        self.long_block_check(workflow)

        return self.findings

    def long_block_check(self, workflow):
        """
        Check the long blocks of code.

        Args:
            workflow: A Workflow object representing the GitHub Actions workflows.
        """

        jobs_count = len(workflow.jobs)

        if jobs_count > self.max_job_per_workflow:
            self.findings.append(f"The workflow has more than {jobs_count} jobs. "
                                 f"Consider splitting the jobs into multiple workflows. "
                                 f"A longer pipeline can be difficult to maintain and "
                                 f"debug and can lead to security vulnerabilities.")

        for jobs_, job in workflow.jobs.items():
            steps_count = len(job.steps)
            if steps_count > self.max_steps_per_job:
                self.findings.append(f"The job '{jobs_}' has more than {steps_count} steps. "
                                     f"Consider splitting the steps into multiple jobs. "
                                     f"A longer job can be difficult to maintain and "
                                     f"debug and can lead to security vulnerabilities.")

            for step in job.steps:
                if step.run is None:
                    self.findings.append(f"The step '{step.name}' does not have any commands to run.")
                else:
                    commands_count = len(step.run.split('\n'))
                    if commands_count > self.max_commands_per_step:
                        self.findings.append(f"The step '{step.name}' run has more than {commands_count} commands. "
                                             f"Consider splitting the commands into multiple step groups. "
                                             f"A longer step group can be difficult to maintain and "
                                             f"debug and can lead to security vulnerabilities.")

        return self.findings

