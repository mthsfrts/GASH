from Analysis.Smells.Categories.Security.RemoteTriggers.RemoteTriggersSt import MainRemoteRunCheck
from Analysis.Smells.Categories.Security.RemoteTriggers.RemoteTriggersFct import RemoteRunFct
from Analysis.Parse.ActionParser import Action
import pytest
from pathlib import Path


@pytest.fixture
def workflow():
    base_dir = Path(__file__).resolve().parent
    yaml_path = base_dir / "../../Yamls/Smells/RemoteTriggers.yaml"
    yaml_path = yaml_path.resolve()

    action = Action(file_path=str(yaml_path))
    workflow = action.prepare_for_analysis()

    assert workflow is not None
    return workflow


def test_remote_dispatch(workflow):
    checker = MainRemoteRunCheck()
    findings = checker.check_dispatch(workflow)

    expected_findings = [
    ]

    assert sorted(findings) == sorted(expected_findings)


def test_remote_call(workflow):
    checker = MainRemoteRunCheck()
    findings = checker.check_call(workflow)

    expected_findings = [
        "Input 'call_input_03' has an invalid type 'invalid_type'.",
        "Input 'call_input_03' lacks a description. Consider adding a "
        "description for better understanding and maintenance.",
        "Input 'call_input_04' is required but has no default value.",
        "Input 'call_input_08' is required but has no default value.",
        "Input 'call_input_11' is required but has no default value.",
        "Input 'call_input_13' of type 'boolean' should not be required. "
        "Consider removing the parameter.",
        "Input 'call_input_16' is required but has no default value.",
        "Input 'call_input_17' of type 'choice' lacks an 'options' definition.",
        'The trigger has too many inputs. Consider revisiting your original Action '
        'to see the need for all of the inputs. An overflow of inputs might cause '
        'security and maintenance issues.',
        'Workflow call trigger is set with a higher permission on a workflow level. '
        'Consider the add best security protocol for it. This trigger might harm '
        'your pipeline if it is not configured correctly.',
        'You should be careful when referencing secrets in workflow call. '
        'Consider using Secrets Env to do so. Ex: ${{ secrets.SECRET_NAME }}.'
    ]
    assert sorted(findings) == sorted(expected_findings)


def test_remote_run(workflow):
    checker = MainRemoteRunCheck()
    findings = checker.check_run(workflow)

    expected_findings = [
        "Workflow-run has both 'branches' and 'branches-ignore' defined. If you want "
        'to both include and exclude branch patterns for a single event, use the '
        "branches filter along with the '!' character to indicate which branches "
        'should be excluded. The misconfiguration of it might cause you issues but '
        'not a directly security one.'
    ]

    assert sorted(findings) == sorted(expected_findings)


def test_remote_integration(workflow):
    checker = RemoteRunFct(workflow)
    findings = checker.detect()

    expected_findings = [
        "Input 'call_input_03' has an invalid type 'invalid_type'.",
        "Input 'call_input_03' lacks a description. Consider adding a "
        "description for better understanding and maintenance.",
        "Input 'call_input_04' is required but has no default value.",
        "Input 'call_input_08' is required but has no default value.",
        "Input 'call_input_11' is required but has no default value.",
        "Input 'call_input_13' of type 'boolean' should not be required. "
        "Consider removing the parameter.",
        "Input 'call_input_16' is required but has no default value.",
        "Input 'call_input_17' of type 'choice' lacks an 'options' definition.",
        'Invalid configuration for workflow_dispatch: expected a dictionary, '
        'but got NoneType. Ensure the workflow_dispatch configuration is properly defined.',
        'The trigger has too many inputs. Consider revisiting your original Action to see '
        'the need for all of the inputs. An overflow of inputs might cause security and '
        'maintenance issues.',
        'Workflow call trigger is set with a higher permission on a workflow level. '
        'Consider the add best security protocol for it. This trigger might harm '
        'your pipeline if it is not configured correctly.',
        "Workflow-run has both 'branches' and 'branches-ignore' defined. "
        "If you want to both include and exclude branch patterns for a single event, "
        "use the branches filter along with the '!' character to indicate which branches"
        " should be excluded. The misconfiguration of this might cause issues, but not directly "
        "security-related ones.",
        'Workflow-run lacks a workflow. You need to add an event to trigger the run parameter.',
        'You should be careful when referencing secrets in workflow call. '
        'Consider using Secrets Env to do so. Ex: ${{ secrets.SECRET_NAME }}.'
    ]
    assert sorted(findings) == sorted(expected_findings)
