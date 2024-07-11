from Analysis.Smells.Categories.Quality.LongBlocks.LongBlockSt import MainLongBlockCheck

import pytest
import logging
from Analysis.Parse.ActionParser import Action
from Analysis.Smells.Categories.Quality.LongBlocks.LongBlockSt import MainLongBlockCheck
from Analysis.Smells.Categories.Quality.LongBlocks.LongBlockFct import LongBlockFct

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def workflow():
    action = Action(file_path='../../Yamls/Smells/Prisma/test-template.yml')
    workflow = action.prepare_for_analysis()
    return workflow


def test_long_block(workflow):
    checker = MainLongBlockCheck()
    findings = checker.long_block_check(workflow)

    expected_findings = [
        "The job 'no-docker' has more than 16 steps. Consider splitting the steps "
        'into multiple jobs. A longer job can be difficult to maintain and debug and '
        'can lead to security vulnerabilities.',
        "The job 'others' has more than 12 steps. Consider splitting the steps into "
        'multiple jobs. A longer job can be difficult to maintain and debug and can '
        'lead to security vulnerabilities.',
        'The workflow has more than 17 jobs. Consider splitting the jobs into '
        'multiple workflows. A longer pipeline can be difficult to maintain and debug '
        'and can lead to security vulnerabilities.'
    ]

    assert sorted(findings) == sorted(expected_findings)


def test_integration(workflow):
    checker = LongBlockFct(content=workflow)
    findings = checker.detect()

    expected_findings = [
        "The job 'no-docker' has more than 16 steps. Consider splitting the steps "
        'into multiple jobs. A longer job can be difficult to maintain and debug and '
        'can lead to security vulnerabilities.',
        "The job 'others' has more than 12 steps. Consider splitting the steps into "
        'multiple jobs. A longer job can be difficult to maintain and debug and can '
        'lead to security vulnerabilities.',
        'The workflow has more than 17 jobs. Consider splitting the jobs into '
        'multiple workflows. A longer pipeline can be difficult to maintain and debug '
        'and can lead to security vulnerabilities.'
    ]

    assert sorted(findings) == sorted(expected_findings)
