class MainRemoteRunCheck:
    """
    Strategy to check remote triggers configurations in GitHub Actions workflows.
    """

    def __init__(self):
        self.findings = []

    def check(self, workflow):
        """
        Checks remote triggers configurations in the workflow
        """

        self.check_dispatch(workflow)
        self.check_call(workflow)
        self.check_run(workflow)

        return self.findings

    def check_dispatch(self, workflow):
        """
        Check the configuration of the workflow dispatch parameter.

        Args:
            workflow: A Workflow object representing the GitHub Actions workflows.
        """
        dispatch = workflow.on['workflow_dispatch']
        branches = workflow.on['push']['branches']
        permissions = workflow.permissions

        if dispatch is None:
            self.findings.append(
                "Workflow-dispatch is empty. This parameter is mainly responsible for manually trigger the workflow."
                "Consider a secure configuration for it, the lack of it might bring critical issues for your pipeline."
            )

        if isinstance(permissions, str):
            if permissions in ['write', 'write-all']:
                for branch in branches:
                    if branch in ['master', 'main', 'production']:
                        self.findings.append(
                            f"Workflow dispatch trigger is set on a critical branch: {branch}"
                            f", with a higher permission: {permissions}, set on the workflow level. "
                            f"Consider adding the best security protocol for it. "
                            f"This trigger might harm your pipeline if it is not configured correctly."
                        )

        elif isinstance(permissions, dict):
            for key, permission in permissions.items():
                if permission in ['write', 'write-all']:
                    for branch in branches:
                        if branch in ['master', 'main', 'production']:
                            self.findings.append(
                                f"Workflow dispatch trigger is set on a critical branch: {branch}"
                                f", with a higher permission: {permission}, set on the workflow level. "
                                f"Consider adding the best security protocol for it. "
                                f"This trigger might harm your pipeline if it is not configured correctly."
                            )

        else:
            self.findings.append(
                "Workflow dispatch trigger is set with a higher permission on the workflow level. "
                "Consider the add best security protocol for it. This trigger might harm your pipeline if it is not "
                "configure correctly."
            )

        if 'inputs' in dispatch:
            inputs = dispatch['inputs']

            if len(inputs) > 15:
                self.findings.append("The trigger has too many inputs. Consider simplify it, "
                                     "the inputs overflow, can cause security and maintenance issues.")

            for dispatch_name, dispatch_config in inputs.items():

                if 'description' not in dispatch_config:
                    self.findings.append(f"Input '{dispatch_name}' lacks a description. Consider add a description "
                                         f"for a better understanding and maintenance.")

                if 'type' in dispatch_config:
                    input_type = dispatch_config['type']
                    if input_type not in ['string', 'boolean', 'choice', 'number', 'environment']:
                        self.findings.append(f"Input '{dispatch_name}' has an invalid type '{input_type}'.")
                    elif input_type is None:
                        self.findings.append(f"Input '{dispatch_name}' does not have a specified type defined. "
                                             f"You need to define a type for it.")

                    if input_type == 'choice' and 'options' not in dispatch_config:
                        self.findings.append(f"Input '{dispatch_name}' of type 'choice' lacks 'options' definition.")

                    if input_type == 'boolean' and 'required' in dispatch_config:
                        self.findings.append(
                            f"Input '{dispatch_name}' of type 'boolean' should not be required. "
                            f"Consider remove the parameter.")

                    if ('required' in dispatch_config and dispatch_config['required'] and 'default'
                            not in dispatch_config):
                        self.findings.append(f"Input '{dispatch_name}' is required but has no default value.")
        else:
            self.findings.append("No inputs defined for workflow dispatch. Consider add some inputs to better "
                                 "security and maintenance.")

        return self.findings

    def check_call(self, workflow):
        """
        Check the configuration of the workflow call parameter.

        Args:
            workflow: A Workflow object representing the GitHub Actions workflows.
        """
        call = workflow.on['workflow_call']
        secrets = call['secrets']
        permissions = workflow.permissions

        if isinstance(permissions, dict):
            for key, permission in permissions.items():
                if permission in ['write-all', 'write']:
                    self.findings.append(
                        "Workflow call trigger is set with a higher permission on a workflow level. "
                        "Consider the add best security protocol for it. "
                        "This trigger might harm your pipeline if it is not "
                        "configure correctly."
                    )

        if isinstance(permissions, str):
            if permissions in ['write', 'write-all']:
                self.findings.append(
                    "Workflow call trigger is set with a higher permission on a workflow level. "
                    "Consider the add best security protocol for it. "
                    "This trigger might harm your pipeline if it is not "
                    "configure correctly."
                )

        if secrets:
            self.findings.append(
                "Secrets should not be directly referenced in workflow call. Consider use Secrets Env to do so. "
                "Ex: ${{ secrets.SECRET_NAME }}.")

        if 'inputs' in call:
            inputs = call['inputs']

            if len(inputs) > 15:
                self.findings.append("The trigger has too many inputs. Consider revisit your original "
                                     "Action to see the need for all of the inputs. "
                                     "The inputs overflow, might cause security and maintenance issues.")

            for call_name, call_config in inputs.items():

                if 'description' not in call_config:
                    self.findings.append(f"Input '{call_name}' lacks a description. Consider add a description "
                                         f"for a better understanding and maintenance.")

                if 'type' in call_config:
                    input_type = call_config['type']
                    if input_type not in ['string', 'boolean', 'choice', 'number', 'environment']:
                        self.findings.append(f"Input '{call_name}' has an invalid type '{input_type}'.")
                    elif input_type is None:
                        self.findings.append(f"Input '{call_name}' does not have a specified type defined. "
                                             f"You need to define a type for it.")

                    if input_type == 'choice' and 'options' not in call_config:
                        self.findings.append(f"Input '{call_name}' of type 'choice' lacks 'options' definition.")

                    if input_type == 'boolean' and 'required' in call_config:
                        self.findings.append(
                            f"Input '{call_name}' of type 'boolean' should not be required. "
                            f"Consider remove the parameter.")

                    if 'required' in call_config and call_config['required'] and 'default' not in call_config:
                        self.findings.append(f"Input '{call_name}' is required but has no default value.")
        else:
            self.findings.append("You need to provide inputs for the workflow call trigger work correctly. "
                                 "The lack of inputs can cause you critical issues on your pipeline. ")

        return self.findings

    def check_run(self, workflow):
        run = workflow.on['workflow_run']

        if run is None:
            self.findings.append(
                "Workflow-run is empty. This parameter is mainly responsible for trigger the workflow when another "
                "workflow is completed. You need to provide some inputs for the trigger to run."
            )

        if 'branches' and 'branches-ignore' in run:
            self.findings.append(
                "Workflow-run has both 'branches' and 'branches-ignore' defined. If you want to both include and "
                "exclude branch patterns for a single event, use the branches filter along with the '!' character to "
                "indicate which branches should be excluded. The misconfiguration of it might cause you issues but "
                "not a directly security one."
            )

        if 'description' not in run:
            self.findings.append(
                "Workflow-run lacks a description. Consider add a description for a better "
                "understanding and maintenance."
            )

        if 'types' not in run:
            self.findings.append(
                "Workflow-run lacks a type. Consider add a type for a better"
                " understanding and maintenance."
            )

        if 'workflow' not in run:
            self.findings.append(
                "Workflow_run lacks a workflow. You need to add a event to trigger the Run."
            )
        return self.findings
