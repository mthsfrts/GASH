"""
E2E Test Scenario 6: Performance and Scalability
Tests the performance characteristics of GASH.

This scenario validates:
- Single workflow analysis completes within acceptable time (< 30 seconds)
- Batch analysis of 50+ workflows completes within acceptable time (< 5 minutes)
- Memory usage remains stable during batch processing
"""
import pytest
import logging
import subprocess
import sys
import os
import time
import shutil
import tempfile
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from Analysis.Parse.ActionParser import Action
from Analysis.Smells.Categories.Security.AdminByDefault.AdminByDefaultFct import AdminByDefaultFct
from Analysis.Smells.Categories.Security.HardCoded.HardCodedFct import HardCodedFct
from Analysis.Smells.Categories.Security.UnsecureProtocol.UnsecureProtocolFct import UnsecureProtocolFct
from Analysis.Smells.Categories.Security.RemoteTriggers.RemoteTriggersFct import RemoteRunFct
from Analysis.Smells.Categories.Maintenance.CodeReplica.CodeReplicaFct import CodeReplicaFct
from Analysis.Smells.Categories.Maintenance.ErrorHandling.ErrorHandlingFct import ErrorHandlingFct
from Analysis.Smells.Categories.Maintenance.Misconfiguration.MisconfigurationFct import MisconfigurationFct
from Analysis.Smells.Categories.Quality.LongBlocks.LongBlockFct import LongBlockFct

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Performance thresholds
SINGLE_WORKFLOW_TIMEOUT = 30  # seconds
BATCH_50_WORKFLOWS_TIMEOUT = 300  # 5 minutes
MEMORY_LIMIT_MB = 500  # MB


class TestSingleWorkflowPerformance:
    """
    Scenario 6.1: Single workflow performance
    Tests that single workflow analysis completes within acceptable time
    """

    @pytest.fixture
    def complex_workflow_path(self, fixtures_path):
        """Path to complex workflow (most comprehensive fixture)."""
        return fixtures_path / "complex_workflow.yml"

    def test_single_workflow_analysis_time(self, complex_workflow_path):
        """
        Single workflow analysis should complete within 30 seconds.
        """
        start_time = time.time()

        # Parse workflow
        action = Action(file_path=str(complex_workflow_path))
        workflow = action.prepare_for_analysis()

        # Run all detectors
        detectors = [
            AdminByDefaultFct(content=workflow),
            HardCodedFct(content=workflow),
            RemoteRunFct(content=workflow),
            UnsecureProtocolFct(content=workflow),
            CodeReplicaFct(content=workflow),
            ErrorHandlingFct(content=workflow),
            MisconfigurationFct(content=workflow),
            LongBlockFct(content=workflow),
        ]

        for detector in detectors:
            detector.detect()

        elapsed_time = time.time() - start_time
        logger.info(f"Single workflow analysis completed in {elapsed_time:.2f} seconds")

        assert elapsed_time < SINGLE_WORKFLOW_TIMEOUT, \
            f"Single workflow analysis took {elapsed_time:.2f}s, expected < {SINGLE_WORKFLOW_TIMEOUT}s"

    def test_parser_performance(self, complex_workflow_path):
        """
        YAML parsing should be fast (< 1 second for single file).
        """
        start_time = time.time()

        action = Action(file_path=str(complex_workflow_path))
        workflow = action.prepare_for_analysis()

        elapsed_time = time.time() - start_time
        logger.info(f"Parsing completed in {elapsed_time:.3f} seconds")

        assert elapsed_time < 1.0, \
            f"Parsing took {elapsed_time:.3f}s, expected < 1.0s"
        assert workflow is not None

    def test_individual_detector_performance(self, complex_workflow_path):
        """
        Each detector should complete within 5 seconds individually.
        """
        action = Action(file_path=str(complex_workflow_path))
        workflow = action.prepare_for_analysis()

        detectors = {
            'AdminByDefault': AdminByDefaultFct(content=workflow),
            'HardCoded': HardCodedFct(content=workflow),
            'RemoteTriggers': RemoteRunFct(content=workflow),
            'UnsecureProtocol': UnsecureProtocolFct(content=workflow),
            'CodeReplica': CodeReplicaFct(content=workflow),
            'ErrorHandling': ErrorHandlingFct(content=workflow),
            'Misconfiguration': MisconfigurationFct(content=workflow),
            'LongBlocks': LongBlockFct(content=workflow),
        }

        for name, detector in detectors.items():
            start_time = time.time()
            detector.detect()
            elapsed_time = time.time() - start_time

            logger.info(f"{name} completed in {elapsed_time:.3f} seconds")

            assert elapsed_time < 5.0, \
                f"{name} took {elapsed_time:.3f}s, expected < 5.0s"


