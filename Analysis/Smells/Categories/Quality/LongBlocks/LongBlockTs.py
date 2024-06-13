from Analysis.Smells.Categories.Quality.LongBlocks.LongBlockSt import MainLongBlockCheck

import pytest
import logging
from Analysis.Parse.ActionParser import Action
from Analysis.Smells.Categories.Quality.LongBlocks.LongBlockSt import MainLongBlockCheck
from Analysis.Smells.Categories.Quality.LongBlocks.LongBlockFct import LongBlockFct

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def workflow():
    action = Action(file_path='LongBlock.yaml')
    workflow = action.prepare_for_analysis()
    return workflow


def test_long_block(workflow):
    checker = MainLongBlockCheck()
    findings = checker.long_block_check(workflow)

    expected_findings = [
        "The job 'job2' has more than 11 steps. Consider splitting the steps into "
        'multiple jobs. A longer job can be difficult to maintain and debug and can '
        'lead to security vulnerabilities.',

        "The step 'Step 1' run has more than 22 commands. Consider splitting the "
        'commands into multiple step groups. A longer step group can be difficult to '
        'maintain and debug and can lead to security vulnerabilities.',

        'The workflow has more than 11 jobs. Consider splitting the jobs into '
        'multiple workflows. A longer pipeline can be difficult to maintain and debug '
        'and can lead to security vulnerabilities.'
    ]

    assert sorted(findings) == sorted(expected_findings)


def test_integration(workflow):
    checker = LongBlockFct(content=workflow)
    findings = checker.detect()

    expected_findings = [
        "The job 'job2' has more than 11 steps. Consider splitting the steps into "
        'multiple jobs. A longer job can be difficult to maintain and debug and can '
        'lead to security vulnerabilities.',

        "The step 'Step 1' run has more than 22 commands. Consider splitting the "
        'commands into multiple step groups. A longer step group can be difficult to '
        'maintain and debug and can lead to security vulnerabilities.',

        'The workflow has more than 11 jobs. Consider splitting the jobs into '
        'multiple workflows. A longer pipeline can be difficult to maintain and debug '
        'and can lead to security vulnerabilities.'
    ]

    assert sorted(findings) == sorted(expected_findings)
