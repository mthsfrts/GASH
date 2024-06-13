class MainErrorHandlingCheck:
    """
    Strategy for checking the error handling of the workflow

    """

    def __init__(self):
        self.findings = []

    def check(self, workflow):
        """
        Check the workflow for lack of error handling.

        Args:
            workflow: A Workflow object representing the GitHub Actions workflows.

        Returns:
            A list of findings indicating lack of error handling.
        """

        self.check_continue_on_error(workflow)
        self.check_fail_fast(workflow)
        self.check_timeouts(workflow)
        return self.findings

    def check_continue_on_error(self, workflow):
        """
        Check if the job has continue-on-error set to true.

        Args:
            workflow: A Job object representing the job in the workflow.

        Returns:
            A list of findings indicating lack of error handling.
        """

        for job_name, job in workflow.jobs.items():
            if job.continue_on_error:
                self.findings.append(f"Job '{job_name}' has continue-on-error set to true. "
                                     f"This could be useful in some cases, but it is generally not recommended."
                                     f"Meaning that the job will continue to run even if a step fails. "
                                     f"This can lead to unexpected behavior and should be avoided.")

            for step in job.steps:
                if step.continue_on_error:
                    self.findings.append(f"Step '{step.name}' has continue-on-error set to true. "
                                         f"This could be useful in some cases, but it is generally not recommended."
                                         f"Meaning that the step will continue to run even if it fails. "
                                         f"This can lead to unexpected behavior and should be avoided.")

        return self.findings

    def check_fail_fast(self, workflow):
        """
        Check if the job has fail-fast set to true.
        """

        for job_name, job in workflow.jobs.items():
            if job.strategy:
                failfast = job.strategy['fail-fast']
                if failfast not in [True, 'True', 'true']:
                    self.findings.append(f"Job '{job.name}' has fail-fast set to {failfast}. "
                                         f"This means that the job will continue to run even if a step fails. "
                                         f"This can lead to unexpected behavior and should be avoided.")

        return self.findings

    def check_timeouts(self, workflow):
        """
        Check the workflow for lack of timeouts.

        Args:
            workflow: A Workflow object representing the GitHub Actions workflows.
        """

        for job_name, job in workflow.jobs.items():
            if job.timeout_minutes is None:
                self.findings.append(f"Job '{job_name}' does not have a timeout set. "
                                     f"It is recommended to set a timeout for jobs to prevent them from running "
                                     f"with the default value of 6 hours and consuming resources unnecessarily.")

            if job.timeout_minutes == 1:
                self.findings.append(f"Job '{job_name}' has a timeout of {job.timeout_minutes} min. "
                                     f"This is a short time for a job to run. If the timeout have a short value, "
                                     f"it will lead to cancel the job before it finishes.")

            if job.timeout_minutes >= 10:
                self.findings.append(f"Job '{job_name}' has a timeout of {job.timeout_minutes} min. "
                                     f"This is a long time for a job to run. If a job is taking this long to run, "
                                     f"it may be a sign that something is wrong. "
                                     f"It is recommended to investigate why the job is taking so long to run "
                                     f"and to try to optimize it.")

            for step in job.steps:
                if step.timeout_minutes is None:
                    self.findings.append(f"Step '{step.name}' does not have a timeout set. "
                                         f"It is recommended to set a timeout for steps to prevent them from running "
                                         f"with the default value of 6 hours and consuming resources unnecessarily.")

                if step.timeout_minutes == 1:
                    self.findings.append(f"Step '{step.name}' has a timeout of {step.timeout_minutes} min. "
                                         f"This is a short time for a step to run. If the timeout have a short value, "
                                         f"it will lead to cancel the step before it finishes.")

                if step.timeout_minutes >= 10:
                    self.findings.append(f"Step '{step.name}' has a timeout of {step.timeout_minutes} min. "
                                         f"This is a long time for a step to run. If a step is taking this long to run, "
                                         f"it may be a sign that something is wrong. "
                                         f"It is recommended to investigate why the step is taking so long to run "
                                         f"and to try to optimize it.")

        return self.findings

        # def check_retry_logic(self, workflow):
    #     for job in workflow.jobs.items():
    #         if job.strategy and not job.strategy.get('fail-fast'):
    #             self.findings.append(
    #                 f"Job '{job_name}' has retry logic but no 'max_attempts' set, which can "
    #                 f"lead to undefined retry behavior.")
    #
    #     return self.findings
