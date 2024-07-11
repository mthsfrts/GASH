import pytest
import logging
from Analysis.DataStruct import Workflow, Jobs, Steps
from Analysis.Parse.ActionParser import Action
from Analysis.Smells.Categories.Maintenance.CodeReplica.CodeReplicaFct import CodeReplicaFct
from Analysis.Smells.Categories.Maintenance.CodeReplica.CodeReplicaSt import MainCodeReplicaCheck

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def workflow():
    workflow = Workflow.Workflow()
    workflow.env = {"VAR1": "value1", "VAR2": "value1", "VAR3": "value2", "VAR4": "value1"}

    job = Jobs.Job()
    job.env = {"VAR1": "value1", "VAR2": "value1", "VAR3": "value2", "VAR4": "value1"}

    step = Steps.Step()
    step.name = "step1"
    step.run = "echo 'Hello'"
    step.env = {"VAR5": "value2", "VAR6": "value4"}
    step.with_params = {"param1": "value2", "param2": "value1"}

    job.steps.append(step)
    workflow.jobs = {"build": job, "test": job}

    return workflow


def test_unit(workflow):
    logging.debug(f"Running test_find_duplicated_values with workflow: {workflow}")
    checker = MainCodeReplicaCheck(threshold=2)
    findings = checker.check(workflow)
    logging.debug(f"Findings: {findings}")

    expected_findings = ["Job 'test' is replicated with job 'build'. Consider use reusable actions. "
                         "You can find examples in the documentation: "
                         "https://docs.github.com/en/actions/using-workflows/reusing-workflows",

                         "Value 'value1' is replicated in contexts: Job 'build' env variable 'VAR1', "
                         "Job 'build' env variable 'VAR2'. If not an Env consider use Matrix to define "
                         "versions. Ex: 'strategy: matrix: {'python': ['3.6', '3.7', '3.8']}'",

                         "Value 'value2' is replicated in contexts: Job 'build' env variable 'VAR3', "
                         "Step 'step1' env variable 'VAR5' in job 'build' is replicated. Consider use "
                         "Global Env variables: Ex: Env: 'VAR5': 'value2'. If not an Env consider use "
                         "Matrix to define versions. Ex: 'strategy: matrix: {'python': ['3.6', '3.7', "
                         "'3.8']}'",

                         "Value 'value4' is replicated in contexts: Step 'step1' env variable 'VAR6' "
                         "in job 'build' is replicated. Consider use Global Env variables: Ex: Env: "
                         "'VAR6': 'value4', Step 'step1' env variable 'VAR6' in job 'test' is "
                         "replicated. Consider use Global Env variables: Ex: Env: 'VAR6': 'value4'. If "
                         "not an Env consider use Matrix to define versions. Ex: 'strategy: matrix: "
                         "{'python': ['3.6', '3.7', '3.8']}'"]

    assert sorted(findings) == sorted(expected_findings)


def test_integration():
    logging.debug("Running test_integration")
    action = Action(file_path='../../Yamls/Smells/Prisma/release-latest.yml')
    workflow = action.prepare_for_analysis()
    factory = CodeReplicaFct(content=workflow)
    findings = factory.detect()

    expected_findings = [
        "Value '${{ secrets.BOT_TOKEN }}' is replicated in contexts: Step 'Publish "
        "all packages to npm' env variable 'GITHUB_TOKEN' in job 'release' is "
        "replicated. Consider use Global Env variables: Ex: Env: 'GITHUB_TOKEN': '${{ "
        "secrets.BOT_TOKEN }}', Step 'Create a tag on prisma-engines repository' "
        "parameter 'github-token' in job 'release' is replicated. Consider use "
        "Defaults params. Ex: Defaults: 'github-token': '${{ secrets.BOT_TOKEN }}'. "
        "If not an Env consider use Matrix to define versions. Ex: 'strategy: matrix: "
        "{'python': ['3.6', '3.7', '3.8']}'",
        "Value '${{ secrets.SLACK_RELEASE_FEED_WEBHOOK }}' is replicated in contexts: "
        "Step 'Publish all packages to npm' env variable 'SLACK_RELEASE_FEED_WEBHOOK' "
        "in job 'release' is replicated. Consider use Global Env variables: Ex: Env: "
        "'SLACK_RELEASE_FEED_WEBHOOK': '${{ secrets.SLACK_RELEASE_FEED_WEBHOOK }}', "
        "Step 'Slack Notification on Success' env variable 'SLACK_WEBHOOK' in job "
        "'success' is replicated. Consider use Global Env variables: Ex: Env: "
        "'SLACK_WEBHOOK': '${{ secrets.SLACK_RELEASE_FEED_WEBHOOK }}'. If not an Env "
        "consider use Matrix to define versions. Ex: 'strategy: matrix: {'python': "
        "['3.6', '3.7', '3.8']}'",
        "Value 'true' is replicated in contexts: Step 'Publish all packages to npm' "
        "env variable 'BUILDKITE' in job 'release' is replicated. Consider use Global "
        "Env variables: Ex: Env: 'BUILDKITE': 'true', Step 'Publish all packages to "
        "npm' env variable 'NPM_CONFIG_PROVENANCE' in job 'release' is replicated. "
        "Consider use Global Env variables: Ex: Env: 'NPM_CONFIG_PROVENANCE': 'true'. "
        "If not an Env consider use Matrix to define versions. Ex: 'strategy: matrix: "
        "{'python': ['3.6', '3.7', '3.8']}'"]

    assert sorted(findings) == sorted(expected_findings)
