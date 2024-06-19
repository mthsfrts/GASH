import pytest
import logging
from Analysis.Smells.Categories.Security.UnsecureProtocol.UnsecureProtocolFct import UnsecureProtocolFct
from Analysis.DataStruct import Workflow, Jobs, Steps
from Analysis.Parse.ActionParser import Action

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def workflow():
    workflow = Workflow.Workflow()
    workflow.env = {"API_URL": "http://unsecure-url.com"}

    job = Jobs.Job()
    job.env = {"API_ENDPOINT": "http://another-unsecure-url.com"}

    step = Steps.Step()
    step.run = "curl http://yet-another-unsecure-url.com"
    step.env = {"SERVICE_URL": "http://service-url.com"}

    job.steps.append(step)
    workflow.jobs = {"build": job}

    return workflow


def test_unsecure_protocol_detection(workflow):
    logging.debug(f"Running test_unsecure_protocol_detection with workflow: {workflow}")
    factory = UnsecureProtocolFct(content=workflow)
    findings = factory.detect()
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        "Unsecure protocol found in workflow env 'API_URL': http://unsecure-url.com. "
        "Try use HTTPS instead of HTTP. If you need to use HTTP, please provide certain level of security.",
        "Unsecure protocol found in job build env 'API_ENDPOINT': http://another-unsecure-url.com. "
        "Try use HTTPS instead of HTTP. If you need to use HTTP, please provide certain level of security.",
        "Unsecure protocol found in step in job build env 'SERVICE_URL': http://service-url.com. "
        "Try use HTTPS instead of HTTP. If you need to use HTTP, please provide certain level of security.",
        "Unsecure protocol found in step in job build run command 'curl http://yet-another-unsecure-url.com'. "
        "Try use HTTPS instead of HTTP. If you need to use HTTP, please provide certain level of security."
    ]

    assert findings == expected_findings


def test_integration():
    logging.debug("Running test_integration")
    action = Action(file_path="../../Yamls/Smells/UnsecureProtocol.yaml")
    workflow = action.prepare_for_analysis()
    logging.debug(f"Parsed workflow: {workflow}")

    factory = UnsecureProtocolFct(content=workflow)
    findings = factory.detect()
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        "Unsecure protocol found in workflow env 'API_URL': http://unsecure-url.com. "
        "Try use HTTPS instead of HTTP. If you need to use HTTP, please provide certain level of security.",
        "Unsecure protocol found in job build env 'API_ENDPOINT': http://another-unsecure-url.com. "
        "Try use HTTPS instead of HTTP. If you need to use HTTP, please provide certain level of security.",
        "Unsecure protocol found in step in job build env 'SERVICE_URL': http://service-url.com. "
        "Try use HTTPS instead of HTTP. If you need to use HTTP, please provide certain level of security.",
        "Unsecure protocol found in step in job build run command 'curl http://yet-another-unsecure-url.com'. "
        "Try use HTTPS instead of HTTP. If you need to use HTTP, please provide certain level of security."
    ]

    assert findings == expected_findings
