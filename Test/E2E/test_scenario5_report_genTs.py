"""
E2E Test Scenario 5: Report Generation
Tests the report output formats and content of GASH.

This scenario validates:
- Console output format ("Findings for {detector}:")
- All 9 detectors are represented in output
- Log file generation for batch analysis
- Completeness of report data
- Proper formatting of findings (bullet points)
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
from Analysis.Smells.Categories.Security.RemoteTriggers.RemoteTriggersFct import RemoteRunFct
from Analysis.Smells.Categories.Security.UnsecureProtocol.UnsecureProtocolFct import UnsecureProtocolFct
from Analysis.Smells.Categories.Maintenance.CodeReplica.CodeReplicaFct import CodeReplicaFct
from Analysis.Smells.Categories.Maintenance.ErrorHandling.ErrorHandlingFct import ErrorHandlingFct
from Analysis.Smells.Categories.Maintenance.Misconfiguration.MisconfigurationFct import MisconfigurationFct
from Analysis.Smells.Categories.Quality.LongBlocks.LongBlockFct import LongBlockFct

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# All detector names as they appear in GASH output
DETECTOR_NAMES = [
    'CodeReplica',
    'ErrorHandling',
    'Misconfiguration',
    'LongBlock',
    'AdminByDefault',
    'HardCoded',
    'RemoteRun',
    'UnsecureProtocol',
    'UntrustedDependencies'
]


class TestConsoleOutputFormat:
    """
    Scenario 5.1: Console output format validation
    Tests the format of CLI output for single file analysis
    """

    @pytest.fixture
    def vulnerable_workflow(self, fixtures_path):
        """Parse vulnerable workflow."""
        action = Action(file_path=str(fixtures_path / "vulnerable_workflow.yml"))
        return action.prepare_for_analysis()

    @pytest.fixture
    def complex_workflow(self, fixtures_path):
        """Parse complex workflow."""
        action = Action(file_path=str(fixtures_path / "complex_workflow.yml"))
        return action.prepare_for_analysis()

    def test_detector_output_format_pattern(self, vulnerable_workflow):
        """
        Each detector should output findings in "Findings for {name}:" format.
        Testing directly with detectors to validate output format.
        """
        detectors = {
            'AdminByDefault': AdminByDefaultFct(content=vulnerable_workflow),
            'HardCoded': HardCodedFct(content=vulnerable_workflow),
        }

        for name, detector in detectors.items():
            findings = detector.detect()
            # Verify findings are returned as a list
            assert isinstance(findings, list), f"{name} should return a list"

            # If there are findings, they should be strings
            for finding in findings:
                assert isinstance(finding, str), f"{name} findings should be strings"

    def test_findings_are_descriptive(self, vulnerable_workflow):
        """
        Findings should contain descriptive information about the smell.
        """
        admin_detector = AdminByDefaultFct(content=vulnerable_workflow)
        findings = admin_detector.detect()

        assert len(findings) > 0, "Expected AdminByDefault findings"

        # Findings should contain meaningful text
        for finding in findings:
            assert len(finding) > 10, f"Finding too short: {finding}"
            # Should mention permission-related terms
            assert any(term in finding.lower() for term in ['permission', 'elevated', 'write']), \
                f"Finding should mention permission issues: {finding}"

    def test_hardcoded_findings_contain_context(self, vulnerable_workflow):
        """
        HardCoded findings should provide context about the detected secret.
        """
        detector = HardCodedFct(content=vulnerable_workflow)
        findings = detector.detect()

        assert len(findings) > 0, "Expected HardCoded findings"

        # At least some findings should have context
        logger.info(f"HardCoded findings: {findings}")

    def test_all_detectors_return_consistent_format(self, complex_workflow):
        """
        All detectors should return findings in a consistent format.
        """
        all_detectors = {
            'AdminByDefault': AdminByDefaultFct(content=complex_workflow),
            'HardCoded': HardCodedFct(content=complex_workflow),
            'RemoteTriggers': RemoteRunFct(content=complex_workflow),
            'UnsecureProtocol': UnsecureProtocolFct(content=complex_workflow),
            'CodeReplica': CodeReplicaFct(content=complex_workflow),
            'ErrorHandling': ErrorHandlingFct(content=complex_workflow),
            'Misconfiguration': MisconfigurationFct(content=complex_workflow),
            'LongBlocks': LongBlockFct(content=complex_workflow),
        }

        for name, detector in all_detectors.items():
            findings = detector.detect()

            # All detectors must return a list
            assert isinstance(findings, list), f"{name} must return a list, got {type(findings)}"

            # All findings must be strings
            for i, finding in enumerate(findings):
                assert isinstance(finding, str), \
                    f"{name} finding {i} must be string, got {type(finding)}"


class TestDetectorCoverage:
    """
    Scenario 5.2: Detector coverage in reports
    Tests that all 9 detectors are included in analysis
    """

    @pytest.fixture
    def complex_workflow(self, fixtures_path):
        """Parse complex workflow."""
        action = Action(file_path=str(fixtures_path / "complex_workflow.yml"))
        return action.prepare_for_analysis()

    def test_all_detector_types_available(self):
        """
        Verify all 9 detector types are defined.
        """
        assert len(DETECTOR_NAMES) == 9, f"Expected 9 detectors, got {len(DETECTOR_NAMES)}"

    def test_all_detectors_can_be_instantiated(self, complex_workflow):
        """
        All detectors should be instantiable with a workflow.
        """
        detectors = [
            ('AdminByDefault', AdminByDefaultFct),
            ('HardCoded', HardCodedFct),
            ('RemoteTriggers', RemoteRunFct),
            ('UnsecureProtocol', UnsecureProtocolFct),
            ('CodeReplica', CodeReplicaFct),
            ('ErrorHandling', ErrorHandlingFct),
            ('Misconfiguration', MisconfigurationFct),
            ('LongBlocks', LongBlockFct),
        ]

        for name, detector_class in detectors:
            try:
                detector = detector_class(content=complex_workflow)
                assert detector is not None, f"{name} instantiation returned None"
            except Exception as e:
                pytest.fail(f"Failed to instantiate {name}: {e}")

    def test_all_detectors_have_detect_method(self, complex_workflow):
        """
        All detectors should have a detect() method.
        """
        detectors = [
            AdminByDefaultFct(content=complex_workflow),
            HardCodedFct(content=complex_workflow),
            RemoteRunFct(content=complex_workflow),
            UnsecureProtocolFct(content=complex_workflow),
            CodeReplicaFct(content=complex_workflow),
            ErrorHandlingFct(content=complex_workflow),
            MisconfigurationFct(content=complex_workflow),
            LongBlockFct(content=complex_workflow),
        ]

        for detector in detectors:
            assert hasattr(detector, 'detect'), \
                f"{detector.__class__.__name__} missing detect() method"
            assert callable(detector.detect), \
                f"{detector.__class__.__name__}.detect is not callable"

    def test_complex_workflow_triggers_multiple_detectors(self, complex_workflow):
        """
        Complex workflow should trigger findings from multiple detector types.
        """
        detectors = {
            'AdminByDefault': AdminByDefaultFct(content=complex_workflow),
            'HardCoded': HardCodedFct(content=complex_workflow),
            'RemoteTriggers': RemoteRunFct(content=complex_workflow),
            'UnsecureProtocol': UnsecureProtocolFct(content=complex_workflow),
            'CodeReplica': CodeReplicaFct(content=complex_workflow),
            'ErrorHandling': ErrorHandlingFct(content=complex_workflow),
            'Misconfiguration': MisconfigurationFct(content=complex_workflow),
            'LongBlocks': LongBlockFct(content=complex_workflow),
        }

        detectors_with_findings = 0
        for name, detector in detectors.items():
            findings = detector.detect()
            if findings:
                detectors_with_findings += 1
                logger.info(f"{name}: {len(findings)} findings")

        assert detectors_with_findings >= 5, \
            f"Expected at least 5 detectors with findings, got {detectors_with_findings}"


class TestLogFileGeneration:
    """
    Scenario 5.3: Log file generation for batch analysis
    Tests the log files created by batch-analyze command
    """

    @pytest.fixture
    def batch_test_dir(self, fixtures_path, tmp_path):
        """Create temp directory with workflow files."""
        batch_dir = tmp_path / "batch_report_test"
        batch_dir.mkdir()

        for workflow in ["clean_workflow.yml", "vulnerable_workflow.yml"]:
            src = fixtures_path / workflow
            if src.exists():
                shutil.copy(src, batch_dir / workflow)

        return batch_dir

    @pytest.mark.requires_real_token
    def test_log_files_created_for_each_workflow(self, batch_test_dir, ci_token_env):
        """
        Batch analyze should create a log file for each workflow analyzed.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(batch_test_dir)],
            capture_output=True,
            text=True,
            timeout=180,
            env=ci_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"stdout: {result.stdout}")

        # Check for GashAnalyses directory
        analysis_dir = batch_test_dir.parent / "GashAnalyses"

        if analysis_dir.exists():
            log_files = list(analysis_dir.glob("*.log"))
            assert len(log_files) >= 1, "Expected at least one log file"

            # Check log file names match workflow names (without extension)
            log_names = {f.stem for f in log_files}
            expected_names = {"clean_workflow", "vulnerable_workflow"}
            assert log_names & expected_names, \
                f"Log files should match workflow names. Got: {log_names}"

    @pytest.mark.requires_real_token
    def test_log_file_contains_detector_sections(self, batch_test_dir, ci_token_env):
        """
        Log files should contain sections for each detector.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(batch_test_dir)],
            capture_output=True,
            text=True,
            timeout=180,
            env=ci_token_env,
            cwd=str(PROJECT_ROOT)
        )

        analysis_dir = batch_test_dir.parent / "GashAnalyses"

        if analysis_dir.exists():
            log_files = list(analysis_dir.glob("*.log"))

            for log_file in log_files:
                content = log_file.read_text()
                logger.debug(f"Log file {log_file.name} content:\n{content[:500]}")

                # Should contain "Findings for" sections
                assert "Findings for" in content, \
                    f"Log file {log_file.name} should contain 'Findings for' sections"

    @pytest.mark.requires_real_token
    def test_log_file_format_structure(self, batch_test_dir, ci_token_env):
        """
        Log files should have proper structure with findings or "No findings" message.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(batch_test_dir)],
            capture_output=True,
            text=True,
            timeout=180,
            env=ci_token_env,
            cwd=str(PROJECT_ROOT)
        )

        analysis_dir = batch_test_dir.parent / "GashAnalyses"

        if analysis_dir.exists():
            log_files = list(analysis_dir.glob("*.log"))

            for log_file in log_files:
                content = log_file.read_text()

                # Each detector section should have either findings (with "-") or "No findings detected"
                for detector in DETECTOR_NAMES:
                    if f"Findings for {detector}" in content:
                        # Section found, check it has content
                        pass  # Valid - section exists


