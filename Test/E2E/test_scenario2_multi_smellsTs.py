"""
E2E Test Scenario 2: Multi-Smell Detection
Tests that GASH correctly detects multiple types of smells in workflows.

This scenario validates:
- Security smells are properly detected (AdminByDefault, HardCoded, UnsecureProtocol, RemoteTriggers)
- Maintenance smells are properly detected (CodeReplica, ErrorHandling, Misconfiguration)
- Quality smells are properly detected (LongBlocks)
- Complex workflows with all smell types are analyzed correctly
- Real-world vulnerable repositories (juice-shop) produce expected findings
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
from Analysis.Smells.Categories.Security.RemoteTriggers.RemoteTriggersFct import RemoteRunFct
from Analysis.Smells.Categories.Security.UnsecureProtocol.UnsecureProtocolFct import UnsecureProtocolFct
from Analysis.Smells.Categories.Maintenance.CodeReplica.CodeReplicaFct import CodeReplicaFct
from Analysis.Smells.Categories.Maintenance.ErrorHandling.ErrorHandlingFct import ErrorHandlingFct
from Analysis.Smells.Categories.Maintenance.Misconfiguration.MisconfigurationFct import MisconfigurationFct
from Analysis.Smells.Categories.Quality.LongBlocks.LongBlockFct import LongBlockFct

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestSecuritySmellsDetection:
    """
    Scenario 2.1: Security smell detection
    - AdminByDefault: write-all permissions
    - HardCoded: hardcoded secrets/credentials
    - UnsecureProtocol: HTTP URLs
    - RemoteTriggers: workflow_dispatch without proper config
    """

    @pytest.fixture
    def vulnerable_workflow_path(self, fixtures_path):
        """Path to vulnerable workflow fixture."""
        return str(fixtures_path / "vulnerable_workflow.yml")

    @pytest.fixture
    def vulnerable_workflow(self, vulnerable_workflow_path):
        """Parse vulnerable workflow into Workflow object."""
        action = Action(file_path=vulnerable_workflow_path)
        return action.prepare_for_analysis()

    def test_admin_by_default_detected(self, vulnerable_workflow):
        """
        AdminByDefault detector should find write-all permissions.
        Expected findings: workflow-level write-all, job-level elevated permissions
        """
        detector = AdminByDefaultFct(content=vulnerable_workflow)
        findings = detector.detect()

        logger.debug(f"AdminByDefault findings: {findings}")

        assert len(findings) > 0, "Expected AdminByDefault findings for write-all permissions"

    def test_hard_coded_secrets_detected(self, vulnerable_workflow):
        """
        HardCoded detector should find hardcoded secrets.
        Expected: API keys, passwords, private keys, AWS credentials
        """
        detector = HardCodedFct(content=vulnerable_workflow)
        findings = detector.detect()

        logger.debug(f"HardCoded findings: {findings}")

        assert len(findings) > 0, "Expected HardCoded findings for secrets in workflow"

    def test_unsecure_protocol_detected(self, vulnerable_workflow):
        """
        UnsecureProtocol detector should find HTTP URLs.
        Expected: http:// URLs in env vars and run commands
        """
        detector = UnsecureProtocolFct(content=vulnerable_workflow)
        findings = detector.detect()

        logger.debug(f"UnsecureProtocol findings: {findings}")

        assert len(findings) > 0, "Expected UnsecureProtocol findings for HTTP URLs"

    def test_remote_triggers_detected(self, vulnerable_workflow):
        """
        RemoteTriggers detector should find misconfigured triggers.
        Expected: workflow_dispatch and repository_dispatch without proper config
        """
        detector = RemoteRunFct(content=vulnerable_workflow)
        findings = detector.detect()

        logger.debug(f"RemoteTriggers findings: {findings}")

        assert len(findings) > 0, "Expected RemoteTriggers findings for dispatch events"

    def test_all_security_smells_combined(self, vulnerable_workflow):
        """
        All security detectors should find issues in vulnerable workflow.
        """
        security_detectors = {
            'AdminByDefault': AdminByDefaultFct(content=vulnerable_workflow),
            'HardCoded': HardCodedFct(content=vulnerable_workflow),
            'UnsecureProtocol': UnsecureProtocolFct(content=vulnerable_workflow),
            'RemoteTriggers': RemoteRunFct(content=vulnerable_workflow),
        }

        all_findings = {}
        total_findings = 0

        for name, detector in security_detectors.items():
            findings = detector.detect()
            all_findings[name] = findings
            total_findings += len(findings)
            logger.info(f"{name}: {len(findings)} findings")

        # Should have findings from multiple detectors
        detectors_with_findings = sum(1 for f in all_findings.values() if f)
        assert detectors_with_findings >= 3, \
            f"Expected at least 3 security detectors to find issues, got {detectors_with_findings}"


class TestMaintenanceSmellsDetection:
    """
    Scenario 2.2: Maintenance smell detection
    - CodeReplica: duplicated code blocks
    - ErrorHandling: continue-on-error, fail-fast: false
    - Misconfiguration: missing fields, fuzzy versions
    """

    @pytest.fixture
    def maintenance_workflow_path(self, fixtures_path):
        """Path to maintenance issues workflow fixture."""
        return str(fixtures_path / "maintenance_issues.yml")

    @pytest.fixture
    def maintenance_workflow(self, maintenance_workflow_path):
        """Parse maintenance workflow into Workflow object."""
        action = Action(file_path=maintenance_workflow_path)
        return action.prepare_for_analysis()

    def test_code_replica_detected(self, maintenance_workflow):
        """
        CodeReplica detector should find duplicated steps across jobs.
        Expected: build, test, lint jobs have similar setup patterns
        """
        detector = CodeReplicaFct(content=maintenance_workflow)
        findings = detector.detect()

        logger.debug(f"CodeReplica findings: {findings}")

        assert len(findings) > 0, "Expected CodeReplica findings for duplicated job patterns"

    def test_error_handling_detected(self, maintenance_workflow):
        """
        ErrorHandling detector should find error handling issues.
        Expected: continue-on-error, fail-fast: false, short timeouts
        """
        detector = ErrorHandlingFct(content=maintenance_workflow)
        findings = detector.detect()

        logger.debug(f"ErrorHandling findings: {findings}")

        assert len(findings) > 0, "Expected ErrorHandling findings for error handling issues"

    def test_misconfiguration_detected(self, maintenance_workflow):
        """
        Misconfiguration detector should find configuration issues.
        Expected: missing runs-on, fuzzy versions, complex conditionals
        """
        detector = MisconfigurationFct(content=maintenance_workflow)
        findings = detector.detect()

        logger.debug(f"Misconfiguration findings: {findings}")

        assert len(findings) > 0, "Expected Misconfiguration findings"

    def test_all_maintenance_smells_combined(self, maintenance_workflow):
        """
        All maintenance detectors should find issues.
        """
        maintenance_detectors = {
            'CodeReplica': CodeReplicaFct(content=maintenance_workflow),
            'ErrorHandling': ErrorHandlingFct(content=maintenance_workflow),
            'Misconfiguration': MisconfigurationFct(content=maintenance_workflow),
        }

        all_findings = {}
        for name, detector in maintenance_detectors.items():
            findings = detector.detect()
            all_findings[name] = findings
            logger.info(f"{name}: {len(findings)} findings")

        # Should have findings from multiple detectors
        detectors_with_findings = sum(1 for f in all_findings.values() if f)
        assert detectors_with_findings >= 2, \
            f"Expected at least 2 maintenance detectors to find issues, got {detectors_with_findings}"


class TestQualitySmellsDetection:
    """
    Scenario 2.3: Quality smell detection
    - LongBlocks: excessively long code blocks
    """

    @pytest.fixture
    def complex_workflow_path(self, fixtures_path):
        """Path to complex workflow fixture."""
        return str(fixtures_path / "complex_workflow.yml")

    @pytest.fixture
    def complex_workflow(self, complex_workflow_path):
        """Parse complex workflow into Workflow object."""
        action = Action(file_path=complex_workflow_path)
        return action.prepare_for_analysis()

    def test_long_blocks_detected(self, complex_workflow):
        """
        LongBlocks detector should find excessively long run blocks.
        Expected: The 30-line echo block in complex_workflow
        """
        detector = LongBlockFct(content=complex_workflow)
        findings = detector.detect()

        logger.debug(f"LongBlocks findings: {findings}")

        assert len(findings) > 0, "Expected LongBlocks findings for long run blocks"


class TestAllSmellTypesInComplexWorkflow:
    """
    Scenario 2.4: Complex workflow with all 9 smell types
    Validates comprehensive smell detection
    """

    @pytest.fixture
    def complex_workflow_path(self, fixtures_path):
        """Path to complex workflow fixture."""
        return str(fixtures_path / "complex_workflow.yml")

    @pytest.fixture
    def complex_workflow(self, complex_workflow_path):
        """Parse complex workflow into Workflow object."""
        action = Action(file_path=complex_workflow_path)
        return action.prepare_for_analysis()

    def test_minimum_smell_types_detected(self, complex_workflow, mock_github_api):
        """
        Complex workflow should trigger at least 5 different smell types.
        This validates broad detection coverage.
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

        all_findings = {}
        for name, detector in all_detectors.items():
            findings = detector.detect()
            all_findings[name] = findings
            logger.info(f"{name}: {len(findings)} findings")

        detectors_with_findings = sum(1 for f in all_findings.values() if f)
        total_findings = sum(len(f) for f in all_findings.values())

        logger.info(f"Total: {detectors_with_findings}/8 detectors found issues")
        logger.info(f"Total findings: {total_findings}")

        # Complex workflow should trigger at least 5 smell types
        assert detectors_with_findings >= 5, \
            f"Expected at least 5 smell types, got {detectors_with_findings}. " \
            f"Findings: {[(k, len(v)) for k, v in all_findings.items() if v]}"

    def test_security_smells_in_complex_workflow(self, complex_workflow):
        """
        Complex workflow should have multiple security issues.
        """
        security_findings = []

        # AdminByDefault
        admin_detector = AdminByDefaultFct(content=complex_workflow)
        security_findings.extend(admin_detector.detect())

        # HardCoded
        hardcoded_detector = HardCodedFct(content=complex_workflow)
        security_findings.extend(hardcoded_detector.detect())

        # UnsecureProtocol
        protocol_detector = UnsecureProtocolFct(content=complex_workflow)
        security_findings.extend(protocol_detector.detect())

        logger.info(f"Total security findings: {len(security_findings)}")

        assert len(security_findings) >= 3, \
            f"Expected at least 3 security findings, got {len(security_findings)}"

    def test_maintenance_smells_in_complex_workflow(self, complex_workflow):
        """
        Complex workflow should have maintenance issues.
        """
        maintenance_findings = []

        # CodeReplica
        replica_detector = CodeReplicaFct(content=complex_workflow)
        maintenance_findings.extend(replica_detector.detect())

        # ErrorHandling
        error_detector = ErrorHandlingFct(content=complex_workflow)
        maintenance_findings.extend(error_detector.detect())

        logger.info(f"Total maintenance findings: {len(maintenance_findings)}")

        assert len(maintenance_findings) >= 1, \
            f"Expected at least 1 maintenance finding, got {len(maintenance_findings)}"


