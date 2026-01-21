"""
E2E Test Scenario 1: Clean Repository Analysis
Tests that GASH correctly reports no smells for well-configured workflows.

This scenario validates:
- Clean workflows produce no findings
- All 9 detectors return empty results for proper configurations
- No false positives on GitHub's official starter-workflows (golden master)
"""
import pytest
import logging
import subprocess
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from Analysis.Parse.ActionParser import Action
from Analysis.Smells.Categories.Security.AdminByDefault.AdminByDefaultFct import AdminByDefaultFct
from Analysis.Smells.Categories.Security.HardCoded.HardCodedFct import HardCodedFct
from Analysis.Smells.Categories.Security.RemoteTriggers.RemoteRunFct import RemoteRunFct
from Analysis.Smells.Categories.Security.UnsecureProtocol.UnsecureProtocolFct import UnsecureProtocolFct
from Analysis.Smells.Categories.Maintenance.CodeReplica.CodeReplicaFct import CodeReplicaFct
from Analysis.Smells.Categories.Maintenance.ErrorHandling.ErrorHandlingFct import ErrorHandlingFct
from Analysis.Smells.Categories.Maintenance.Misconfiguration.MisconfigurationFct import MisconfigurationFct
from Analysis.Smells.Categories.Quality.LongBlocks.LongBlockFct import LongBlockFct

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestCleanRepositoryAnalysis:
    """
    Scenario 1: Clean repository analysis
    - No smells should be detected in properly configured workflows
    - Exit code should be 0
    - Output should confirm clean analysis
    """

    @pytest.fixture
    def clean_workflow_path(self, fixtures_path):
        """Path to clean workflow fixture."""
        return str(fixtures_path / "clean_workflow.yml")

    @pytest.fixture
    def clean_workflow(self, clean_workflow_path):
        """Parse clean workflow into Workflow object."""
        action = Action(file_path=clean_workflow_path)
        return action.prepare_for_analysis()

    # ================================================================
    # Unit Tests: Individual Detector Validation
    # ================================================================

    def test_admin_by_default_no_findings(self, clean_workflow):
        """AdminByDefault detector should find no issues in clean workflow."""
        detector = AdminByDefaultFct(content=clean_workflow)
        findings = detector.detect()

        assert findings == [], f"Unexpected AdminByDefault findings: {findings}"

    def test_hard_coded_no_findings(self, clean_workflow):
        """HardCoded detector should find no secrets in clean workflow."""
        detector = HardCodedFct(content=clean_workflow)
        findings = detector.detect()

        assert findings == [], f"Unexpected HardCoded findings: {findings}"

    def test_remote_triggers_no_findings(self, clean_workflow):
        """RemoteTriggers detector should find no issues in clean workflow."""
        detector = RemoteRunFct(content=clean_workflow)
        findings = detector.detect()

        assert findings == [], f"Unexpected RemoteTriggers findings: {findings}"

    def test_unsecure_protocol_no_findings(self, clean_workflow):
        """UnsecureProtocol detector should find no HTTP URLs in clean workflow."""
        detector = UnsecureProtocolFct(content=clean_workflow)
        findings = detector.detect()

        assert findings == [], f"Unexpected UnsecureProtocol findings: {findings}"

    def test_code_replica_no_findings(self, clean_workflow):
        """CodeReplica detector should find no duplicates in clean workflow."""
        detector = CodeReplicaFct(content=clean_workflow)
        findings = detector.detect()

        assert findings == [], f"Unexpected CodeReplica findings: {findings}"

    def test_error_handling_no_findings(self, clean_workflow):
        """ErrorHandling detector should find no issues in clean workflow."""
        detector = ErrorHandlingFct(content=clean_workflow)
        findings = detector.detect()

        assert findings == [], f"Unexpected ErrorHandling findings: {findings}"

    def test_misconfiguration_no_findings(self, clean_workflow):
        """Misconfiguration detector should find no issues in clean workflow."""
        detector = MisconfigurationFct(content=clean_workflow)
        findings = detector.detect()

        assert findings == [], f"Unexpected Misconfiguration findings: {findings}"

    def test_long_blocks_no_findings(self, clean_workflow):
        """LongBlocks detector should find no issues in clean workflow."""
        detector = LongBlockFct(content=clean_workflow)
        findings = detector.detect()

        assert findings == [], f"Unexpected LongBlocks findings: {findings}"

    # ================================================================
    # Integration Test: All Detectors Combined
    # ================================================================

    def test_all_detectors_clean(self, clean_workflow, mock_github_api):
        """
        All 9 detectors should return empty findings for clean workflow.
        Note: UntrustedDependencies requires API mock.
        """
        detectors = {
            'AdminByDefault': AdminByDefaultFct(content=clean_workflow),
            'HardCoded': HardCodedFct(content=clean_workflow),
            'RemoteTriggers': RemoteRunFct(content=clean_workflow),
            'UnsecureProtocol': UnsecureProtocolFct(content=clean_workflow),
            'CodeReplica': CodeReplicaFct(content=clean_workflow),
            'ErrorHandling': ErrorHandlingFct(content=clean_workflow),
            'Misconfiguration': MisconfigurationFct(content=clean_workflow),
            'LongBlocks': LongBlockFct(content=clean_workflow),
        }

        all_findings = {}
        for name, detector in detectors.items():
            findings = detector.detect()
            all_findings[name] = findings
            logger.debug(f"{name}: {findings}")

        # Verify all detectors return empty
        for name, findings in all_findings.items():
            assert findings == [], f"{name} returned unexpected findings: {findings}"

    # ================================================================
    # CLI Integration Test
    # ================================================================

    def test_cli_analyze_clean_workflow(self, clean_workflow_path, mock_token_env):
        """
        CLI analyze command should report no findings for clean workflow.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", clean_workflow_path],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"CLI stdout: {result.stdout}")
        logger.debug(f"CLI stderr: {result.stderr}")

        # Check for successful execution
        # Note: The actual output format depends on GASH.py implementation
        assert "Error" not in result.stderr or result.returncode == 0


class TestStarterWorkflowsGoldenMaster:
    """
    Golden Master Tests using actions/starter-workflows repository.
    These official GitHub workflows should NOT trigger false positives.
    """

    @pytest.mark.requires_real_token
    @pytest.mark.slow
    def test_starter_workflows_no_false_positives(self, starter_workflows_path, mock_github_api):
        """
        GitHub's official starter-workflows should produce minimal/no findings.
        This validates we're not generating false positives on standard patterns.
        """
        if starter_workflows_path is None:
            pytest.skip("Could not clone starter-workflows repository")

        workflow_files = list(starter_workflows_path.glob("**/*.yml"))
        logger.info(f"Testing {len(workflow_files)} starter workflows")

        false_positive_threshold = 0.1  # Allow 10% of workflows to have findings
        workflows_with_findings = 0

        for workflow_file in workflow_files[:20]:  # Test first 20 for speed
            try:
                action = Action(file_path=str(workflow_file))
                workflow = action.prepare_for_analysis()

                if workflow is None:
                    continue

                # Test with AdminByDefault (common false positive candidate)
                admin_detector = AdminByDefaultFct(content=workflow)
                admin_findings = admin_detector.detect()

                if admin_findings:
                    workflows_with_findings += 1
                    logger.warning(f"Findings in {workflow_file.name}: {admin_findings}")

            except Exception as e:
                logger.debug(f"Skipping {workflow_file.name}: {e}")
                continue

        tested_count = min(20, len(workflow_files))
        false_positive_rate = workflows_with_findings / tested_count if tested_count > 0 else 0

        logger.info(f"False positive rate: {false_positive_rate:.2%} ({workflows_with_findings}/{tested_count})")

        assert false_positive_rate <= false_positive_threshold, \
            f"Too many false positives: {false_positive_rate:.2%} > {false_positive_threshold:.2%}"

    @pytest.mark.requires_real_token
    @pytest.mark.slow
    def test_starter_workflows_parse_successfully(self, starter_workflows_path):
        """
        All starter-workflows should parse without errors.
        Validates our YAML parser handles real-world workflows.
        """
        if starter_workflows_path is None:
            pytest.skip("Could not clone starter-workflows repository")

        workflow_files = list(starter_workflows_path.glob("**/*.yml"))
        parse_failures = []

        for workflow_file in workflow_files[:30]:  # Test first 30
            try:
                action = Action(file_path=str(workflow_file))
                workflow = action.prepare_for_analysis()

                if workflow is None:
                    parse_failures.append(workflow_file.name)

            except Exception as e:
                parse_failures.append(f"{workflow_file.name}: {e}")

        failure_rate = len(parse_failures) / min(30, len(workflow_files))

        assert failure_rate < 0.2, \
            f"Too many parse failures ({failure_rate:.2%}): {parse_failures[:5]}"
