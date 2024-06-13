import pytest
import logging
from unittest.mock import patch
from Analysis.Smells.Categories.Security.UntrustedDependencies.UntrustedDependenciesFct import UntrustedDependenciesFct
from Analysis.DataStruct import Workflow, Jobs, Steps
from Analysis.Parse.ActionParser import Action

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def workflow():
    workflow = Workflow.Workflow()
    job = Jobs.Job()

    step1 = Steps.Step()
    step1.uses = "actions/checkout@v4"

    step2 = Steps.Step()
    step2.uses = "rhysd/github-action-benchmark@v1"

    step3 = Steps.Step()
    step3.uses = "CodSpeedHQ/action@v2"

    step4 = Steps.Step()
    step4.uses = "rtCamp/action-slack-notify@v2.3.0"

    job.steps = [step1, step2, step3, step4]
    workflow.jobs = {"benchmark": job}

    return workflow


def mock_get_repository_vulnerabilities(owner, repo):
    if owner == "CodSpeedHQ" and repo == "action":
        return {
            "ghsa_id": "GHSA-7f32-hm4h-w77q",
            "cve_id": "CVE-2022-39321",
            "summary": "Example vulnerability",
            "description": "This is a mock vulnerability description.",
            "severity": "high",
            "identifiers": [
                {"value": "GHSA-7f32-hm4h-w77q", "type": "GHSA"},
                {"value": "CVE-2022-39321", "type": "CVE"}
            ],
            "state": "published",
            "published_at": "2022-10-24T16:00:18Z",
            "updated_at": "2022-10-24T16:00:18Z"
        }
    return None


@patch('Mining.Mining.Mining.get_repository_vulnerabilities', side_effect=mock_get_repository_vulnerabilities)
def test_untrusted_dependencies_detection(mock_get_vulns, workflow):
    logging.debug(f"Running test_untrusted_dependencies_detection with workflow: {workflow}")
    factory = UntrustedDependenciesFct(content=workflow)
    findings = factory.detect()
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        'Unverified dependency found in step in job benchmark: actions/checkout@v4. '
        'Consider using actions from verified creators.',
        'Unverified dependency found in step in job benchmark: '
        'rhysd/github-action-benchmark@v1. Consider using actions from verified '
        'creators.',
        'Unverified dependency found in step in job benchmark: CodSpeedHQ/action@v2. '
        'Consider using actions from verified creators.',
        'Vulnerabilities found in step in job benchmark: CodSpeedHQ/action@v2. '
        "Details: {'ghsa_id': 'GHSA-7f32-hm4h-w77q', 'cve_id': 'CVE-2022-39321', "
        "'summary': 'Example vulnerability', 'description': 'This is a mock "
        "vulnerability description.', 'severity': 'high', 'identifiers': [{'value': "
        "'GHSA-7f32-hm4h-w77q', 'type': 'GHSA'}, {'value': 'CVE-2022-39321', 'type': "
        "'CVE'}], 'state': 'published', 'published_at': '2022-10-24T16:00:18Z', "
        "'updated_at': '2022-10-24T16:00:18Z'}",
        'Unverified dependency found in step in job benchmark: '
        'rtCamp/action-slack-notify@v2.3.0. Consider using actions from verified '
        'creators.'
    ]

    assert findings == expected_findings


@patch('Mining.Mining.Mining.get_repository_vulnerabilities', side_effect=mock_get_repository_vulnerabilities)
def test_integration(mock_get_vulns):
    logging.debug("Running test_integration")
    action = Action(file_path="UntrustedDependencies.yaml")
    workflow_file = action.prepare_for_analysis()
    logging.debug(f"Parsed workflow: {workflow_file}")

    factory = UntrustedDependenciesFct(content=workflow_file)
    findings = factory.detect()
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        'Unverified dependency found in step in job benchmark: actions/checkout@v4. '
        'Consider using actions from verified creators.',
        'Unverified dependency found in step in job benchmark: '
        'rhysd/github-action-benchmark@v1. Consider using actions from verified '
        'creators.',
        'Unverified dependency found in step in job benchmark: CodSpeedHQ/action@v2. '
        'Consider using actions from verified creators.',
        'Vulnerabilities found in step in job benchmark: CodSpeedHQ/action@v2. '
        "Details: {'ghsa_id': 'GHSA-7f32-hm4h-w77q', 'cve_id': 'CVE-2022-39321', "
        "'summary': 'Example vulnerability', 'description': 'This is a mock "
        "vulnerability description.', 'severity': 'high', 'identifiers': [{'value': "
        "'GHSA-7f32-hm4h-w77q', 'type': 'GHSA'}, {'value': 'CVE-2022-39321', 'type': "
        "'CVE'}], 'state': 'published', 'published_at': '2022-10-24T16:00:18Z', "
        "'updated_at': '2022-10-24T16:00:18Z'}",
        'Unverified dependency found in step in job benchmark: '
        'rtCamp/action-slack-notify@v2.3.0. Consider using actions from verified '
        'creators.'
    ]

    assert findings == expected_findings