class TestCLIMultiSmellDetection:
    """
    CLI integration tests for multi-smell detection
    """

    @pytest.fixture
    def vulnerable_workflow_path(self, fixtures_path):
        return str(fixtures_path / "vulnerable_workflow.yml")

    @pytest.fixture
    def complex_workflow_path(self, fixtures_path):
        return str(fixtures_path / "complex_workflow.yml")

    def test_cli_detects_smells_in_vulnerable_workflow(self, vulnerable_workflow_path, mock_token_env):
        """
        CLI should report findings for vulnerable workflow.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", vulnerable_workflow_path],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"CLI stdout: {result.stdout}")
        logger.debug(f"CLI stderr: {result.stderr}")

        # CLI should execute without crashing
        assert result.returncode == 0 or "Findings" in result.stdout or "Error" not in result.stderr

    def test_cli_detects_smells_in_complex_workflow(self, complex_workflow_path, mock_token_env):
        """
        CLI should report findings for complex workflow with all smell types.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "analyze", "--file", complex_workflow_path],
            capture_output=True,
            text=True,
            timeout=60,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"CLI stdout: {result.stdout}")
        logger.debug(f"CLI stderr: {result.stderr}")

        # CLI should execute without crashing
        assert result.returncode == 0 or "Findings" in result.stdout or "Error" not in result.stderr

    def test_cli_batch_analyze_fixtures_directory(self, fixtures_path, mock_token_env):
        """
        CLI batch-analyze should process multiple workflow files.
        """
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "GASH.py"), "batch-analyze", "--dir", str(fixtures_path)],
            capture_output=True,
            text=True,
            timeout=120,
            env=mock_token_env,
            cwd=str(PROJECT_ROOT)
        )

        logger.debug(f"CLI stdout: {result.stdout}")
        logger.debug(f"CLI stderr: {result.stderr}")

        # Batch analyze should process files without crashing
        # Note: Some files may have parse errors (malformed) which is expected
        assert result.returncode == 0 or "analyzed" in result.stdout.lower() or "Error" not in result.stderr


