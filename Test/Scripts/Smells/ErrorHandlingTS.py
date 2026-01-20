import pytest
import logging
from Analysis.Parse.ActionParser import Action
from Analysis.Smells.Categories.Maintenance.ErrorHandling.ErrorHandlingFct import ErrorHandlingFct
from Analysis.Smells.Categories.Maintenance.ErrorHandling.ErrorHandlingSt import MainErrorHandlingCheck

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def workflow():
    action = Action(file_path='../../Yamls/Smells/Prisma/benchmark.yml')
    workflow = action.prepare_for_analysis()
    return workflow


def test_continue_on_error(workflow):
    checker = MainErrorHandlingCheck()
    findings = checker.check_continue_on_error(workflow)
    logging.debug(f"Findings: {findings}")

    expected_findings = [

    ]

    assert sorted(findings) == sorted(expected_findings)


def test_fail_fast(workflow):
    checker = MainErrorHandlingCheck()
    findings = checker.check_fail_fast(workflow)
    logging.debug(f"Findings: {findings}")

    expected_findings = [

    ]

    assert sorted(findings) == sorted(expected_findings)


def test_timeout(workflow):
    checker = MainErrorHandlingCheck()
    findings = checker.check_timeouts(workflow)
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        "Job 'benchmark' does not have a timeout set. It is recommended to set a "
        'timeout for jobs to prevent them from running with the default value of 6 '
        'hours and consuming resources unnecessarily.',
        "Step 'Install & build' does not have a timeout set. It is recommended to set "
        'a timeout for steps to prevent them from running with the default value of 6 '
        'hours and consuming resources unnecessarily.',
        "Step 'None' does not have a timeout set. It is recommended to set a timeout "
        'for steps to prevent them from running with the default value of 6 hours and '
        'consuming resources unnecessarily.',
        "Step 'Run benchmarks for Codspeed' does not have a timeout set. It is "
        'recommended to set a timeout for steps to prevent them from running with the '
        'default value of 6 hours and consuming resources unnecessarily.',
        "Step 'Run benchmarks' does not have a timeout set. It is recommended to set "
        'a timeout for steps to prevent them from running with the default value of 6 '
        'hours and consuming resources unnecessarily.',
        "Step 'Set current job url in SLACK_FOOTER env var' does not have a timeout "
        'set. It is recommended to set a timeout for steps to prevent them from '
        'running with the default value of 6 hours and consuming resources '
        'unnecessarily.',
        "Step 'Slack Notification on Failure' does not have a timeout set. It is "
        'recommended to set a timeout for steps to prevent them from running with the '
        'default value of 6 hours and consuming resources unnecessarily.',
        "Step 'Store benchmark result' does not have a timeout set. It is recommended "
        'to set a timeout for steps to prevent them from running with the default '
        'value of 6 hours and consuming resources unnecessarily.'
    ]

    assert sorted(findings) == sorted(expected_findings)


def test_integration(workflow):
    logging.debug(f"Running test_missing_parameters with workflow: {workflow}")
    factory = ErrorHandlingFct(content=workflow)
    findings = factory.detect()
    logging.debug(f"Findings: {findings}")

    expected_findings = [

        "Job 'benchmark' does not have a timeout set. It is recommended to set a "
        'timeout for jobs to prevent them from running with the default value of 6 '
        'hours and consuming resources unnecessarily.',
        "Step 'Install & build' does not have a timeout set. It is recommended to set "
        'a timeout for steps to prevent them from running with the default value of 6 '
        'hours and consuming resources unnecessarily.',
        "Step 'None' does not have a timeout set. It is recommended to set a timeout "
        'for steps to prevent them from running with the default value of 6 hours and '
        'consuming resources unnecessarily.',
        "Step 'Run benchmarks for Codspeed' does not have a timeout set. It is "
        'recommended to set a timeout for steps to prevent them from running with the '
        'default value of 6 hours and consuming resources unnecessarily.',
        "Step 'Run benchmarks' does not have a timeout set. It is recommended to set "
        'a timeout for steps to prevent them from running with the default value of 6 '
        'hours and consuming resources unnecessarily.',
        "Step 'Set current job url in SLACK_FOOTER env var' does not have a timeout "
        'set. It is recommended to set a timeout for steps to prevent them from '
        'running with the default value of 6 hours and consuming resources '
        'unnecessarily.',
        "Step 'Slack Notification on Failure' does not have a timeout set. It is "
        'recommended to set a timeout for steps to prevent them from running with the '
        'default value of 6 hours and consuming resources unnecessarily.',
        "Step 'Store benchmark result' does not have a timeout set. It is recommended "
        'to set a timeout for steps to prevent them from running with the default '
        'value of 6 hours and consuming resources unnecessarily.'

    ]

    assert sorted(findings) == sorted(expected_findings)