class TestBatchWorkflowPerformance:
    """
    Scenario 6.2: Batch workflow performance
    Tests that batch analysis of multiple workflows completes within acceptable time
    """

    @pytest.fixture
    def batch_50_workflows_dir(self, fixtures_path, tmp_path):
        """
        Create a directory with 50+ workflow files for batch testing.
        Uses copies of existing fixtures to simulate a large repository.
        """
        batch_dir = tmp_path / "batch_50_test"
        batch_dir.mkdir()

        source_files = list(fixtures_path.glob("*.yml"))

        # Create 50+ files by copying and renaming
        file_count = 0
        while file_count < 55:
            for src_file in source_files:
                if file_count >= 55:
                    break
                # Skip malformed file for this test
                if "malformed" in src_file.name:
                    continue
                dst_file = batch_dir / f"workflow_{file_count:03d}_{src_file.name}"
                shutil.copy(src_file, dst_file)
                file_count += 1

        logger.info(f"Created {file_count} workflow files for batch testing")
        return batch_dir

    def test_batch_50_workflows_direct_analysis(self, batch_50_workflows_dir):
        """
        Direct analysis of 50+ workflows should complete within 5 minutes.
        """
        workflow_files = list(batch_50_workflows_dir.glob("*.yml"))
        assert len(workflow_files) >= 50, f"Expected 50+ files, got {len(workflow_files)}"

        start_time = time.time()
        analyzed_count = 0
        error_count = 0

        for workflow_file in workflow_files:
            try:
                action = Action(file_path=str(workflow_file))
                workflow = action.prepare_for_analysis()

                if workflow is None:
                    error_count += 1
                    continue

                # Run all detectors
                detectors = [
                    AdminByDefaultFct(content=workflow),
                    HardCodedFct(content=workflow),
                    RemoteRunFct(content=workflow),
                    UnsecureProtocolFct(content=workflow),
                    CodeReplicaFct(content=workflow),
                    ErrorHandlingFct(content=workflow),
                    MisconfigurationFct(content=workflow),
                    LongBlockFct(content=workflow),
                ]

                for detector in detectors:
                    detector.detect()

                analyzed_count += 1

            except Exception as e:
                logger.debug(f"Error analyzing {workflow_file.name}: {e}")
                error_count += 1

        elapsed_time = time.time() - start_time
        logger.info(f"Batch analysis: {analyzed_count} workflows in {elapsed_time:.2f} seconds")
        logger.info(f"Errors: {error_count}")

        assert elapsed_time < BATCH_50_WORKFLOWS_TIMEOUT, \
            f"Batch analysis took {elapsed_time:.2f}s, expected < {BATCH_50_WORKFLOWS_TIMEOUT}s"

        # At least 90% should be analyzed successfully
        success_rate = analyzed_count / len(workflow_files)
        assert success_rate >= 0.9, \
            f"Success rate {success_rate:.0%} is below 90%"

    def test_batch_analysis_throughput(self, batch_50_workflows_dir):
        """
        Batch analysis should maintain reasonable throughput (> 1 workflow/second).
        """
        workflow_files = list(batch_50_workflows_dir.glob("*.yml"))[:20]  # Use subset for throughput test

        start_time = time.time()
        analyzed_count = 0

        for workflow_file in workflow_files:
            try:
                action = Action(file_path=str(workflow_file))
                workflow = action.prepare_for_analysis()

                if workflow is None:
                    continue

                # Run a subset of detectors for throughput test
                AdminByDefaultFct(content=workflow).detect()
                HardCodedFct(content=workflow).detect()

                analyzed_count += 1
            except Exception:
                continue

        elapsed_time = time.time() - start_time
        throughput = analyzed_count / elapsed_time if elapsed_time > 0 else 0

        logger.info(f"Throughput: {throughput:.2f} workflows/second")

        assert throughput >= 1.0, \
            f"Throughput {throughput:.2f}/s is below 1.0/s minimum"


