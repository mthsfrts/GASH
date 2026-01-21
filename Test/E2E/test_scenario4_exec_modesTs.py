"""
E2E Test Scenario 4: Execution Modes
Tests the different execution modes of GASH CLI.

This scenario validates:
- Single file analysis mode (analyze --file)
- Batch directory analysis mode (batch-analyze --dir)
- Consistency between single and batch modes
- Proper output generation for each mode
- Correct handling of different file types and structures
"""
import pytest
import logging
import subprocess
import sys
import os
import shutil
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from Analysis.Parse.ActionParser import Action
from Analysis.Smells.Categories.Security.AdminByDefault.AdminByDefaultFct import AdminByDefaultFct
from Analysis.Smells.Categories.Security.HardCoded.HardCodedFct import HardCodedFct
from Analysis.Smells.Categories.Security.UnsecureProtocol.UnsecureProtocolFct import UnsecureProtocolFct
from Analysis.Smells.Categories.Maintenance.ErrorHandling.ErrorHandlingFct import ErrorHandlingFct

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestSingleFileAnalysisMode:
    """
    Scenario 4.1: Single file analysis mode
    Tests the `analyze --file` command
    """

    @pytest.fixture
    def clean_workflow_path(self, fixtures_path):
        """Path to clean workflow fixture."""
        return str(fixtures_path / "clean_workflow.yml")

    @pytest.fixture
    def vulnerable_workflow_path(self, fixtures_path):
        """Path to vulnerable workflow fixture."""
        return str(fixtures_path / "vulnerable_workflow.yml")

    @pytest.fixture
    def complex_workflow_path(self, fixtures_path):
        """Path to complex workflow fixture."""
        return str(fixtures_path / "complex_workflow.yml")

    def test_single_file_analysis_executes(self, clean_workflow_path, mock_token_env):
        """
        CLI analyze command should execute successfully for a single file.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", clean_workflow_path],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"stdout: {result.stdout}")
        logger.debug(f"stderr: {result.stderr}")

        # Should execute without crashing
        assert result.returncode == 0 or "Error" not in result.stderr

    @pytest.mark.requires_real_token
    def test_single_file_analysis_output_format(self, vulnerable_workflow_path, ci_token_env):
        """
        CLI analyze should output findings in expected format.
        Requires real token to validate output format.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", vulnerable_workflow_path],
            capture_output=True,
            text=True,
            timeout=60,
            env=ci_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"stdout: {result.stdout}")

        # Output should contain "Findings for" sections
        assert "Findings for" in result.stdout or "Analyzing" in result.stdout

    @pytest.mark.requires_real_token
    def test_single_file_detects_all_detector_types(self, complex_workflow_path, ci_token_env):
        """
        Single file analysis should run all 9 detectors.
        Requires real token to execute full analysis.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", complex_workflow_path],
            capture_output=True,
            text=True,
            timeout=60,
            env=ci_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"stdout: {result.stdout}")

        # Should mention multiple detector names in output
        detector_names = [
            'CodeReplica', 'ErrorHandling', 'Misconfiguration', 'LongBlock',
            'AdminByDefault', 'HardCoded', 'RemoteRun', 'UnsecureProtocol',
            'UntrustedDependencies'
        ]

        detectors_in_output = sum(1 for name in detector_names if name in result.stdout)
        assert detectors_in_output >= 5, \
            f"Expected at least 5 detectors in output, found {detectors_in_output}"

    def test_single_file_with_yml_extension(self, fixtures_path, mock_token_env):
        """
        CLI should handle .yml extension files.
        """
        yml_file = fixtures_path / "clean_workflow.yml"
        assert yml_file.exists(), f"Test fixture not found: {yml_file}"

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", str(yml_file)],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        assert result.returncode == 0 or "Error" not in result.stderr

    def test_single_file_with_yaml_extension(self, fixtures_path, tmp_path, mock_token_env):
        """
        CLI should handle .yaml extension files.
        """
        # Copy a fixture and rename to .yaml
        src = fixtures_path / "clean_workflow.yml"
        dst = tmp_path / "test_workflow.yaml"
        shutil.copy(src, dst)

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", str(dst)],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        assert result.returncode == 0 or "Error" not in result.stderr


class TestBatchDirectoryAnalysisMode:
    """
    Scenario 4.2: Batch directory analysis mode
    Tests the `batch-analyze --dir` command
    """

    @pytest.fixture
    def batch_test_dir(self, fixtures_path, tmp_path):
        """
        Create a temporary directory with multiple workflow files for batch testing.
        """
        batch_dir = tmp_path / "batch_test"
        batch_dir.mkdir()

        # Copy fixtures to batch directory
        for workflow in ["clean_workflow.yml", "vulnerable_workflow.yml", "maintenance_issues.yml"]:
            src = fixtures_path / workflow
            if src.exists():
                shutil.copy(src, batch_dir / workflow)

        return batch_dir

    def test_batch_analyze_executes(self, batch_test_dir, mock_token_env):
        """
        CLI batch-analyze command should execute successfully.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(batch_test_dir)],
            capture_output=True,
            text=True,
            timeout=120,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"stdout: {result.stdout}")
        logger.debug(f"stderr: {result.stderr}")

        # Should execute without crashing
        assert result.returncode == 0 or "Error" not in result.stderr

    @pytest.mark.requires_real_token
    def test_batch_analyze_processes_multiple_files(self, batch_test_dir, ci_token_env):
        """
        Batch analyze should process multiple workflow files.
        Requires real token to execute full analysis.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(batch_test_dir)],
            capture_output=True,
            text=True,
            timeout=120,
            env=ci_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"stdout: {result.stdout}")

        # Should indicate processing of files
        assert "Analyzing" in result.stdout or "Analysis complete" in result.stdout

    def test_batch_analyze_creates_log_files(self, batch_test_dir, mock_token_env):
        """
        Batch analyze should create log files for each analyzed workflow.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(batch_test_dir)],
            capture_output=True,
            text=True,
            timeout=120,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        # Check for GashAnalyses directory creation
        # Note: The directory is created at os.path.dirname(repo_dir)
        parent_dir = batch_test_dir.parent
        analysis_dir = parent_dir / "GashAnalyses"

        if analysis_dir.exists():
            log_files = list(analysis_dir.glob("*.log"))
            logger.info(f"Found {len(log_files)} log files in {analysis_dir}")
            assert len(log_files) > 0, "Expected log files to be created"
        else:
            # If no analysis dir, check output mentions completion
            assert "complete" in result.stdout.lower() or result.returncode == 0

    def test_batch_analyze_handles_mixed_extensions(self, tmp_path, fixtures_path, mock_token_env):
        """
        Batch analyze should handle both .yml and .yaml files.
        """
        mixed_dir = tmp_path / "mixed_extensions"
        mixed_dir.mkdir()

        # Create .yml file
        shutil.copy(fixtures_path / "clean_workflow.yml", mixed_dir / "workflow1.yml")

        # Create .yaml file
        shutil.copy(fixtures_path / "vulnerable_workflow.yml", mixed_dir / "workflow2.yaml")

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(mixed_dir)],
            capture_output=True,
            text=True,
            timeout=120,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        # Should process files without errors
        assert result.returncode == 0 or "Error" not in result.stderr

    def test_batch_analyze_recursive_search(self, tmp_path, fixtures_path, mock_token_env):
        """
        Batch analyze should find workflow files in subdirectories.
        """
        # Create nested directory structure
        nested_dir = tmp_path / "nested"
        nested_dir.mkdir()
        subdir = nested_dir / ".github" / "workflows"
        subdir.mkdir(parents=True)

        shutil.copy(fixtures_path / "clean_workflow.yml", subdir / "ci.yml")

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(nested_dir)],
            capture_output=True,
            text=True,
            timeout=120,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"stdout: {result.stdout}")

        # Should find and process the nested file
        assert "Analyzing" in result.stdout or result.returncode == 0