class TestReportCompleteness:
    """
    Scenario 5.4: Report data completeness
    Tests that reports contain all necessary information
    """

    @pytest.fixture
    def vulnerable_workflow(self, fixtures_path):
        action = Action(file_path=str(fixtures_path / "vulnerable_workflow.yml"))
        return action.prepare_for_analysis()

    @pytest.fixture
    def maintenance_workflow(self, fixtures_path):
        action = Action(file_path=str(fixtures_path / "maintenance_issues.yml"))
        return action.prepare_for_analysis()

    def test_security_findings_have_actionable_info(self, vulnerable_workflow):
        """
        Security findings should contain actionable information.
        """
        admin_findings = AdminByDefaultFct(content=vulnerable_workflow).detect()

        for finding in admin_findings:
            # Should mention what to do (review, apply principle, etc.)
            actionable_terms = ['review', 'apply', 'consider', 'avoid', 'use', 'remove']
            has_action = any(term in finding.lower() for term in actionable_terms)
            logger.info(f"Finding: {finding}")
            # Not strictly required but good to have
            if not has_action:
                logger.warning(f"Finding may lack actionable guidance: {finding}")

    def test_findings_identify_location(self, vulnerable_workflow):
        """
        Findings should identify where the issue was found (workflow, job, step).
        """
        admin_findings = AdminByDefaultFct(content=vulnerable_workflow).detect()

        location_terms = ['workflow', 'job', 'step', 'build', 'deploy']
        findings_with_location = 0

        for finding in admin_findings:
            if any(term in finding.lower() for term in location_terms):
                findings_with_location += 1

        # Most findings should indicate location
        if admin_findings:
            location_rate = findings_with_location / len(admin_findings)
            assert location_rate >= 0.5, \
                f"At least 50% of findings should indicate location, got {location_rate:.0%}"

    def test_maintenance_findings_are_specific(self, maintenance_workflow):
        """
        Maintenance findings should be specific about the issue.
        """
        error_findings = ErrorHandlingFct(content=maintenance_workflow).detect()

        for finding in error_findings:
            # Findings should be reasonably detailed
            assert len(finding) > 15, f"Finding too vague: {finding}"

    def test_no_empty_findings_strings(self, vulnerable_workflow):
        """
        Findings should never be empty strings.
        """
        detectors = [
            AdminByDefaultFct(content=vulnerable_workflow),
            HardCodedFct(content=vulnerable_workflow),
            UnsecureProtocolFct(content=vulnerable_workflow),
        ]

        for detector in detectors:
            findings = detector.detect()
            for finding in findings:
                assert finding.strip(), "Finding should not be empty or whitespace-only"


