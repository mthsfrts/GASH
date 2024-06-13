import pytest
import logging
from Analysis.Smells.Categories.Security.SecurityFlaws.SecurityFlawsFct import SecurityFlawsFct
from Analysis.DataStruct import Workflow, Jobs
from Analysis.Parse.ActionParser import Action

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def workflow():
    workflow = Workflow.Workflow()
    workflow.permissions = {"contents": "write-all"}

    job = Jobs.Job()
    job.permissions = {"actions": "write"}

    workflow.jobs = {"build": job}

    return workflow


def test_security_flaws_detection(workflow):
    logging.debug(f"Running test_security_flaws_detection with workflow: {workflow}")
    factory = SecurityFlawsFct(content=workflow)
    findings = factory.detect()
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        "Permissions found in workflow: {'contents': 'write-all'}, a top level may harm your pipeline."
        " Make sure to grant the right level for GitHub Token permissions.",
        "Permissions found in job build: {'actions': 'write'}. "
        "Make sure to grant the right level for GitHub Token permissions."
    ]

    assert findings == expected_findings


def test_integration():
    logging.debug("Running test_integration")
    action = Action(file_path="SecurityFlaws.yaml")
    workflow_file = action.prepare_for_analysis()
    logging.debug(f"Parsed workflow: {workflow_file}")

    factory = SecurityFlawsFct(content=workflow_file)
    findings = factory.detect()
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        "Permissions found in workflow: {'contents': 'write-all'}, a top level may harm your pipeline."
        " Make sure to grant the right level for GitHub Token permissions.",
        "Permissions found in job build: {'actions': 'write'}. "
        "Make sure to grant the right level for GitHub Token permissions."
    ]

    assert findings == expected_findings