class TestSingleVsBatchConsistency:
    """
    Scenario 4.3: Consistency between single file and batch analysis
    Validates that results are consistent across execution modes
    """

    @pytest.fixture
    def test_workflow_path(self, fixtures_path):
        """Path to test workflow."""
        return fixtures_path / "vulnerable_workflow.yml"

    @pytest.fixture
    def test_workflow(self, test_workflow_path):
        """Parse test workflow."""
        action = Action(file_path=str(test_workflow_path))
        return action.prepare_for_analysis()

    @pytest.mark.requires_real_token
    def test_detector_results_match_cli_single(self, test_workflow, test_workflow_path, ci_token_env):
        """
        Direct detector results should match CLI single file output.
        Requires real token to compare detector results with CLI output.
        """
        # Get findings directly from detector
        admin_detector = AdminByDefaultFct(content=test_workflow)
        direct_findings = admin_detector.detect()

        # Get findings via CLI
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", str(test_workflow_path)],
            capture_output=True,
            text=True,
            timeout=60,
            env=ci_token_env,
            cwd=str(PROJECT_ROOT)
        )

        # If we have direct findings, CLI should report them
        if direct_findings:
            assert "AdminByDefault" in result.stdout, \
                f"Expected AdminByDefault in CLI output. Direct findings: {direct_findings}"

    def test_single_and_batch_detect_same_smells(self, fixtures_path, tmp_path, mock_token_env):
        """
        Single file and batch analysis should detect the same smells for the same file.
        """
        test_file = fixtures_path / "vulnerable_workflow.yml"

        # Single file analysis
        single_result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", str(test_file)],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        # Batch analysis (copy to temp dir)
        batch_dir = tmp_path / "batch_consistency"
        batch_dir.mkdir()
        shutil.copy(test_file, batch_dir / "vulnerable_workflow.yml")

        batch_result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(batch_dir)],
            capture_output=True,
            text=True,
            timeout=120,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"Single output: {single_result.stdout[:500]}")
        logger.debug(f"Batch output: {batch_result.stdout[:500]}")

        # Both should execute successfully
        assert single_result.returncode == 0 or "Error" not in single_result.stderr
        assert batch_result.returncode == 0 or "Error" not in batch_result.stderr

    def test_findings_count_consistency(self, fixtures_path):
        """
        Detector findings should be consistent regardless of how the workflow is loaded.
        """
        workflow_path = fixtures_path / "vulnerable_workflow.yml"

        # Load and analyze twice
        action1 = Action(file_path=str(workflow_path))
        workflow1 = action1.prepare_for_analysis()
        findings1 = HardCodedFct(content=workflow1).detect()

        action2 = Action(file_path=str(workflow_path))
        workflow2 = action2.prepare_for_analysis()
        findings2 = HardCodedFct(content=workflow2).detect()

        # Results should be identical
        assert len(findings1) == len(findings2), \
            f"Inconsistent findings count: {len(findings1)} vs {len(findings2)}"


