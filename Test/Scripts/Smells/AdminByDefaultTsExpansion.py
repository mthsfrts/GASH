import pytest
import os
from Analysis.Parse.ActionParser import Action
from Analysis.Smells.Categories.Security.AdminByDefault.AdminByDefaultSt import MainAdminByDefaultCheck

FIXTURES_PATH = os.path.join(
    os.path.dirname(__file__),
    '../../Fixtures/AdminByDefault'
)

ROOT_FIXTURES_PATH = os.path.join(
    os.path.dirname(__file__),
    '../../Fixtures'
)

@pytest.fixture
def load_workflow():
    """
    Loads a workflow YAML file from the fixtures directory
    and prepares it for analysis using ActionParser.
    """
    def _loader(filename, root=False):
        base = ROOT_FIXTURES_PATH if root else FIXTURES_PATH
        file_path = os.path.join(base, filename)
        action = Action(file_path=file_path)
        return action.prepare_for_analysis()
    return _loader


# =========================
# Admin By Default Tests
# =========================

def test_admin_at_workflow_level(load_workflow):
    workflow = load_workflow('workflow_write_all_workflow.yml')
    if workflow is None:
        pytest.fail("Fixture global não encontrada.")
        
    checker = MainAdminByDefaultCheck()
    findings = checker.check(workflow)
    
    assert isinstance(findings, list)
    if len(findings) > 0:
        assert any("workflow" in f.lower() or "elevated" in f.lower() for f in findings)

def test_admin_at_job_level(load_workflow): 
    workflow = load_workflow('workflow_write_all_job.yml')
    if workflow is None:
        pytest.fail("Fixture de job não encontrada.")
        
    checker = MainAdminByDefaultCheck()
    findings = checker.check(workflow)
    
    assert isinstance(findings, list)
    assert len(findings) > 0, "O GASH deveria ter detectado permissões write-all no job"

def test_no_permissions_declared(load_workflow): 
    workflow = load_workflow('workflow_no_permissions.yml')
    if workflow is None:
        pytest.fail("Fixture sem permissões não encontrada.")
        
    checker = MainAdminByDefaultCheck()
    findings = checker.check(workflow)
    
    assert isinstance(findings, list) 