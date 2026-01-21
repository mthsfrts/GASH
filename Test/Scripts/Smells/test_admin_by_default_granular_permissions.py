import pytest

from Analysis.Smells.Categories.Security.AdminByDefault.AdminByDefaultSt import (
    MainAdminByDefaultCheck
)
from Analysis.DataStruct import Workflow, Jobs


@pytest.fixture
def workflow_with_granular_permissions():
    """
    Cria um workflow com permissões estritamente read-only.

    Este workflow NÃO deve ser sinalizado como Admin By Default,
    de acordo com a lógica atual do detector.
    """
    workflow = Workflow.Workflow()
    workflow.permissions = {
        "contents": "read"
    }

    job = Jobs.Job()
    job.permissions = {
        "contents": "read"
    }

    workflow.jobs = {
        "build": job
    }

    return workflow


def test_admin_by_default_with_granular_permissions_should_not_detect(
    workflow_with_granular_permissions
):
    """
    Arrange:
        Workflow com permissões granulares.

    Act:
        Executa o detector MainAdminByDefaultCheck.

    Assert:
        Nenhum finding deve ser retornado.
    """
    checker = MainAdminByDefaultCheck()

    findings = checker.check(workflow_with_granular_permissions)

    assert findings == [], (
        "Detector Admin By Default gerou falso positivo "
        "para permissões granulares corretamente configuradas."
    )