import pytest
import logging
from Analysis.Smells.Categories.Security.AdminByDefault.AdminByDefaultFct import AdminByDefaultFct
from Analysis.Smells.Categories.Security.AdminByDefault.AdminByDefaultSt import MainAdminByDefaultCheck
from Analysis.Parse.ActionParser import Action
from Analysis.DataStruct import Workflow, Jobs

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def workflow():
    workflow = Workflow.Workflow()
    workflow.permissions = {"contents": "write"}

    job = Jobs.Job()
    job.permissions = {"actions": "write-all"}

    workflow.jobs = {"build": job}

    return workflow


def test_admin_by_default_detection(workflow):
    factory = MainAdminByDefaultCheck()
    findings = factory.check(workflow)

    expected_findings = [
        'Elevate permission found at job build: actions = write-all. Review the '
        'permission and check if the user is qualified for that. Use the least '
        'privilege principle.']

    assert findings == expected_findings


def test_integration():
    action = Action(file_path="AdminByDefault.yaml")
    workflow_ = action.prepare_for_analysis()

    factory = AdminByDefaultFct(content=workflow_)
    findings = factory.detect()

    expected_findings = ['Elevate permission found at job build: actions = write-all. Review the '
                         'permission and check if the user is qualified for that. Use the least '
                         'privilege principle.']

    assert findings == expected_findings
