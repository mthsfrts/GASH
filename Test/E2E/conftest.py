"""
E2E Test Configuration and Shared Fixtures
Handles mock tokens, temp directories, and docker setup.
"""
import os
import sys
import pytest
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from Test.E2E.helpers.repo_fetcher import fetch_repo_workflows


# ============================================================
# TOKEN HANDLING FIXTURES (Mock + Environment Variable)
# ============================================================

@pytest.fixture(scope="session")
def mock_token():
    """
    Mock token for local tests that don't require real API access.
    Used for detector tests that only parse local YAML files.
    """
    return "mock_github_token_for_testing"


@pytest.fixture(scope="session")
def real_token():
    """
    Real token from environment variable for CI tests.
    Falls back to skip if not available.
    """
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if not token:
        pytest.skip("Real GitHub token not available, skipping API-dependent test")
    return token


@pytest.fixture
def mock_token_env(mock_token, tmp_path):
    """
    Environment with mocked token configuration.
    Creates temporary config file to avoid interactive prompts.
    """
    config_dir = tmp_path / ".gash"
    config_dir.mkdir()
    config_file = config_dir / "config.ini"
    config_file.write_text(f"[github]\ntoken = {mock_token}\n")

    env = dict(os.environ)
    env['HOME'] = str(tmp_path)
    env['GASH_TEST_MODE'] = 'true'

    return env


@pytest.fixture
def ci_token_env(real_token):
    """
    Environment with real token for CI pipeline tests.
    Uses GITHUB_TOKEN environment variable.
    """
    env = dict(os.environ)
    env['GITHUB_TOKEN'] = real_token
    return env


# ============================================================
# MOCK GITHUB API FIXTURES
# ============================================================

@pytest.fixture
def mock_github_api():
    """
    Mocked GitHub API for UntrustedDependencies detector.
    Returns verified status for all actions.
    """
    with patch('APIs.GitHub.GitHubAPI') as mock_api:
        mock_instance = MagicMock()
        mock_instance.get_rate_limit.return_value = 200
        mock_instance.fetch_action_verification.return_value = (True, True)
        mock_instance.get_repository_vulnerabilities.return_value = None
        mock_api.return_value = mock_instance
        yield mock_instance


# ============================================================
# PATH FIXTURES
# ============================================================

@pytest.fixture(scope="session")
def project_root():
    """Project root directory."""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def fixtures_path():
    """Path to E2E test fixtures."""
    return Path(__file__).parent / "fixtures" / "workflows"


@pytest.fixture(scope="session")
def scalability_fixtures_path():
    """Path to scalability test fixtures (50+ workflows)."""
    return Path(__file__).parent / "fixtures" / "workflows" / "scalability"


@pytest.fixture(scope="session")
def real_repos_path():
    """Path to real repository workflows."""
    return Path(__file__).parent / "fixtures" / "real_repos"


# ============================================================
# REAL REPOSITORY FIXTURES (Cloned at runtime)
# ============================================================

@pytest.fixture(scope="session")
def starter_workflows_path(tmp_path_factory):
    """
    Clone actions/starter-workflows for golden master tests.
    Used in Scenario 1 to verify no false positives.
    """
    return fetch_repo_workflows("actions/starter-workflows", tmp_path_factory)


@pytest.fixture(scope="session")
def juice_shop_workflows_path(tmp_path_factory):
    """
    Clone juice-shop/juice-shop for security smell tests.
    OWASP intentionally vulnerable project.
    Used in Scenario 2 for security smell validation.
    """
    return fetch_repo_workflows("juice-shop/juice-shop", tmp_path_factory)


# ============================================================
# TEMPORARY DIRECTORY FIXTURES
# ============================================================

@pytest.fixture
def temp_workflow_dir(tmp_path):
    """
    Temporary directory for workflow files during tests.
    Automatically cleaned up after test.
    """
    workflow_dir = tmp_path / "workflows"
    workflow_dir.mkdir()
    yield workflow_dir


@pytest.fixture
def temp_output_dir(tmp_path):
    """
    Temporary directory for GASH output files.
    """
    output_dir = tmp_path / "GashAnalyses"
    output_dir.mkdir()
    yield output_dir


# ============================================================
# UTILITY FIXTURES
# ============================================================

@pytest.fixture
def copy_fixture_to_temp(fixtures_path, tmp_path):
    """
    Factory fixture to copy specific fixtures to temp directory.
    """
    def _copy(fixture_name):
        src = fixtures_path / fixture_name
        dst = tmp_path / fixture_name
        shutil.copy(src, dst)
        return dst
    return _copy


@pytest.fixture(autouse=True)
def cleanup_gash_artifacts(tmp_path):
    """
    Ensure clean state before and after each test.
    """
    yield
    # Cleanup any temporary config files
    config_dir = tmp_path / ".gash"
    if config_dir.exists():
        shutil.rmtree(config_dir)
    # Cleanup GashAnalyses if created
    gash_output = tmp_path / "GashAnalyses"
    if gash_output.exists():
        shutil.rmtree(gash_output)


# ============================================================
# DOCKER FIXTURES (pytest-docker)
# ============================================================

@pytest.fixture(scope="session")
def docker_compose_file():
    """Path to docker-compose.yml for pytest-docker."""
    return str(Path(__file__).parent / "docker-compose.yml")


@pytest.fixture(scope="session")
def docker_compose_project_name():
    """Unique project name for test isolation."""
    return "gash_e2e_tests"


# ============================================================
# PYTEST MARKERS
# ============================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "requires_real_token: mark test as requiring real GitHub token"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow (performance tests)"
    )
    config.addinivalue_line(
        "markers", "docker: mark test as requiring Docker"
    )
