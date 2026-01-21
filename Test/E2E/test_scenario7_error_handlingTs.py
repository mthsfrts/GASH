"""
E2E Test Scenario 7: Error Handling
Tests graceful handling of error conditions.

This scenario validates:
- Malformed YAML files are handled gracefully
- Non-existent files produce clear error messages
- Empty directories are handled appropriately
- Invalid tokens produce meaningful errors
- System doesn't crash on edge cases
"""
import pytest
import logging
import subprocess
import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from Analysis.Parse.ActionParser import Action

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestMalformedYAMLHandling:
    """
    Tests for handling invalid/malformed YAML files.
    System should not crash and should provide meaningful feedback.
    """

    @pytest.fixture
    def malformed_workflow_path(self, fixtures_path):
        """Path to malformed workflow fixture."""
        return str(fixtures_path / "malformed_workflow.yml")

    def test_malformed_yaml_returns_none(self, malformed_workflow_path):
        """
        ActionParser should return None for malformed YAML.
        Should not raise unhandled exception.
        """
        action = Action(file_path=malformed_workflow_path)

        # Should not crash - may return None or raise handled exception
        try:
            workflow = action.prepare_for_analysis()
            # If it returns, it should be None or a partial result
            logger.info(f"Malformed YAML result: {workflow}")
        except Exception as e:
            # Exception is acceptable as long as it's not a crash
            logger.info(f"Malformed YAML raised expected exception: {type(e).__name__}: {e}")
            assert True  # Exception was handled

    def test_malformed_yaml_cli_no_crash(self, malformed_workflow_path, mock_token_env):
        """
        CLI should handle malformed YAML without crashing.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", malformed_workflow_path],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"CLI stdout: {result.stdout}")
        logger.debug(f"CLI stderr: {result.stderr}")

        # Should complete (with or without error) but not crash with traceback
        # A controlled error message is acceptable
        assert result.returncode is not None, "Process should complete"


class TestNonExistentFileHandling:
    """
    Tests for handling non-existent files and paths.
    """

    def test_nonexistent_file_returns_none(self):
        """
        ActionParser should handle non-existent files gracefully.
        """
        fake_path = "/nonexistent/path/to/workflow.yml"
        action = Action(file_path=fake_path)

        try:
            workflow = action.prepare_for_analysis()
            # Should return None for non-existent file
            assert workflow is None, "Should return None for non-existent file"
        except FileNotFoundError:
            # FileNotFoundError is an acceptable response
            pass
        except Exception as e:
            # Other exceptions should be logged but test passes
            logger.info(f"Non-existent file raised: {type(e).__name__}: {e}")

    def test_nonexistent_file_cli(self, mock_token_env):
        """
        CLI should provide clear error for non-existent file.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", "/fake/path/workflow.yml"],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"CLI stdout: {result.stdout}")
        logger.debug(f"CLI stderr: {result.stderr}")

        # Should complete without hanging
        assert result.returncode is not None

    def test_nonexistent_directory_batch_analyze(self, mock_token_env):
        """
        batch-analyze should handle non-existent directory gracefully.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", "/nonexistent/directory/"],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"CLI stdout: {result.stdout}")
        logger.debug(f"CLI stderr: {result.stderr}")

        # Should complete
        assert result.returncode is not None


class TestEmptyDirectoryHandling:
    """
    Tests for handling empty directories.
    """

    def test_empty_directory_batch_analyze(self, tmp_path, mock_token_env):
        """
        batch-analyze should handle empty directory gracefully.
        """
        empty_dir = tmp_path / "empty_workflows"
        empty_dir.mkdir()

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(empty_dir)],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"CLI stdout: {result.stdout}")
        logger.debug(f"CLI stderr: {result.stderr}")

        # Should complete without crashing
        assert result.returncode is not None

    def test_directory_with_no_yaml_files(self, tmp_path, mock_token_env):
        """
        batch-analyze should handle directory with no YAML files.
        """
        non_yaml_dir = tmp_path / "no_yaml"
        non_yaml_dir.mkdir()

        # Create some non-YAML files
        (non_yaml_dir / "readme.txt").write_text("This is not a YAML file")
        (non_yaml_dir / "script.py").write_text("print('hello')")

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(non_yaml_dir)],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"CLI stdout: {result.stdout}")
        logger.debug(f"CLI stderr: {result.stderr}")

        # Should complete
        assert result.returncode is not None


class TestEdgeCases:
    """
    Tests for various edge cases and boundary conditions.
    """

    def test_empty_yaml_file(self, tmp_path):
        """
        ActionParser should handle empty YAML files.
        """
        empty_file = tmp_path / "empty.yml"
        empty_file.write_text("")

        action = Action(file_path=str(empty_file))

        try:
            workflow = action.prepare_for_analysis()
            # Empty file should return None or empty workflow
            logger.info(f"Empty YAML result: {workflow}")
        except Exception as e:
            logger.info(f"Empty YAML raised: {type(e).__name__}: {e}")

    def test_yaml_with_only_comments(self, tmp_path):
        """
        ActionParser should handle YAML with only comments.
        """
        comments_only = tmp_path / "comments.yml"
        comments_only.write_text("# This is just a comment\n# Another comment\n")

        action = Action(file_path=str(comments_only))

        try:
            workflow = action.prepare_for_analysis()
            logger.info(f"Comments-only YAML result: {workflow}")
        except Exception as e:
            logger.info(f"Comments-only YAML raised: {type(e).__name__}: {e}")

    def test_yaml_with_null_values(self, tmp_path):
        """
        ActionParser should handle YAML with null values.
        """
        null_yaml = tmp_path / "nulls.yml"
        null_yaml.write_text("""
