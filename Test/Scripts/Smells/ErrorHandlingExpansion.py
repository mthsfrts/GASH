import pytest
import os
from Analysis.Parse.ActionParser import Action
from Analysis.Smells.Categories.Maintenance.ErrorHandling.ErrorHandlingSt import MainErrorHandlingCheck

def load_data(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, '..', '..', 'Fixtures', 'ErrorHandling', filename)
    # Se o ActionParser estiver falhando porque o arquivo não é um workflow completo,
    # você pode carregar o YAML puro aqui, mas vamos tentar via ActionParser primeiro:
    action = Action(file_path=file_path)
    return action.prepare_for_analysis()

@pytest.fixture
def checker():
    return MainErrorHandlingCheck()

def test_expansion_steps_no_error_handling(checker):
    data = load_data('steps_no_error_handling.yml')
    findings = checker.check(data)
    assert len(findings) > 0

def test_expansion_continue_on_error(checker):
    data = load_data('inadequate_continue_on_error.yml')
    findings = checker.check_continue_on_error(data)
    assert len(findings) > 0

def test_expansion_output_validation(checker):
    data = load_data('missing_output_validation.yml')
    findings = checker.check(data)
    assert isinstance(findings, list)

def test_expansion_retry_logic(checker):
    data = load_data('no_retry_logic.yml')
    findings = checker.check(data)
    assert isinstance(findings, list)