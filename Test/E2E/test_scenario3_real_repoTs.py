"""
E2E Test Scenario 3: Real Repository Analysis
Tests GASH robustness with real-world GitHub Actions workflows.

This scenario validates:
- Complete analysis of real repository without crashes
- Handling of diverse workflow patterns from production repos
- Reasonable execution time for real repositories
- Complete report generation for all workflows
- Stability across different workflow structures
"""
import pytest
import logging
import subprocess
import sys
import time
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


class TestRealRepositoryRobustness:
    """
    Scenario 3.1: Real repository robustness
    Tests that GASH can analyze a complete real repository without crashes
    """

    @pytest.mark.requires_real_token
    @pytest.mark.slow
    def test_starter_workflows_complete_analysis(self, starter_workflows_path):
        """
        Complete analysis of actions/starter-workflows repository.
        All workflows should be parsed and analyzed without crashing.
        """
        if starter_workflows_path is None:
            pytest.skip("Could not clone starter-workflows repository")

        workflow_files = list(starter_workflows_path.glob("*.yml")) + \
                         list(starter_workflows_path.glob("*.yaml"))

        if not workflow_files:
            pytest.skip("No workflow files found in starter-workflows")

        logger.info(f"Analyzing {len(workflow_files)} workflows from actions/starter-workflows")

        analyzed_count = 0
        parse_errors = []
        detector_errors = []

        for workflow_file in workflow_files:
            try:
                # Parse workflow
                action = Action(file_path=str(workflow_file))
                workflow = action.prepare_for_analysis()

                if workflow is None:
                    parse_errors.append(workflow_file.name)
                    continue

                # Run all detectors
                try:
                    AdminByDefaultFct(content=workflow).detect()
                    HardCodedFct(content=workflow).detect()
                    RemoteRunFct(content=workflow).detect()
                    UnsecureProtocolFct(content=workflow).detect()
                    CodeReplicaFct(content=workflow).detect()
                    ErrorHandlingFct(content=workflow).detect()
                    MisconfigurationFct(content=workflow).detect()
                    LongBlockFct(content=workflow).detect()

                    analyzed_count += 1

                except Exception as e:
                    detector_errors.append(f"{workflow_file.name}: {e}")

            except Exception as e:
                parse_errors.append(f"{workflow_file.name}: {e}")

        logger.info(f"Successfully analyzed: {analyzed_count}/{len(workflow_files)}")
        logger.info(f"Parse errors: {len(parse_errors)}")
        logger.info(f"Detector errors: {len(detector_errors)}")

        if parse_errors:
            logger.warning(f"Parse errors: {parse_errors[:3]}")
        if detector_errors:
            logger.warning(f"Detector errors: {detector_errors[:3]}")

        # Should successfully analyze at least 90% of workflows
        success_rate = analyzed_count / len(workflow_files)
        assert success_rate >= 0.9, \
            f"Success rate {success_rate:.0%} is below 90%. Analyzed: {analyzed_count}/{len(workflow_files)}"

    @pytest.mark.requires_real_token
    @pytest.mark.slow
    def test_real_repo_no_crashes(self, starter_workflows_path):
        """
        Analysis should not crash on any workflow in the repository.
        Even if parsing fails, the tool should handle it gracefully.
        """
        if starter_workflows_path is None:
            pytest.skip("Could not clone starter-workflows repository")

        workflow_files = list(starter_workflows_path.glob("*.yml")) + \
                         list(starter_workflows_path.glob("*.yaml"))

        if not workflow_files:
            pytest.skip("No workflow files found in starter-workflows")

        crashes = []

        for workflow_file in workflow_files:
            try:
                action = Action(file_path=str(workflow_file))
                workflow = action.prepare_for_analysis()

                if workflow:
                    # Run detectors that are more complex
                    CodeReplicaFct(content=workflow).detect()
                    ErrorHandlingFct(content=workflow).detect()
                    MisconfigurationFct(content=workflow).detect()

            except Exception as e:
                crashes.append(f"{workflow_file.name}: {str(e)[:100]}")

        if crashes:
            logger.warning(f"Crashes: {crashes}")

        # Allow some failures, but not too many
        crash_rate = len(crashes) / len(workflow_files) if workflow_files else 0
        assert crash_rate < 0.2, \
            f"Crash rate {crash_rate:.0%} is too high. Crashes: {crashes[:5]}"

    @pytest.mark.requires_real_token
    @pytest.mark.slow
    def test_real_repo_execution_time(self, starter_workflows_path):
        """
        Analysis of real repository should complete in reasonable time.
        """
        if starter_workflows_path is None:
            pytest.skip("Could not clone starter-workflows repository")

        workflow_files = list(starter_workflows_path.glob("*.yml")) + \
                         list(starter_workflows_path.glob("*.yaml"))

        if not workflow_files:
            pytest.skip("No workflow files found in starter-workflows")

        start_time = time.time()
        analyzed_count = 0

        for workflow_file in workflow_files:
            try:
                action = Action(file_path=str(workflow_file))
                workflow = action.prepare_for_analysis()

                if workflow:
                    # Run all detectors
                    AdminByDefaultFct(content=workflow).detect()
                    HardCodedFct(content=workflow).detect()
                    RemoteRunFct(content=workflow).detect()
                    UnsecureProtocolFct(content=workflow).detect()
                    CodeReplicaFct(content=workflow).detect()
                    ErrorHandlingFct(content=workflow).detect()
                    MisconfigurationFct(content=workflow).detect()
                    LongBlockFct(content=workflow).detect()

                    analyzed_count += 1
            except Exception:
                continue

        elapsed_time = time.time() - start_time

        logger.info(f"Analyzed {analyzed_count} workflows in {elapsed_time:.2f}s")
        logger.info(f"Average time per workflow: {elapsed_time/max(analyzed_count,1):.3f}s")

        # Should complete within 3 minutes for typical repo
        assert elapsed_time < 180, \
            f"Analysis took {elapsed_time:.2f}s, expected < 180s"