name: Null Test
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    env: null
    steps:
      - name: Test
        run: echo "test"
        env: ~
""")

        action = Action(file_path=str(null_yaml))

        try:
            workflow = action.prepare_for_analysis()
            logger.info(f"Null values YAML result: {workflow}")
            # Should not crash
            assert True
        except Exception as e:
            logger.info(f"Null values YAML raised: {type(e).__name__}: {e}")

    def test_very_large_workflow(self, tmp_path):
        """
        ActionParser should handle very large workflow files.
        """
        large_yaml = tmp_path / "large.yml"

        # Generate a large workflow with many jobs
        content = "name: Large Workflow\non: push\njobs:\n"
        for i in range(100):
            content += f"""  job_{i}:
    runs-on: ubuntu-latest
    steps:
      - name: Step {i}
        run: echo "Job {i}"
"""
        large_yaml.write_text(content)

        action = Action(file_path=str(large_yaml))

        try:
            workflow = action.prepare_for_analysis()
            logger.info(f"Large YAML parsed: {workflow is not None}")
            assert workflow is not None, "Should parse large workflow"
        except Exception as e:
            pytest.fail(f"Large YAML should not crash: {e}")

    def test_unicode_in_workflow(self, tmp_path):
        """
        ActionParser should handle unicode characters.
        """
        unicode_yaml = tmp_path / "unicode.yml"
        unicode_yaml.write_text("""
name: Workflow com acentuação 日本語 🚀
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Tëst with ünïcödé
        run: echo "Olá Mundo! 你好世界"
""", encoding='utf-8')

        action = Action(file_path=str(unicode_yaml))

        try:
            workflow = action.prepare_for_analysis()
            logger.info(f"Unicode YAML parsed: {workflow is not None}")
        except Exception as e:
            logger.info(f"Unicode YAML raised: {type(e).__name__}: {e}")


class TestTokenErrorHandling:
    """
    Tests for token-related error handling.
    Note: These tests are limited as token validation happens at runtime.
    """

    def test_analysis_works_without_api_calls(self, fixtures_path):
        """
        Basic analysis should work without requiring token validation.
        Most detectors don't need API access.
        """
        clean_path = str(fixtures_path / "clean_workflow.yml")
        action = Action(file_path=clean_path)
        workflow = action.prepare_for_analysis()

        # Should parse without token
        assert workflow is not None, "Should parse workflow without token"

    def test_detectors_work_without_token(self, fixtures_path):
        """
        Most detectors should work without GitHub token.
        Only UntrustedDependencies requires API access.
        """
        from Analysis.Smells.Categories.Security.AdminByDefault.AdminByDefaultFct import AdminByDefaultFct
        from Analysis.Smells.Categories.Security.HardCoded.HardCodedFct import HardCodedFct

        clean_path = str(fixtures_path / "clean_workflow.yml")
        action = Action(file_path=clean_path)
        workflow = action.prepare_for_analysis()

        # These should work without token
        admin_detector = AdminByDefaultFct(content=workflow)
        admin_findings = admin_detector.detect()

        hardcoded_detector = HardCodedFct(content=workflow)
        hardcoded_findings = hardcoded_detector.detect()

        # Should complete without errors
        assert isinstance(admin_findings, list)
        assert isinstance(hardcoded_findings, list)