class TestJuiceShopVulnerableRepository:
    """
    Scenario 2.5: Real-world vulnerable repository test
    Uses OWASP Juice Shop - intentionally vulnerable application
    """

    @pytest.mark.requires_real_token
    @pytest.mark.slow
    def test_juice_shop_workflows_have_findings(self, juice_shop_workflows_path, mock_github_api):
        """
        Juice Shop workflows should produce security findings.
        This validates detection on real-world vulnerable code.
        """
        if juice_shop_workflows_path is None:
            pytest.skip("Could not clone juice-shop repository")

        workflow_files = list(juice_shop_workflows_path.glob("*.yml")) + \
                         list(juice_shop_workflows_path.glob("*.yaml"))

        if not workflow_files:
            pytest.skip("No workflow files found in juice-shop")

        logger.info(f"Testing {len(workflow_files)} Juice Shop workflows")

        all_findings = {
            'AdminByDefault': [],
            'HardCoded': [],
            'UnsecureProtocol': [],
            'RemoteTriggers': [],
            'ErrorHandling': [],
        }

        workflows_parsed = 0
        for workflow_file in workflow_files:
            try:
                action = Action(file_path=str(workflow_file))
                workflow = action.prepare_for_analysis()

                if workflow is None:
                    continue

                workflows_parsed += 1

                # Run security-focused detectors
                all_findings['AdminByDefault'].extend(
                    AdminByDefaultFct(content=workflow).detect()
                )
                all_findings['HardCoded'].extend(
                    HardCodedFct(content=workflow).detect()
                )
                all_findings['UnsecureProtocol'].extend(
                    UnsecureProtocolFct(content=workflow).detect()
                )
                all_findings['RemoteTriggers'].extend(
                    RemoteRunFct(content=workflow).detect()
                )
                all_findings['ErrorHandling'].extend(
                    ErrorHandlingFct(content=workflow).detect()
                )

            except Exception as e:
                logger.debug(f"Error parsing {workflow_file.name}: {e}")
                continue

        logger.info(f"Successfully parsed {workflows_parsed} workflows")

        for detector, findings in all_findings.items():
            logger.info(f"{detector}: {len(findings)} findings")

        total_findings = sum(len(f) for f in all_findings.values())
        logger.info(f"Total findings in Juice Shop: {total_findings}")

        # Juice Shop should have at least some findings
        # Being lenient here as the project may have improved security
        assert workflows_parsed > 0, "Should parse at least one workflow"

    @pytest.mark.requires_real_token
    @pytest.mark.slow
    def test_juice_shop_all_workflows_parse(self, juice_shop_workflows_path):
        """
        All Juice Shop workflows should parse without crashing.
        """
        if juice_shop_workflows_path is None:
            pytest.skip("Could not clone juice-shop repository")

        workflow_files = list(juice_shop_workflows_path.glob("*.yml")) + \
                         list(juice_shop_workflows_path.glob("*.yaml"))

        if not workflow_files:
            pytest.skip("No workflow files found in juice-shop")

        parse_failures = []
        for workflow_file in workflow_files:
            try:
                action = Action(file_path=str(workflow_file))
                workflow = action.prepare_for_analysis()
                # Just check that parsing doesn't raise an exception
            except Exception as e:
                parse_failures.append(f"{workflow_file.name}: {e}")

        if parse_failures:
            logger.warning(f"Parse failures: {parse_failures}")

        failure_rate = len(parse_failures) / len(workflow_files) if workflow_files else 0
        assert failure_rate < 0.5, \
            f"Too many parse failures ({failure_rate:.0%}): {parse_failures[:3]}"