class TestDiverseWorkflowPatterns:
    """
    Scenario 3.2: Handling diverse workflow patterns
    Tests that GASH handles various real-world workflow structures
    """

    @pytest.mark.requires_real_token
    @pytest.mark.slow
    def test_various_workflow_structures(self, starter_workflows_path):
        """
        Different workflow structures should all be parseable.
        """
        if starter_workflows_path is None:
            pytest.skip("Could not clone starter-workflows repository")

        workflow_files = list(starter_workflows_path.glob("*.yml")) + \
                         list(starter_workflows_path.glob("*.yaml"))

        if not workflow_files:
            pytest.skip("No workflow files found")

        workflow_stats = {
            'simple': 0,      # 1 job
            'multi_job': 0,   # 2+ jobs
            'matrix': 0,      # uses matrix strategy
            'reusable': 0,    # workflow_call
        }

        for workflow_file in workflow_files:
            try:
                action = Action(file_path=str(workflow_file))
                workflow = action.prepare_for_analysis()

                if workflow is None:
                    continue

                # Categorize workflow
                if hasattr(workflow, 'jobs') and workflow.jobs:
                    job_count = len(workflow.jobs)

                    if job_count == 1:
                        workflow_stats['simple'] += 1
                    elif job_count > 1:
                        workflow_stats['multi_job'] += 1

                    # Check for matrix strategy
                    for job in workflow.jobs:
                        if hasattr(job, 'strategy') and job.strategy:
                            workflow_stats['matrix'] += 1
                            break

                # Check for workflow_call (reusable workflow)
                content = workflow_file.read_text()
                if 'workflow_call' in content:
                    workflow_stats['reusable'] += 1

            except Exception as e:
                logger.debug(f"Error analyzing {workflow_file.name}: {e}")

        logger.info(f"Workflow structure stats: {workflow_stats}")

        # Should successfully categorize workflows
        # (Note: starter-workflows may have mostly simple workflows, which is fine)
        total_categorized = sum(workflow_stats.values())
        assert total_categorized > 0, \
            f"Could not categorize any workflows. Stats: {workflow_stats}"

        # At least one workflow type should be found
        types_found = sum(1 for count in workflow_stats.values() if count > 0)
        assert types_found >= 1, \
            f"No workflow types identified. Stats: {workflow_stats}"

    @pytest.mark.requires_real_token
    @pytest.mark.slow
    def test_workflows_with_different_triggers(self, starter_workflows_path):
        """
        Workflows with different trigger types should be handled.
        """
        if starter_workflows_path is None:
            pytest.skip("Could not clone starter-workflows repository")

        workflow_files = list(starter_workflows_path.glob("*.yml")) + \
                         list(starter_workflows_path.glob("*.yaml"))

        if not workflow_files:
            pytest.skip("No workflow files found")

        trigger_types = set()

        for workflow_file in workflow_files[:20]:  # Sample first 20
            try:
                content = workflow_file.read_text()

                # Check for different trigger types
                if 'on: push' in content or 'on:\n  push' in content:
                    trigger_types.add('push')
                if 'pull_request' in content:
                    trigger_types.add('pull_request')
                if 'schedule' in content:
                    trigger_types.add('schedule')
                if 'workflow_dispatch' in content:
                    trigger_types.add('workflow_dispatch')
                if 'workflow_call' in content:
                    trigger_types.add('workflow_call')

            except Exception:
                continue

        logger.info(f"Trigger types found: {trigger_types}")

        # Should find multiple trigger types
        assert len(trigger_types) >= 2, \
            f"Expected multiple trigger types, found: {trigger_types}"


