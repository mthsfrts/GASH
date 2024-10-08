import pytest
import logging
from Analysis.Smells.Categories.Security.HardCoded.HardCodedFct import HardCodedFct
from Analysis.DataStruct import Workflow, Jobs, Steps
from Analysis.Parse.ActionParser import Action

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def workflow():
    workflow = Workflow.Workflow()
    workflow.env = {"API_KEY": "my_secret_key"}

    job = Jobs.Job()
    job.env = {"DB_PASSWORD": "super_secret_password"}

    step = Steps.Step()
    step.run = "echo 'my_secret_key'"
    step.env = {"TOKEN": "another_secret_token"}

    job.steps.append(step)
    workflow.jobs = {"build": job}

    return workflow


def test_hard_coded_secret_detection(workflow):
    logging.debug(f"Running test_hard_coded_secret_detection with workflow: {workflow}")
    factory = HardCodedFct(content=workflow)
    findings = factory.detect()
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        "Hard-coded secret in workflow env 'API_KEY'",
        "Hard-coded secret in job build env 'DB_PASSWORD'",
        "Hard-coded secret in step in job build env 'TOKEN'",
        "Hard-coded secret in step in job build run command 'echo 'my_secret_key''"
    ]

    assert findings == expected_findings


def test_integration():
    logging.debug("Running test_integration")
    action = Action(file_path="../../Yamls/Smells/Prisma/manage-dist-tag.yml")
    workflow = action.prepare_for_analysis()
    logging.debug(f"Parsed workflow: {workflow}")

    factory = HardCodedFct(content=workflow)
    findings = factory.detect()
    logging.debug(f"Findings: {findings}")

    expected_findings = [
        "Hard-coded secret in step in job manage_tag run command 'echo "
        '"//registry.npmjs.org/:_authToken=${NODE_AUTH_TOKEN}" > ~/.npmrc\n'
        '\n'
        'echo "The following commands will be executed, for example:"\n'
        'echo "npm dist-tag \'${{ env.ACTION }}\' \'@prisma/client${{ env.VERSION '
        '}}\' \'${{ env.TAG_NAME }}\'"\n'
        '\n'
        'sleep 10\n'
        '\n'
        'npm dist-tag "${{ env.ACTION }}" "@prisma/client${{ env.VERSION }}" "${{ '
        'env.TAG_NAME }}"\n'
        'npm dist-tag "${{ env.ACTION }}" "prisma${{ env.VERSION }}" "${{ '
        'env.TAG_NAME }}"\n'
        '\n'
        'npm dist-tag "${{ env.ACTION }}" "@prisma/adapter-d1${{ env.VERSION }}" "${{ '
        'env.TAG_NAME }}"\n'
        "'"
    ]

    assert findings == expected_findings