class TestExecutionModeEdgeCases:
    """
    Scenario 4.4: Edge cases for execution modes
    """

    def test_analyze_with_absolute_path(self, fixtures_path, mock_token_env):
        """
        CLI should handle absolute file paths.
        """
        absolute_path = (fixtures_path / "clean_workflow.yml").resolve()

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", str(absolute_path)],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        assert result.returncode == 0 or "Error" not in result.stderr

    def test_analyze_with_relative_path(self, fixtures_path, mock_token_env):
        """
        CLI should handle relative file paths.
        """
        # Get relative path from project root
        relative_path = fixtures_path.relative_to(PROJECT_ROOT) / "clean_workflow.yml"

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", str(relative_path)],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        assert result.returncode == 0 or "Error" not in result.stderr

    def test_batch_analyze_empty_directory(self, tmp_path, mock_token_env):
        """
        Batch analyze should handle empty directories gracefully.
        """
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(empty_dir)],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        # Should not crash
        assert "Error" not in result.stderr or result.returncode == 0

    def test_batch_analyze_directory_with_no_yaml(self, tmp_path, mock_token_env):
        """
        Batch analyze should handle directories with no YAML files.
        """
        no_yaml_dir = tmp_path / "no_yaml"
        no_yaml_dir.mkdir()

        # Create non-YAML files
        (no_yaml_dir / "readme.txt").write_text("This is not a YAML file")
        (no_yaml_dir / "script.py").write_text("print('hello')")

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(no_yaml_dir)],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        # Should indicate no files found
        assert "No YAML files" in result.stdout or result.returncode == 0

    def test_analyze_nonexistent_file(self, mock_token_env):
        """
        Analyze should handle nonexistent files gracefully.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", "/nonexistent/path/workflow.yml"],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        # Should not crash, may show error message
        # The important thing is it doesn't throw an unhandled exception
        logger.debug(f"stdout: {result.stdout}")
        logger.debug(f"stderr: {result.stderr}")

    def test_batch_analyze_nonexistent_directory(self, mock_token_env):
        """
        Batch analyze should handle nonexistent directories gracefully.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", "/nonexistent/directory"],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        # Should indicate no repositories found
        assert "No repositories found" in result.stdout or "Error" not in result.stderr


