"""
Helper module for fetching GitHub repository workflows.
Uses sparse checkout to clone only .github/workflows/ directory efficiently.
"""
import subprocess
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def fetch_repo_workflows(repo: str, tmp_path_factory, branch: str = "main") -> Optional[Path]:
    """
    Clone only .github/workflows/ directory from a GitHub repository.
    Uses sparse checkout for efficiency - downloads only the workflow files.

    Args:
        repo: GitHub repository in format "owner/repo"
        tmp_path_factory: pytest tmp_path_factory fixture
        branch: Branch to clone (default: main)

    Returns:
        Path to the workflows directory, or None if clone fails

    """
    repo_name = repo.replace("/", "_")
    dest = tmp_path_factory.mktemp(repo_name)

    try:
        # Clone with sparse checkout (only metadata, no files)
        logger.info(f"Cloning workflows from {repo}...")
        subprocess.run(
            [
                "git", "clone",
                "--depth", "1",
                "--filter=blob:none",
                "--sparse",
                f"https://github.com/{repo}.git",
                str(dest)
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )

        # Configure sparse checkout to only get workflows
        subprocess.run(
            ["git", "sparse-checkout", "set", ".github/workflows"],
            cwd=dest,
            check=True,
            capture_output=True,
            text=True,
            timeout=60
        )

        workflows_path = dest / ".github" / "workflows"

        if workflows_path.exists():
            workflow_count = len(list(workflows_path.glob("*.yml"))) + len(list(workflows_path.glob("*.yaml")))
            logger.info(f"Successfully fetched {workflow_count} workflows from {repo}")
            return workflows_path
        else:
            logger.warning(f"No .github/workflows directory found in {repo}")
            return None

    except subprocess.TimeoutExpired:
        logger.error(f"Timeout cloning {repo}")
        return None
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to clone {repo}: {e.stderr}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error cloning {repo}: {e}")
        return None


def count_workflows(workflows_path: Path) -> int:
    """
    Count the number of workflow files in a directory.

    Args:
        workflows_path: Path to workflows directory

    Returns:
        Number of .yml and .yaml files
    """
    if not workflows_path or not workflows_path.exists():
        return 0
    yml_count = len(list(workflows_path.glob("*.yml")))
    yaml_count = len(list(workflows_path.glob("*.yaml")))
    return yml_count + yaml_count


def list_workflow_files(workflows_path: Path) -> list:
    """
    List all workflow files in a directory.

    Args:
        workflows_path: Path to workflows directory

    Returns:
        List of workflow file paths
    """
    if not workflows_path or not workflows_path.exists():
        return []
    yml_files = list(workflows_path.glob("*.yml"))
    yaml_files = list(workflows_path.glob("*.yaml"))
    return sorted(yml_files + yaml_files)