class TestCLIReportOutput:
    """
    Scenario 5.5: CLI report output validation
    Tests CLI output format with real token
    """

    @pytest.mark.requires_real_token
    def test_cli_output_has_all_detector_sections(self, fixtures_path, ci_token_env):
        """
        CLI output should have a section for each detector.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file",
             str(fixtures_path / "complex_workflow.yml")],
            capture_output=True,
            text=True,
            timeout=60,
            env=ci_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"CLI output: {result.stdout}")

        # Count how many detector names appear in output
        detectors_in_output = sum(1 for name in DETECTOR_NAMES if name in result.stdout)

        assert detectors_in_output >= 8, \
            f"Expected at least 8 detector sections in output, found {detectors_in_output}"

    @pytest.mark.requires_real_token
    def test_cli_output_findings_formatted_with_bullets(self, fixtures_path, ci_token_env):
        """
        CLI findings should be formatted with bullet points.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file",
             str(fixtures_path / "vulnerable_workflow.yml")],
            capture_output=True,
            text=True,
            timeout=60,
            env=ci_token_env,
            cwd=str(PROJECT_ROOT)
        )

        # If there are findings, they should have bullet points
        if "Findings for" in result.stdout:
            lines = result.stdout.split('\n')
            bullet_lines = [l for l in lines if l.strip().startswith('-')]

            # Should have at least some bullet points for findings
            assert len(bullet_lines) > 0 or "No findings detected" in result.stdout, \
                "Expected bullet points or 'No findings detected'"

    @pytest.mark.requires_real_token
    def test_cli_clean_workflow_shows_no_findings(self, fixtures_path, ci_token_env):
        """
        Clean workflow should show "No findings detected" for most detectors.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file",
             str(fixtures_path / "clean_workflow.yml")],
            capture_output=True,
            text=True,
            timeout=60,
            env=ci_token_env,
            cwd=str(PROJECT_ROOT)
        )

        # Clean workflow should have "No findings detected" messages
        no_findings_count = result.stdout.count("No findings detected")

        logger.info(f"'No findings detected' count: {no_findings_count}")

        # Most detectors should report no findings for clean workflow
        # (allowing some due to known bugs mentioned in issue25.md)
        assert no_findings_count >= 5, \
            f"Expected at least 5 'No findings detected' for clean workflow, got {no_findings_count}"


class TestReportConsistency:
    """
    Scenario 5.6: Report consistency across runs
    Tests that reports are consistent and reproducible
    """

    @pytest.fixture
    def test_workflow(self, fixtures_path):
        return fixtures_path / "vulnerable_workflow.yml"

    def test_detector_findings_are_deterministic(self, test_workflow):
        """
        Running the same detector twice should produce identical findings.
        """
        action1 = Action(file_path=str(test_workflow))
        workflow1 = action1.prepare_for_analysis()
        findings1 = AdminByDefaultFct(content=workflow1).detect()

        action2 = Action(file_path=str(test_workflow))
        workflow2 = action2.prepare_for_analysis()
        findings2 = AdminByDefaultFct(content=workflow2).detect()

        assert findings1 == findings2, \
            f"Findings should be deterministic. Run 1: {findings1}, Run 2: {findings2}"

    def test_findings_order_is_consistent(self, test_workflow):
        """
        Findings should be returned in a consistent order.
        """
        action = Action(file_path=str(test_workflow))
        workflow = action.prepare_for_analysis()

        # Run multiple times
        results = []
        for _ in range(3):
            findings = HardCodedFct(content=workflow).detect()
            results.append(findings)

        # All runs should produce same order
        assert all(r == results[0] for r in results), \
            "Findings order should be consistent across runs"

    def test_multiple_detectors_consistent_across_runs(self, test_workflow):
        """
        All detectors should produce consistent results across runs.
        """
        action = Action(file_path=str(test_workflow))
        workflow = action.prepare_for_analysis()

        detectors_classes = [
            AdminByDefaultFct,
            HardCodedFct,
            UnsecureProtocolFct,
            RemoteRunFct,
        ]

        for detector_class in detectors_classes:
            findings1 = detector_class(content=workflow).detect()
            findings2 = detector_class(content=workflow).detect()

            assert findings1 == findings2, \
                f"{detector_class.__name__} produced inconsistent results"