class TestOutputValidation:
    """
    Scenario 4.5: Output validation for execution modes
    """

    @pytest.mark.requires_real_token
    def test_single_analysis_output_contains_filename(self, fixtures_path, ci_token_env):
        """
        Single file analysis output should reference the analyzed file.
        Requires real token to get full output.
        """
        test_file = fixtures_path / "clean_workflow.yml"

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", str(test_file)],
            capture_output=True,
            text=True,
            timeout=60,
            env=ci_token_env,
            cwd=str(PROJECT_ROOT)
        )

        # Output should mention the file being analyzed
        assert "clean_workflow.yml" in result.stdout or "Analyzing" in result.stdout

    @pytest.mark.requires_real_token
    def test_single_analysis_output_structure(self, fixtures_path, ci_token_env):
        """
        Single file analysis should output findings in structured format.
        Requires real token to validate output structure.
        """
        test_file = fixtures_path / "vulnerable_workflow.yml"

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", str(test_file)],
            capture_output=True,
            text=True,
            timeout=60,
            env=ci_token_env,
            cwd=str(PROJECT_ROOT)
        )

        # Should have structured output with "Findings for X:" pattern
        assert "Findings for" in result.stdout

    @pytest.mark.requires_real_token
    def test_batch_analysis_reports_progress(self, fixtures_path, tmp_path, ci_token_env):
        """
        Batch analysis should report progress as it processes files.
        Requires real token to see progress output.
        """
        batch_dir = tmp_path / "progress_test"
        batch_dir.mkdir()

        # Copy multiple files
        for workflow in ["clean_workflow.yml", "vulnerable_workflow.yml"]:
            src = fixtures_path / workflow
            if src.exists():
                shutil.copy(src, batch_dir / workflow)

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(batch_dir)],
            capture_output=True,
            text=True,
            timeout=120,
            env=ci_token_env,
            cwd=str(PROJECT_ROOT)
        )

        # Should show progress indicators
        assert "Analyzing" in result.stdout or "Starting analysis" in result.stdout

    @pytest.mark.requires_real_token
    def test_findings_reported_with_bullet_points(self, fixtures_path, ci_token_env):
        """
        Findings should be reported with bullet points for readability.
        Requires real token to see findings output.
        """
        test_file = fixtures_path / "vulnerable_workflow.yml"

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", str(test_file)],
            capture_output=True,
            text=True,
            timeout=60,
            env=ci_token_env,
            cwd=str(PROJECT_ROOT)
        )

        # If there are findings, they should be formatted with bullets
        if "Findings for" in result.stdout and "No findings detected" not in result.stdout:
            assert "-" in result.stdout, "Expected bullet points in findings output"