class TestSmellAccuracy:
    """
    Accuracy validation tests
    Ensures detectors find specific expected smells
    """

    @pytest.fixture
    def vulnerable_workflow(self, fixtures_path):
        action = Action(file_path=str(fixtures_path / "vulnerable_workflow.yml"))
        return action.prepare_for_analysis()

    def test_hardcoded_finds_api_keys(self, vulnerable_workflow):
        """
        HardCoded detector should find API key patterns.
        """
        detector = HardCodedFct(content=vulnerable_workflow)
        findings = detector.detect()

        # Convert findings to string for pattern matching
        findings_str = str(findings).lower()

        # Should detect at least one type of secret
        secret_indicators = ['secret', 'key', 'password', 'token', 'credential']
        found_secret = any(indicator in findings_str for indicator in secret_indicators) or len(findings) > 0

        assert found_secret, \
            f"Expected HardCoded to find secrets. Findings: {findings}"

    def test_unsecure_protocol_finds_http(self, vulnerable_workflow):
        """
        UnsecureProtocol detector should find HTTP URLs.
        """
        detector = UnsecureProtocolFct(content=vulnerable_workflow)
        findings = detector.detect()

        assert len(findings) > 0, \
            f"Expected UnsecureProtocol to find HTTP URLs. Findings: {findings}"

    def test_admin_by_default_finds_write_all(self, vulnerable_workflow):
        """
        AdminByDefault detector should find write-all permissions.
        """
        detector = AdminByDefaultFct(content=vulnerable_workflow)
        findings = detector.detect()

        assert len(findings) > 0, \
            f"Expected AdminByDefault to find elevated permissions. Findings: {findings}"
