import pytest
import logging
from Analysis.Parse.ActionParser import Action
from Analysis.Smells.Categories.Maintenance.Misconfiguration.MisconfigurationST import MainMisconfigurationCheck
from Analysis.Smells.Categories.Maintenance.Misconfiguration.MisconfigurationFct import MisconfigurationFct

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def workflow():
    action = Action(file_path='../../Yamls/Smells/Misconfiguration.yaml')
    workflow = action.prepare_for_analysis()
    return workflow


def test_missing_parameters(workflow):
    logging.debug(f"Running test_missing_parameters with workflow: {workflow}")
    checker = MainMisconfigurationCheck()
    findings = checker.check_missing_parameters(workflow)
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        "Job 'build' do not have a runner specified, it will be use the default "
        "runner 'ubuntu-latest'. Consider specifying 'runs-on' explicitly.",

        "Job '{job_name}' is missing the 'environment' parameter. Consider create a "
        'new environment for better security and maintenance. You can find all the '
        'available environments at '
        'https://docs.github.com/en/actions/deployment/targeting-different-environments',
        "Step 'Checkout code' in job 'build' is missing the 'run' parameter. Consider "
        'specifying the shell command to run.',

        "Step 'Install dependencies' in job 'build' is missing the 'uses' parameter. "
        'Consider specifying the action to use.',

        "Step 'Setup Node.js' in job 'build' is missing the 'run' parameter. Consider "
        'specifying the shell command to run.',

        "Step 'DataStruct' in job 'build' is missing the 'uses' parameter. Consider "
        'specifying the action to use.',

        "Workflow is missing the 'defaults' parameter. Consider using the 'defaults' "
        'parameter to set the common values for all your jobs.'
    ]

    assert sorted(findings) == sorted(expected_findings)


def test_fuzzy_versions(workflow):
    logging.debug(f"Running test_fuzzy_versions with workflow: {workflow}")
    checker = MainMisconfigurationCheck()
    findings = checker.check_fuzzy_versions(workflow)
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        "Job 'build' has a step with an unspecified or fuzzy version v2.*. Consider "
        'specifying a more precise version or use the Matrix parameter.',

        "Job 'test' has a step with an unspecified or fuzzy version v2.x. Consider "
        'specifying a more precise version or use the Matrix parameter.'
    ]

    assert sorted(findings) == sorted(expected_findings)


def test_unnecessary_complexity(workflow):
    logging.debug(f"Running test_unnecessary_complexity with workflow: {workflow}")
    checker = MainMisconfigurationCheck()
    findings = checker.check_unnecessary_complexity(workflow)
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        "Job 'build' has a step 'DataStruct' with an unnecessary complexity on 'if' "
        'condition. Consider simplifying the condition ou separating into different '
        'steps ou jobs.',

        "Job 'deploy' has a step 'Deploy' with an unnecessary complexity on 'if' "
        'condition. Consider simplifying the condition ou separating into different '
        'steps ou jobs.',

        "Step 'Deploy' in job 'deploy' has multiple logical operators in 'if' "
        "condition: 'branch == 'main' && tag == 'v1.0' && (event == 'push' || status "
        "== success())'. Consider simplifying the condition ou separating into "
        'different steps ou jobs.',

        "Step 'Deploy' in job 'deploy' has nested 'if' conditions: 'branch == 'main' "
        "&& tag == 'v1.0' && (event == 'push' || status == success())'. Consider "
        'simplifying the condition ou separating into different steps ou jobs.',
        "Step 'DataStruct' in job 'build' has multiple logical operators in 'if' condition: "
        "'branch == 'main' && tag == 'v1.0' && (event == 'push' || status == "
        "success())'. Consider simplifying the condition ou separating into different "
        'steps ou jobs.',

        "Step 'DataStruct' in job 'build' has nested 'if' conditions: 'branch == 'main' && "
        "tag == 'v1.0' && (event == 'push' || status == success())'. Consider "
        'simplifying the condition ou separating into different steps ou jobs.'
    ]

    assert sorted(findings) == sorted(expected_findings)


def test_concurrency(workflow):
    logging.debug(f"Running test_concurrency with workflow: {workflow}")
    checker = MainMisconfigurationCheck()
    findings = checker.check_concurrency(workflow)
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        'Concurrency configuration for cancel-in-progress is not a boolean, valid '
        'GitHub expression or is not set to True. (cancel-in-progress: false). Ensure '
        'cancel-in-progress has the right configuration.'
    ]

    assert sorted(findings) == sorted(expected_findings)


def test_integration(workflow):
    logging.debug(f"Running test_integration with workflow: {workflow}")
    factory = MisconfigurationFct(content=workflow)
    findings = factory.detect()

    expected_findings = [
        'Concurrency configuration for cancel-in-progress is not a boolean, valid '
        'GitHub expression or is not set to True. (cancel-in-progress: false). Ensure '
        'cancel-in-progress has the right configuration.',
        "Job 'build' do not have a runner specified, it will be use the default "
        "runner 'ubuntu-latest'. Consider specifying 'runs-on' explicitly.",
        "Job 'build' has a step 'DataStruct' with an unnecessary complexity on 'if' "
        'condition. Consider simplifying the condition ou separating into different '
        'steps ou jobs.',
        "Job 'build' has a step with an unspecified or fuzzy version v2.*. Consider "
        'specifying a more precise version or use the Matrix parameter.',
        "Job 'deploy' has a step 'Deploy' with an unnecessary complexity on 'if' "
        'condition. Consider simplifying the condition ou separating into different '
        'steps ou jobs.',
        "Job 'test' has a step with an unspecified or fuzzy version v2.x. Consider "
        'specifying a more precise version or use the Matrix parameter.',
        "Job '{job_name}' is missing the 'environment' parameter. Consider create a "
        'new environment for better security and maintenance. You can find all the '
        'available environments at '
        'https://docs.github.com/en/actions/deployment/targeting-different-environments',
        "Step 'Checkout code' in job 'build' is missing the 'run' parameter. Consider "
        'specifying the shell command to run.',
        "Step 'Deploy' in job 'deploy' has multiple logical operators in 'if' "
        "condition: 'branch == 'main' && tag == 'v1.0' && (event == 'push' || status "
        "== success())'. Consider simplifying the condition ou separating into "
        'different steps ou jobs.',
        "Step 'Deploy' in job 'deploy' has nested 'if' conditions: 'branch == 'main' "
        "&& tag == 'v1.0' && (event == 'push' || status == success())'. Consider "
        'simplifying the condition ou separating into different steps ou jobs.',
        "Step 'Install dependencies' in job 'build' is missing the 'uses' parameter. "
        'Consider specifying the action to use.',
        "Step 'Setup Node.js' in job 'build' is missing the 'run' parameter. Consider "
        'specifying the shell command to run.',
        "Step 'DataStruct' in job 'build' has multiple logical operators in 'if' condition: "
        "'branch == 'main' && tag == 'v1.0' && (event == 'push' || status == "
        "success())'. Consider simplifying the condition ou separating into different "
        'steps ou jobs.',
        "Step 'DataStruct' in job 'build' has nested 'if' conditions: 'branch == 'main' && "
        "tag == 'v1.0' && (event == 'push' || status == success())'. Consider "
        'simplifying the condition ou separating into different steps ou jobs.',
        "Step 'DataStruct' in job 'build' is missing the 'uses' parameter. Consider "
        'specifying the action to use.',
        "Workflow is missing the 'defaults' parameter. Consider using the 'defaults' "
        'parameter to set the common values for all your jobs.'
    ]

    assert sorted(findings) == sorted(expected_findings)
