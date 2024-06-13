import pytest
from Analysis.DataStruct import Jobs, Steps, Workflow, Smells


def test_job_initialization():
    job = Jobs.Job()
    job.name = "test_job"
    job.runs_on = "ubuntu-latest"
    assert job.name == "test_job"
    assert job.runs_on == "ubuntu-latest"
    assert job.steps == []
    assert job.env == {}
    assert job._if is None
    assert job.concurrency is None
    assert job.container is None
    assert job.continue_on_error is None
    assert job.defaults == {}
    assert job.outputs == {}
    assert job.permissions == {}
    assert job.services == {}
    assert job.strategy == {}
    assert job.secrets == {}
    assert job.timeout_minutes is None
    assert job.needs == []
    assert job.uses is None
    assert job.with_params == {}


def test_step_initialization():
    step = Steps.Step()
    step.name = "Checkout code"
    step.uses = "actions/checkout@v2"
    assert step.name == "Checkout code"
    assert step.uses == "actions/checkout@v2"
    assert step.run is None
    assert step.working_directory is None
    assert step.env == {}
    assert step._if is None
    assert step.continue_on_error is None
    assert step.timeout_minutes is None
    assert step.with_params == {}


def test_workflow_initialization():
    workflow = Workflow.Workflow()
    workflow.name = "Test Workflow"
    workflow.env = {"VAR": "value"}
    assert workflow.name == "Test Workflow"
    assert workflow.env == {"VAR": "value"}
    assert workflow.on == {}
    assert workflow.jobs == {}
    assert workflow.concurrency is None
    assert workflow.permissions == {}
    assert workflow.defaults == {}


def test_smells_initialization():
    smell = Smells.Smells(
        category="Security",
        name="Hardcoded Secret",
        description="Secrets should not be hardcoded.",
        strategy="Search for hardcoded secrets.",
        mitigation="Use environment variables for secrets.",
        severity_level="High",
        severity_justification="Hardcoded secrets can be easily exposed."
    )
    assert smell.category == "Security"
    assert smell.name == "Hardcoded Secret"
    assert smell.description == "Secrets should not be hardcoded."
    assert smell.strategy == "Search for hardcoded secrets."
    assert smell.mitigation == "Use environment variables for secrets."
    assert smell.severity_level == "High"
    assert smell.severity_justification == "Hardcoded secrets can be easily exposed."
    assert str(smell) == ("Category: Security\n"
                          "Name: Hardcoded Secret\n"
                          "Description: Secrets should not be hardcoded.\n"
                          "Strategy: Search for hardcoded secrets.\n"
                          "Mitigation: Use environment variables for secrets.\n"
                          "Severity Level: High\n"
                          "Severity Justification: Hardcoded secrets can be easily exposed.")


def test_create_smells_from_dict():
    severities = {
        "Categories": {
            "Security": {
                "Smells": {
                    "Hardcoded Secret": {
                        "Description": "Secrets should not be hardcoded.",
                        "Strategy": "Search for hardcoded secrets.",
                        "Mitigation": "Use environment variables for secrets.",
                        "Vulnerability": {
                            "Level": "High",
                            "Justification": "Hardcoded secrets can be easily exposed."
                        }
                    }
                }
            }
        }
    }

    smells_list = Smells.create_smells_from_dict(severities)

    assert len(smells_list) == 1
    smell = smells_list[0]
    assert smell.category == "Security"
    assert smell.name == "Hardcoded Secret"
    assert smell.description == "Secrets should not be hardcoded."
    assert smell.strategy == "Search for hardcoded secrets."
    assert smell.mitigation == "Use environment variables for secrets."
    assert smell.severity_level == "High"
    assert smell.severity_justification == "Hardcoded secrets can be easily exposed."