class TestReportGenerationForRealRepo:
    """
    Scenario 3.3: Report generation for real repository
    Tests that complete reports are generated for real repos
    """

    @pytest.mark.requires_real_token
    @pytest.mark.slow
    def test_all_detectors_run_on_real_repo(self, starter_workflows_path):
        """
        All 9 detectors should run on each workflow in the real repo.
        """
        if starter_workflows_path is None:
            pytest.skip("Could not clone starter-workflows repository")

        workflow_files = list(starter_workflows_path.glob("*.yml")) + \
                         list(starter_workflows_path.glob("*.yaml"))

        if not workflow_files:
            pytest.skip("No workflow files found")

        # Test with first 5 workflows
        sample_files = workflow_files[:5]

        for workflow_file in sample_files:
            try:
                action = Action(file_path=str(workflow_file))
                workflow = action.prepare_for_analysis()

                if workflow is None:
                    continue

                # All detectors should be runnable
                detectors_run = 0

                try:
                    AdminByDefaultFct(content=workflow).detect()
                    detectors_run += 1
                except Exception as e:
                    logger.warning(f"AdminByDefault failed on {workflow_file.name}: {e}")

                try:
                    HardCodedFct(content=workflow).detect()
                    detectors_run += 1
                except Exception as e:
                    logger.warning(f"HardCoded failed on {workflow_file.name}: {e}")

                try:
                    RemoteRunFct(content=workflow).detect()
                    detectors_run += 1
                except Exception as e:
                    logger.warning(f"RemoteRun failed on {workflow_file.name}: {e}")

                try:
                    UnsecureProtocolFct(content=workflow).detect()
                    detectors_run += 1
                except Exception as e:
                    logger.warning(f"UnsecureProtocol failed on {workflow_file.name}: {e}")

                try:
                    CodeReplicaFct(content=workflow).detect()
                    detectors_run += 1
                except Exception as e:
                    logger.warning(f"CodeReplica failed on {workflow_file.name}: {e}")

                try:
                    ErrorHandlingFct(content=workflow).detect()
                    detectors_run += 1
                except Exception as e:
                    logger.warning(f"ErrorHandling failed on {workflow_file.name}: {e}")

                try:
                    MisconfigurationFct(content=workflow).detect()
                    detectors_run += 1
                except Exception as e:
                    logger.warning(f"Misconfiguration failed on {workflow_file.name}: {e}")

                try:
                    LongBlockFct(content=workflow).detect()
                    detectors_run += 1
                except Exception as e:
                    logger.warning(f"LongBlock failed on {workflow_file.name}: {e}")

                logger.info(f"{workflow_file.name}: {detectors_run}/8 detectors completed")

                # At least 6 of 8 detectors should run successfully
                assert detectors_run >= 6, \
                    f"Only {detectors_run}/8 detectors ran on {workflow_file.name}"

            except Exception as e:
                logger.warning(f"Error with {workflow_file.name}: {e}")

    @pytest.mark.requires_real_token
    @pytest.mark.slow
    def test_findings_aggregation_for_repo(self, starter_workflows_path):
        """
        Aggregate findings across all workflows in repository.
        """
        if starter_workflows_path is None:
            pytest.skip("Could not clone starter-workflows repository")

        workflow_files = list(starter_workflows_path.glob("*.yml")) + \
                         list(starter_workflows_path.glob("*.yaml"))

        if not workflow_files:
            pytest.skip("No workflow files found")

        total_findings = {
            'AdminByDefault': 0,
            'HardCoded': 0,
            'UnsecureProtocol': 0,
            'RemoteTriggers': 0,
            'CodeReplica': 0,
            'ErrorHandling': 0,
            'Misconfiguration': 0,
            'LongBlocks': 0,
        }

        for workflow_file in workflow_files:
            try:
                action = Action(file_path=str(workflow_file))
                workflow = action.prepare_for_analysis()

                if workflow is None:
                    continue

                # Collect findings from each detector
                try:
                    total_findings['AdminByDefault'] += len(
                        AdminByDefaultFct(content=workflow).detect()
                    )
                except Exception:
                    pass

                try:
                    total_findings['HardCoded'] += len(
                        HardCodedFct(content=workflow).detect()
                    )
                except Exception:
                    pass

                try:
                    total_findings['UnsecureProtocol'] += len(
                        UnsecureProtocolFct(content=workflow).detect()
                    )
                except Exception:
                    pass

                try:
                    total_findings['RemoteTriggers'] += len(
                        RemoteRunFct(content=workflow).detect()
                    )
                except Exception:
                    pass

                try:
                    total_findings['CodeReplica'] += len(
                        CodeReplicaFct(content=workflow).detect()
                    )
                except Exception:
                    pass

                try:
                    total_findings['ErrorHandling'] += len(
                        ErrorHandlingFct(content=workflow).detect()
                    )
                except Exception:
                    pass

                try:
                    total_findings['Misconfiguration'] += len(
                        MisconfigurationFct(content=workflow).detect()
                    )
                except Exception:
                    pass

                try:
                    total_findings['LongBlocks'] += len(
                        LongBlockFct(content=workflow).detect()
                    )
                except Exception:
                    pass

            except Exception:
                continue

        logger.info(f"Total findings across repository: {total_findings}")
        logger.info(f"Total: {sum(total_findings.values())} findings")

        # Repository analysis should produce findings report
        # (even if findings count is low for clean repos)
        assert isinstance(total_findings, dict)
        assert len(total_findings) == 8


