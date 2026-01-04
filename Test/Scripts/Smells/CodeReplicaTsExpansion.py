import pytest
import os
from Analysis.Parse.ActionParser import Action
from Analysis.Smells.Categories.Maintenance.CodeReplica.CodeReplicaSt import MainCodeReplicaCheck

FIXTURES_PATH = os.path.join(
    os.path.dirname(__file__),
    '../../Fixtures/CodeReplica'
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
# Code Replica Tests
# =========================

# Detect duplicated code across multiple jobs
# Expected result: smell detected
def test_detects_duplicate_code_across_jobs(load_workflow):
    workflow = load_workflow('code_replica_duplicate_jobs.yml')
    checker = MainCodeReplicaCheck()
    findings = checker.check(workflow)

    assert len(findings) > 0

# Workflow with unique code
# Expected result: NO smell detected
def test_unique_code_passes(load_workflow):
    workflow = load_workflow('code_replica_unique.yml')
    checker = MainCodeReplicaCheck()
    findings = checker.check(workflow)

    assert len(findings) == 0
