import pytest
from Analysis.Parse.ActionParser import Action


@pytest.fixture
def yaml_content():
    return """
    name: DataStruct Workflow
    on:
      push:
        branches:
          - main
    env:
      GLOBAL_VAR: global_value
    jobs:
      test_job:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout code
            uses: actions/checkout@v2
          - name: Run tests
            run: pytest
    """


@pytest.fixture
def action(yaml_content):
    return Action(content=yaml_content)


def test_parse_yaml(action):
    raw_data = action.parse_yaml()
    assert raw_data is not None
    assert raw_data['name'] == 'DataStruct Workflow'


def test_populate_workflow(action):
    raw_data = action.parse_yaml()
    workflow = action.populate_workflow(raw_data)
    assert workflow.name == 'DataStruct Workflow'
    assert 'test_job' in workflow.jobs


def test_populate_job(action):
    raw_data = action.parse_yaml()
    job_data = raw_data['jobs']['test_job']
    job = action.populate_job('test_job', job_data)
    assert job.name == 'test_job'
    assert job.runs_on == 'ubuntu-latest'
    assert len(job.steps) == 2


def test_populate_step(action):
    raw_data = action.parse_yaml()
    step_data = raw_data['jobs']['test_job']['steps'][0]
    step = action.populate_step(step_data)
    assert step.name == 'Checkout code'
    assert step.uses == 'actions/checkout@v2'
