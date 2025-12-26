import pytest
import os
from Analysis.Parse.ActionParser import Action
from Analysis.Smells.Categories.Quality.LongBlocks.LongBlockSt import MainLongBlockCheck

FIXTURES_PATH = os.path.join(os.path.dirname(__file__), '../../Fixtures/LongBlock')

@pytest.fixture
def load_workflow():
    def _loader(filename):
        file_path = os.path.join(FIXTURES_PATH, filename)
        action = Action(file_path=file_path)
        return action.prepare_for_analysis()
    return _loader


# Testa se o detector identifica jobs com muitos passos. Resultado esperado: erro encontrado.
def test_detects_too_many_steps(load_workflow):
    workflow = load_workflow('test_manysteps.yml')
    checker = MainLongBlockCheck()
    findings = checker.long_block_check(workflow)

    assert any("steps" in f for f in findings)


# Testa se o detector identifica scripts longos. Resultado esperado: erro encontrado.
def test_detects_long_scripts(load_workflow):
    workflow = load_workflow('test_longscript.yml')
    checker = MainLongBlockCheck()
    findings = checker.long_block_check(workflow)
    
    assert len(findings) > 0


# Testa um arquivo que segue as boas práticas. Resultado esperado: NENHUM erro encontrado.
def test_negative_scenario_clean_workflow(load_workflow):
    workflow = load_workflow('test_clean.yml')
    checker = MainLongBlockCheck()
    findings = checker.long_block_check(workflow)
    
    assert len(findings) == 0


# Testa se o detector reclama de workflows com jobs excessivos. Resultado esperado: erro encontrado.
def test_detects_too_many_jobs(load_workflow):
    workflow = load_workflow('test_manyjobs.yml')
    checker = MainLongBlockCheck()
    findings = checker.long_block_check(workflow)
    
    assert any("jobs" in f for f in findings)


# Testa um script que não é nem curto demais, nem longo demais. Resultado esperado: NENHUM erro encontrado.
def test_borderline_script_passes(load_workflow):
    workflow = load_workflow('test_medioscript.yml')
    checker = MainLongBlockCheck()
    findings = checker.long_block_check(workflow)
    
    assert len(findings) == 0