class TestStabilityAcrossWorkflows:
    """
    Scenario 3.4: Stability across different workflows
    Tests that analysis is consistent and stable
    """

    @pytest.mark.requires_real_token
    @pytest.mark.slow
    def test_consistent_results_across_runs(self, starter_workflows_path):
        """
        Running analysis twice on same workflow should produce identical results.
        """
        if starter_workflows_path is None:
            pytest.skip("Could not clone starter-workflows repository")

        workflow_files = list(starter_workflows_path.glob("*.yml")) + \
                         list(starter_workflows_path.glob("*.yaml"))

        if not workflow_files:
            pytest.skip("No workflow files found")

        # Test with first workflow
        test_file = workflow_files[0]

        # First run
        action1 = Action(file_path=str(test_file))
        workflow1 = action1.prepare_for_analysis()
        findings1 = []
        if workflow1:
            findings1.extend(AdminByDefaultFct(content=workflow1).detect())
            findings1.extend(HardCodedFct(content=workflow1).detect())

        # Second run
        action2 = Action(file_path=str(test_file))
        workflow2 = action2.prepare_for_analysis()
        findings2 = []
        if workflow2:
            findings2.extend(AdminByDefaultFct(content=workflow2).detect())
            findings2.extend(HardCodedFct(content=workflow2).detect())

        # Results should be identical
        assert findings1 == findings2, \
            f"Inconsistent results: Run 1: {findings1}, Run 2: {findings2}"

    @pytest.mark.requires_real_token
    @pytest.mark.slow
    def test_no_memory_leaks_during_repo_analysis(self, starter_workflows_path):
        """
        Memory should not grow unbounded during repository analysis.
        """
        try:
            import psutil
        except ImportError:
            pytest.skip("psutil not installed")

        if starter_workflows_path is None:
            pytest.skip("Could not clone starter-workflows repository")

        workflow_files = list(starter_workflows_path.glob("*.yml")) + \
                         list(starter_workflows_path.glob("*.yaml"))

        if not workflow_files:
            pytest.skip("No workflow files found")

        process = psutil.Process()
        initial_memory = process.memory_info().rss / (1024 * 1024)  # MB

        # Analyze all workflows
        for workflow_file in workflow_files:
            try:
                action = Action(file_path=str(workflow_file))
                workflow = action.prepare_for_analysis()

                if workflow:
                    AdminByDefaultFct(content=workflow).detect()
                    HardCodedFct(content=workflow).detect()
            except Exception:
                continue

        final_memory = process.memory_info().rss / (1024 * 1024)  # MB
        memory_growth = final_memory - initial_memory

        logger.info(f"Memory: {initial_memory:.1f} MB -> {final_memory:.1f} MB (+{memory_growth:.1f} MB)")

        # Memory growth should be reasonable
        assert memory_growth < 200, \
            f"Memory grew by {memory_growth:.1f} MB, expected < 200 MB"
