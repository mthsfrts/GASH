import pytest
import logging
from Analysis.Parse.ActionParser import Action
from Analysis.Smells.Categories.Maintenance.ErrorHandling.ErrorHandlingFct import ErrorHandlingFct
from Analysis.Smells.Categories.Maintenance.ErrorHandling.ErrorHandlingSt import MainErrorHandlingCheck

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def workflow():
    action = Action(file_path='../../Yamls/Smells/ErrorHandling.yaml')
    workflow = action.prepare_for_analysis()
    return workflow


def test_continue_on_error(workflow):
    checker = MainErrorHandlingCheck()
    findings = checker.check_continue_on_error(workflow)
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        "Job 'build' has continue-on-error set to true. This could be useful in some "
        'cases, but it is generally not recommended.Meaning that the job will '
        'continue to run even if a step fails. This can lead to unexpected behavior '
        'and should be avoided.',

        "Step 'Checkout' has continue-on-error set to true. This could be useful in "
        'some cases, but it is generally not recommended.Meaning that the step will '
        'continue to run even if it fails. This can lead to unexpected behavior and '
        'should be avoided.']

    assert sorted(findings) == sorted(expected_findings)


def test_fail_fast(workflow):
    checker = MainErrorHandlingCheck()
    findings = checker.check_fail_fast(workflow)
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        "Job 'build' has fail-fast set to false. This means that the job will "
        'continue to run even if a step fails. This can lead to unexpected behavior '
        'and should be avoided.'
    ]

    assert sorted(findings) == sorted(expected_findings)


def test_timeout(workflow):
    checker = MainErrorHandlingCheck()
    findings = checker.check_timeouts(workflow)
    logging.debug(f"Findings: {findings}")

    expected_findings = ["Job 'build' has a timeout of 1 min. This is a short time for a job to run. "
                         'If the timeout have a short value, it will lead to cancel the job before it '
                         'finishes.',
                         "Step 'Checkout' has a timeout of 10 min. This is a long time for a step to "
                         'run. If a step is taking this long to run, it may be a sign that something '
                         'is wrong. It is recommended to investigate why the step is taking so long to '
                         'run and to try to optimize it.']

    assert sorted(findings) == sorted(expected_findings)


def test_integration(workflow):
    logging.debug(f"Running test_missing_parameters with workflow: {workflow}")
    factory = ErrorHandlingFct(content=workflow)
    findings = factory.detect()
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        "Job 'build' has a timeout of 1 min. This is a short time for a job to run. "
        'If the timeout have a short value, it will lead to cancel the job before it '
        'finishes.',

        "Job 'build' has continue-on-error set to true. This could be useful in some "
        'cases, but it is generally not recommended.Meaning that the job will '
        'continue to run even if a step fails. This can lead to unexpected behavior '
        'and should be avoided.',

        "Job 'build' has fail-fast set to false. This means that the job will "
        'continue to run even if a step fails. This can lead to unexpected behavior '
        'and should be avoided.',

        "Step 'Checkout' has a timeout of 10 min. This is a long time for a step to "
        'run. If a step is taking this long to run, it may be a sign that something '
        'is wrong. It is recommended to investigate why the step is taking so long to '
        'run and to try to optimize it.',

        "Step 'Checkout' has continue-on-error set to true. This could be useful in "
        'some cases, but it is generally not recommended.Meaning that the step will '
        'continue to run even if it fails. This can lead to unexpected behavior and '
        'should be avoided.'
    ]

    assert sorted(findings) == sorted(expected_findings)