class TestMemoryStability:
    """
    Scenario 6.3: Memory stability during batch processing
    Tests that memory usage remains stable and within limits
    """

    def test_memory_does_not_grow_unbounded(self, fixtures_path, tmp_path):
        """
        Memory usage should not grow unbounded during repeated analysis.
        """
        try:
            import psutil
        except ImportError:
            pytest.skip("psutil not installed - skipping memory test")

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / (1024 * 1024)  # MB

        # Analyze same workflow multiple times
        workflow_path = fixtures_path / "complex_workflow.yml"

        for i in range(20):
            action = Action(file_path=str(workflow_path))
            workflow = action.prepare_for_analysis()

            if workflow:
                detectors = [
                    AdminByDefaultFct(content=workflow),
                    HardCodedFct(content=workflow),
                    CodeReplicaFct(content=workflow),
                    ErrorHandlingFct(content=workflow),
                ]

                for detector in detectors:
                    detector.detect()

        final_memory = process.memory_info().rss / (1024 * 1024)  # MB
        memory_growth = final_memory - initial_memory

        logger.info(f"Initial memory: {initial_memory:.1f} MB")
        logger.info(f"Final memory: {final_memory:.1f} MB")
        logger.info(f"Memory growth: {memory_growth:.1f} MB")

        # Memory growth should be reasonable (< 100 MB for 20 iterations)
        assert memory_growth < 100, \
            f"Memory grew by {memory_growth:.1f} MB, expected < 100 MB"

    def test_peak_memory_within_limits(self, fixtures_path):
        """
        Peak memory during analysis should stay within limits.
        """
        try:
            import psutil
        except ImportError:
            pytest.skip("psutil not installed - skipping memory test")

        process = psutil.Process(os.getpid())

        # Analyze complex workflow
        workflow_path = fixtures_path / "complex_workflow.yml"
        action = Action(file_path=str(workflow_path))
        workflow = action.prepare_for_analysis()

        if workflow:
            detectors = [
                AdminByDefaultFct(content=workflow),
                HardCodedFct(content=workflow),
                RemoteRunFct(content=workflow),
                UnsecureProtocolFct(content=workflow),
                CodeReplicaFct(content=workflow),
                ErrorHandlingFct(content=workflow),
                MisconfigurationFct(content=workflow),
                LongBlockFct(content=workflow),
            ]

            for detector in detectors:
                detector.detect()

        current_memory = process.memory_info().rss / (1024 * 1024)  # MB

        logger.info(f"Current memory usage: {current_memory:.1f} MB")

        assert current_memory < MEMORY_LIMIT_MB, \
            f"Memory usage {current_memory:.1f} MB exceeds limit of {MEMORY_LIMIT_MB} MB"


class TestScalabilityGenerated:
    """
    Scenario 6.5: Generated scalability fixtures
    Tests with programmatically generated workflow files
    """

    @pytest.fixture
    def generated_workflows_dir(self, tmp_path):
        """
        Generate 100 simple workflow files for scalability testing.
        """
        gen_dir = tmp_path / "generated_workflows"
        gen_dir.mkdir()

        template = """name: Generated Workflow {n}
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Step {n}
        run: echo "Workflow {n}"
"""

        for i in range(100):
            workflow_file = gen_dir / f"workflow_{i:03d}.yml"
            workflow_file.write_text(template.format(n=i))

        return gen_dir

    def test_100_simple_workflows_performance(self, generated_workflows_dir):
        """
        Analysis of 100 simple workflows should complete quickly.
        """
        workflow_files = list(generated_workflows_dir.glob("*.yml"))
        assert len(workflow_files) == 100

        start_time = time.time()
        analyzed_count = 0

        for workflow_file in workflow_files:
            try:
                action = Action(file_path=str(workflow_file))
                workflow = action.prepare_for_analysis()

                if workflow:
                    # Run minimal detectors for speed test
                    AdminByDefaultFct(content=workflow).detect()
                    analyzed_count += 1
            except Exception:
                continue

        elapsed_time = time.time() - start_time

        logger.info(f"100 simple workflows analyzed in {elapsed_time:.2f}s")
        logger.info(f"Success: {analyzed_count}/100")

        # 100 simple workflows should complete in under 60 seconds
        assert elapsed_time < 60, \
            f"Analysis took {elapsed_time:.2f}s, expected < 60s"

        assert analyzed_count >= 95, \
            f"Only {analyzed_count}/100 workflows analyzed successfully"

    def test_scalability_linear_growth(self, generated_workflows_dir):
        """
        Analysis time should grow roughly linearly with number of files.
        """
        workflow_files = list(generated_workflows_dir.glob("*.yml"))

        # Time for 10 files
        start_time = time.time()
        for wf in workflow_files[:10]:
            try:
                action = Action(file_path=str(wf))
                workflow = action.prepare_for_analysis()
                if workflow:
                    AdminByDefaultFct(content=workflow).detect()
            except Exception:
                pass
        time_10 = time.time() - start_time

        # Time for 50 files
        start_time = time.time()
        for wf in workflow_files[:50]:
            try:
                action = Action(file_path=str(wf))
                workflow = action.prepare_for_analysis()
                if workflow:
                    AdminByDefaultFct(content=workflow).detect()
            except Exception:
                pass
        time_50 = time.time() - start_time

        logger.info(f"10 files: {time_10:.3f}s, 50 files: {time_50:.3f}s")

        # Time for 50 should be roughly 5x time for 10 (allowing 3x margin)
        expected_max = time_10 * 15  # Allow significant margin for overhead
        assert time_50 < expected_max, \
            f"Time scaling is non-linear: 10 files={time_10:.3f}s, 50 files={time_50:.3f}s"
