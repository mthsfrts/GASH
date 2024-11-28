from Utils.Utilities import Lists


class MainRemoteRunCheck:
    """
    Strategy to check remote triggers configurations in GitHub Actions workflows.
    """

    def __init__(self):
        self.findings = []
        self.list = Lists()

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
        if not isinstance(workflow.on, dict):
            self.findings.append(
                f"Invalid 'workflow.on' configuration: expected a dictionary, but got {type(workflow.on).__name__}. "
                "Ensure the 'on' parameter in the workflow is properly defined."
            )
            return self.findings

        if 'workflow_dispatch' not in workflow.on:
            self.findings.append(
                "No workflow_dispatch trigger found in the workflow configuration. "
                "Ensure it is properly defined if required for manual workflow triggering."
            )
            return self.findings

        dispatch = workflow.on['workflow_dispatch']

        if not isinstance(dispatch, dict):
            self.findings.append(
                f"Invalid configuration for workflow_dispatch: expected a dictionary, but got {type(dispatch).__name__}. "
                "Ensure the workflow_dispatch configuration is properly defined."
            )
            return self.findings

        branches = workflow.on.get('push', {}).get('branches', [])
        permissions = workflow.permissions

        if dispatch is None:
            self.findings.append(
                "Workflow-dispatch is empty. This parameter is mainly responsible for manually triggering the "
                "workflow. Consider a secure configuration for it, as the lack of it might bring critical issues for "
                "your pipeline."
            )
        else:
            if isinstance(permissions, str):
                if permissions in self.list.permissions:
                    for branch in branches:
                        if branch in ['master', 'main', 'production']:
                            self.findings.append(
                                f"Workflow dispatch trigger is set on a critical branch: {branch} "
                                f"with a higher permission: {permissions}, set on the workflow level. "
                                f"Consider adding the best security protocol for it. "
                                f"This trigger might harm your pipeline if it is not configured correctly."
                            )

            elif isinstance(permissions, dict):
                for key, permission in permissions.items():
                    if permission in ['write', 'write-all']:
                        for branch in branches:
                            if branch in ['master', 'main', 'production']:
                                self.findings.append(
                                    f"Workflow dispatch trigger is set on a critical branch: {branch} "
                                    f"with a higher permission: {permission}, set on the workflow level. "
                                    f"Consider adding the best security protocol for it. "
                                    f"This trigger might harm your pipeline if it is not configured correctly."
                                )

            else:
                self.findings.append(
                    "Workflow dispatch trigger is set with a higher permission on the workflow level. "
                    "Consider adding the best security protocol for it. This trigger might harm your pipeline if it "
                    "is not configured correctly."
                )

            if 'inputs' in dispatch:
                inputs = dispatch['inputs']

                if inputs is None:
                    self.findings.append(
                        "Inputs are defined in workflow_dispatch, but the configuration is empty. "
                        "Ensure the inputs parameter is properly defined as a dictionary."
                    )
                elif len(inputs) > 15:
                    self.findings.append(
                        "The trigger has too many inputs. Consider simplifying it, as an overflow of inputs can cause "
                        "security and maintenance issues."
                    )

                if isinstance(inputs, dict):
                    for dispatch_name, dispatch_config in inputs.items():
                        if not isinstance(dispatch_config, dict):
                            self.findings.append(
                                f"Input '{dispatch_name}' has an invalid configuration: expected a dictionary, but got "
                                f"{type(dispatch_config).__name__}. Ensure the input is properly defined."
                            )
                            continue

                        if 'description' not in dispatch_config:
                            self.findings.append(
                                f"Input '{dispatch_name}' lacks a description. Consider adding a description "
                                f"for better understanding and maintenance."
                            )

                        if 'type' in dispatch_config:
                            input_type = dispatch_config['type']
                            if input_type not in ['string', 'boolean', 'choice', 'number', 'environment']:
                                self.findings.append(f"Input '{dispatch_name}' has an invalid type '{input_type}'.")
                            elif input_type is None:
                                self.findings.append(
                                    f"Input '{dispatch_name}' does not have a specified type defined. "
                                    f"You need to define a type for it."
                                )

                            if input_type == 'choice' and 'options' not in dispatch_config:
                                self.findings.append(
                                    f"Input '{dispatch_name}' of type 'choice' lacks an 'options' definition."
                                )

                            if input_type == 'boolean' and 'required' in dispatch_config:
                                self.findings.append(
                                    f"Input '{dispatch_name}' of type 'boolean' should not be required. "
                                    f"Consider removing the parameter."
                                )

                            if ('required' in dispatch_config and dispatch_config['required'] and
                                    'default' not in dispatch_config):
                                self.findings.append(
                                    f"Input '{dispatch_name}' is required but has no default value."
                                )
            else:
                self.findings.append(
                    "No inputs defined for workflow_dispatch. Consider adding some inputs to improve "
                    "security and maintenance."
                )

        return self.findings

    def check_call(self, workflow):
        """
        Check the configuration of the workflow call parameter.

        Args:
            workflow: A Workflow object representing the GitHub Actions workflows.
        """
        if not isinstance(workflow.on, dict):
            self.findings.append(
                f"Invalid configuration for workflow.on: expected a dictionary, but got {type(workflow.on).__name__}. "
                "Ensure the workflow configuration is properly defined."
            )
            return self.findings

        if 'workflow_call' in workflow.on:
            call = workflow.on['workflow_call']

            if not isinstance(call, dict):
                self.findings.append(
                    f"Invalid configuration for workflow_call: expected a dictionary, but got {type(call).__name__}. "
                    "Ensure the workflow_call configuration is properly defined."
                )
                return self.findings

            permissions = workflow.permissions

            if call is not None:
                if isinstance(permissions, dict):
                    for key, permission in permissions.items():
                        if permission in self.list.permissions:
                            self.findings.append(
                                "Workflow call trigger is set with a higher permission on a workflow level. "
                                "Consider the add best security protocol for it. "
                                "This trigger might harm your pipeline if it is not "
                                "configured correctly."
                            )

                if isinstance(permissions, str):
                    if permissions in self.list.permissions:
                        self.findings.append(
                            "Workflow call trigger is set with a higher permission on a workflow level. "
                            "Consider the add best security protocol for it. "
                            "This trigger might harm your pipeline if it is not "
                            "configured correctly."
                        )

                if 'secrets' in call and call['secrets'] is not None:
                    self.findings.append(
                        "You should be careful when referencing secrets in workflow call. Consider using Secrets Env to "
                        "do so. Ex: ${{ secrets.SECRET_NAME }}.")
                else:
                    self.findings.append(
                        "No secrets parameter were found in the workflow call. Consider adding secrets to improve security."
                    )

                if call and 'inputs' in call:
                    inputs = call['inputs']

                    if len(inputs) > 15:
                        self.findings.append(
                            "The trigger has too many inputs. Consider revisiting your original "
                            "Action to see the need for all of the inputs. "
                            "An overflow of inputs might cause security and maintenance issues."
                        )

                    for call_name, call_config in inputs.items():

                        if 'description' not in call_config:
                            self.findings.append(
                                f"Input '{call_name}' lacks a description. Consider adding a description "
                                f"for better understanding and maintenance."
                            )

                        if 'type' in call_config:
                            input_type = call_config['type']
                            if input_type not in ['string', 'boolean', 'choice', 'number', 'environment']:
                                self.findings.append(f"Input '{call_name}' has an invalid type '{input_type}'.")
                            elif input_type is None:
                                self.findings.append(
                                    f"Input '{call_name}' does not have a specified type defined. "
                                    f"You need to define a type for it."
                                )

                            if input_type == 'choice' and 'options' not in call_config:
                                self.findings.append(
                                    f"Input '{call_name}' of type 'choice' lacks an 'options' definition."
                                )

                            if input_type == 'boolean' and 'required' in call_config:
                                self.findings.append(
                                    f"Input '{call_name}' of type 'boolean' should not be required. "
                                    f"Consider removing the parameter."
                                )

                            if 'required' in call_config and call_config['required'] and 'default' not in call_config:
                                self.findings.append(
                                    f"Input '{call_name}' is required but has no default value."
                                )
                else:
                    self.findings.append(
                        "You need to provide inputs for the workflow call trigger to work correctly. "
                        "The lack of inputs can cause critical issues in your pipeline. "
                    )
        else:
            self.findings.append(
                "No workflow_call trigger found in the workflow configuration. "
                "Ensure it is properly defined if required."
            )

        return self.findings

    def check_run(self, workflow):
        """
        Check the configuration of the workflow_run parameter.

        Args:
            workflow: A Workflow object representing the GitHub Actions workflows.
        """
        if not isinstance(workflow.on, dict):
            self.findings.append(
                f"Invalid configuration for workflow.on: expected a dictionary, but got {type(workflow.on).__name__}. "
                "Ensure the workflow configuration is properly defined."
            )
            return self.findings

        if 'workflow_run' in workflow.on:
            run = workflow.on['workflow_run']

            if not isinstance(run, dict):
                self.findings.append(
                    f"Invalid configuration for workflow_run: expected a dictionary, but got {type(run).__name__}. "
                    "Ensure the workflow_run configuration is properly defined."
                )
                return self.findings

            if run is None:
                self.findings.append(
                    "Workflow-run is empty. This parameter is mainly responsible for triggering the workflow when another "
                    "workflow is completed. You need to provide some inputs for the trigger to run."
                )
            else:
                if 'branches' in run and 'branches-ignore' in run:
                    self.findings.append(
                        "Workflow-run has both 'branches' and 'branches-ignore' defined. If you want to both include and "
                        "exclude branch patterns for a single event, use the branches filter along with the '!' character "
                        "to indicate which branches should be excluded. The misconfiguration of this might cause issues, "
                        "but not directly security-related ones."
                    )

                if 'description' not in run:
                    self.findings.append(
                        "Workflow-run lacks a description. Consider adding a description for better "
                        "understanding and maintenance."
                    )

                if 'types' not in run:
                    self.findings.append(
                        "Workflow-run lacks a type. Consider adding a type for better "
                        "understanding and maintenance."
                    )

                if 'workflow' not in run:
                    self.findings.append(
                        "Workflow-run lacks a workflow. You need to add an event to trigger the run parameter."
                    )
        else:
            self.findings.append(
                "No workflow_run trigger found in the workflow configuration. "
                "Ensure it is properly defined if required for triggering workflows based on the completion of other workflows."
            )

        return self.findings
