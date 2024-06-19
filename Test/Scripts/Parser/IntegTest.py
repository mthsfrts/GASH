import yaml
from Analysis.Parse.ActionParser import Action


def test_prepare_for_analysis():
    with open('../../Yamls/Parser/simple.yaml', 'r') as file:
        content = file.read()
    action = Action(content=content)
    workflow = action.prepare_for_analysis()
    assert workflow.name == 'DataStruct Workflow'
    assert 'push' in workflow.on
    assert 'test_job' in workflow.jobs
    job = workflow.jobs['test_job']
    assert job.name == 'test_job'
    assert job.runs_on == 'ubuntu-latest'
    assert len(job.steps) == 2
    step = job.steps[0]
    assert step.name == 'Checkout code'
    assert step.uses == 'actions/checkout@v2'


def test_multiple_jobs():
    with open('../../Yamls/Parser/multijobs.yaml', 'r') as file:
        content = file.read()
    action = Action(content=content)
    workflow = action.prepare_for_analysis()
    assert workflow.name == 'Multiple Jobs Workflow'
    assert 'push' in workflow.on
    assert 'job1' in workflow.jobs
    assert 'job2' in workflow.jobs

    job1 = workflow.jobs['job1']
    assert job1.name == 'job1'
    assert job1.runs_on == 'ubuntu-latest'
    assert len(job1.steps) == 1
    assert job1.steps[0].name == 'Step 1'
    assert job1.steps[0].run == 'echo "Job 1 - Step 1"'

    job2 = workflow.jobs['job2']
    assert job2.name == 'job2'
    assert job2.runs_on == 'ubuntu-latest'
    assert len(job2.steps) == 1
    assert job2.steps[0].name == 'Step 1'
    assert job2.steps[0].run == 'echo "Job 2 - Step 1"'


def test_optional_parameters():
    with open('../../Yamls/Parser/optionalparams.yaml', 'r') as file:
        content = file.read()
    action = Action(content=content)
    workflow = action.prepare_for_analysis()
    assert workflow.name == 'Workflow with Optional Params'
    assert 'push' in workflow.on
    assert 'test_job' in workflow.jobs

    job = workflow.jobs['test_job']
    assert job.name == 'test_job'
    assert job.runs_on == 'ubuntu-latest'
    assert job.concurrency == 'group-1'
    assert job.permissions == {'actions': 'read'}
    assert len(job.steps) == 1
    assert job.steps[0].name == 'Checkout code'
    assert job.steps[0].uses == 'actions/checkout@v2'


def test_steps_with_different_commands():
    with open('../../Yamls/Parser/diffcommands.yaml', 'r') as file:
        content = file.read()
    action = Action(content=content)
    workflow = action.prepare_for_analysis()
    assert workflow.name == 'Workflow with Different Commands'
    assert 'push' in workflow.on
    assert 'test_job' in workflow.jobs

    job = workflow.jobs['test_job']
    assert job.name == 'test_job'
    assert job.runs_on == 'ubuntu-latest'
    assert len(job.steps) == 3

    step1 = job.steps[0]
    assert step1.name == 'Checkout code'
    assert step1.uses == 'actions/checkout@v2'

    step2 = job.steps[1]
    assert step2.name == 'Run tests'
    assert step2.run == 'pytest'

    step3 = job.steps[2]
    assert step3.name == 'Set up environment'
    assert step3.run == 'echo $TEST_VAR'
    assert step3.env == {'TEST_VAR': 'test_value'}


def test_default_values():
    with open('../../Yamls/Parser/nonevalues.yaml', 'r') as file:
        content = file.read()
    action = Action(content=content)
    workflow = action.prepare_for_analysis()
    assert workflow.name == 'Workflow with Default Values'
    assert 'push' in workflow.on
    assert 'test_job' in workflow.jobs

    job = workflow.jobs['test_job']
    assert job.name == 'test_job'
    assert job.runs_on == 'ubuntu-latest'
    assert len(job.steps) == 1

    step = job.steps[0]
    assert step.name == 'Checkout code'
    assert step.run == 'echo "Checking out code"'
    assert step.uses is None  # Ensure 'uses' is None since it wasn't provided


def test_parsing_errors():
    with open('../../Yamls/Parser/invalid.yaml', 'r') as file:
        content = file.read()

    action = Action(content=content)
    try:
        workflow = action.prepare_for_analysis()
        assert workflow is None, "Parsing did not fail for invalid YAML"  # This should not be reached
    except yaml.YAMLError as e:
        print(f"YAML parsing error: {e}")
        assert True  # Expected to catch a parsing error


def test_conditional_workflow():
    with open('../../Yamls/Parser/conditionals.yaml', 'r') as file:
        content = file.read()

    action = Action(content=content)
    workflow = action.prepare_for_analysis()

    assert workflow.name == 'Conditional Workflow'
    assert 'push' in workflow.on
    assert 'test_job' in workflow.jobs

    job = workflow.jobs['test_job']
    assert job.name == 'test_job'
    assert job.runs_on == 'ubuntu-latest'
    assert job._if == "github.ref == 'refs/heads/main'"

    assert len(job.steps) == 3

    step1 = job.steps[0]
    assert step1.name == 'Checkout code'
    assert step1.uses == 'actions/checkout@v2'

    step2 = job.steps[1]
    assert step2.name == 'Run tests'
    assert step2._if == 'success()'
    assert step2.run == 'pytest'
    assert step2.with_params['python-version'] == '3.8'

    step3 = job.steps[2]
    assert step3.name == 'Set up environment'
    assert step3.run == 'echo $TEST_VAR'
    assert step3.env['TEST_VAR'] == 'test_value'


def test_input_output_workflow():
    with open('../../Yamls/Parser/i_o.yaml', 'r') as file:
        content = file.read()

    action = Action(content=content)
    workflow = action.prepare_for_analysis()

    assert workflow.name == 'Input Output Workflow'
    assert 'push' in workflow.on
    assert 'test_job' in workflow.jobs

    job = workflow.jobs['test_job']
    assert job.name == 'test_job'
    assert job.runs_on == 'ubuntu-latest'

    assert len(job.steps) == 2

    step1 = job.steps[0]
    assert step1.name == 'Checkout code'
    assert step1.uses == 'actions/checkout@v2'

    step2 = job.steps[1]
    assert step2.name == 'Use input'
    assert step2.run == 'echo ${{ inputs.example_input }}'

    assert 'example_output' in job.outputs


def test_containers_workflow():
    with open('../../Yamls/Parser/container.yaml', 'r') as file:
        content = file.read()

    action = Action(content=content)
    workflow = action.prepare_for_analysis()

    assert workflow.name == 'Container Workflow'
    assert 'push' in workflow.on
    assert 'test_job' in workflow.jobs

    job = workflow.jobs['test_job']
    assert job.name == 'test_job'
    assert job.runs_on == 'ubuntu-latest'
    assert job.container['image'] == 'node:14'

    assert len(job.steps) == 3

    step1 = job.steps[0]
    assert step1.name == 'Checkout code'
    assert step1.uses == 'actions/checkout@v2'

    step2 = job.steps[1]
    assert step2.name == 'Install dependencies'
    assert step2.run == 'npm install'

    step3 = job.steps[2]
    assert step3.name == 'Run build'
    assert step3.run == 'npm run build'


def test_defaults_workflow():
    with open('../../Yamls/Parser/defaults.yaml', 'r') as file:
        content = file.read()

    action = Action(content=content)
    workflow = action.prepare_for_analysis()

    assert workflow.name == 'Defaults Workflow'
    assert 'push' in workflow.on
    assert 'test_job' in workflow.jobs

    job = workflow.jobs['test_job']
    assert job.name == 'test_job'
    assert job.runs_on == 'ubuntu-latest'

    assert workflow.defaults['run']['shell'] == 'bash'
    assert workflow.defaults['run']['working-directory'] == 'scripts'

    assert len(job.steps) == 2

    step1 = job.steps[0]
    assert step1.name == 'Checkout code'
    assert step1.uses == 'actions/checkout@v2'

    step2 = job.steps[1]
    assert step2.name == 'Run script'
    assert step2.run == './deploy.sh'


def test_continue_on_error_workflow():
    with open('../../Yamls/Parser/continueonerro.yaml', 'r') as file:
        content = file.read()

    action = Action(content=content)
    workflow = action.prepare_for_analysis()

    assert workflow.name == 'Continue on Error Workflow'
    assert 'push' in workflow.on
    assert 'test_job' in workflow.jobs

    job = workflow.jobs['test_job']
    assert job.name == 'test_job'
    assert job.runs_on == 'ubuntu-latest'

    assert len(job.steps) == 3

    step1 = job.steps[0]
    assert step1.name == 'Checkout code'
    assert step1.uses == 'actions/checkout@v2'

    step2 = job.steps[1]
    assert step2.name == 'Run tests'
    assert step2.run == 'pytest'
    assert step2.continue_on_error == 'true'

    step3 = job.steps[2]
    assert step3.name == 'Deploy'
    assert step3.run == './deploy.sh'


def test_needs_workflow():
    with open('../../Yamls/Parser/needs.yaml', 'r') as file:
        content = file.read()

    action = Action(content=content)
    workflow = action.prepare_for_analysis()

    assert workflow.name == 'Needs Workflow'
    assert 'push' in workflow.on
    assert 'build' in workflow.jobs
    assert 'test' in workflow.jobs

    build_job = workflow.jobs['build']
    assert build_job.name == 'build'
    assert build_job.runs_on == 'ubuntu-latest'

    assert len(build_job.steps) == 2

    build_step1 = build_job.steps[0]
    assert build_step1.name == 'Checkout code'
    assert build_step1.uses == 'actions/checkout@v2'

    build_step2 = build_job.steps[1]
    assert build_step2.name == 'Build'
    assert build_step2.run == 'make build'

    test_job = workflow.jobs['test']
    assert test_job.name == 'test'
    assert test_job.runs_on == 'ubuntu-latest'
    assert 'build' in test_job.needs

    assert len(test_job.steps) == 2

    test_step1 = test_job.steps[0]
    assert test_step1.name == 'Checkout code'
    assert test_step1.uses == 'actions/checkout@v2'

    test_step2 = test_job.steps[1]
    assert test_step2.name == 'Run tests'
    assert test_step2.run == 'make test'


def test_service_workflow():
    with open('../../Yamls/Parser/services.yaml', 'r') as file:
        content = file.read()

    action = Action(content=content)
    workflow = action.prepare_for_analysis()

    assert workflow.name == 'Service Workflow'
    assert 'push' in workflow.on
    assert 'test_job' in workflow.jobs

    job = workflow.jobs['test_job']
    assert job.name == 'test_job'
    assert job.runs_on == 'ubuntu-latest'
    assert 'postgres' in job.services
    assert job.services['postgres']['image'] == 'postgres:latest'
    assert job.services['postgres']['ports'] == ['5432:5432']

    assert len(job.steps) == 2

    step1 = job.steps[0]
    assert step1.name == 'Checkout code'
    assert step1.uses == 'actions/checkout@v2'

    step2 = job.steps[1]
    assert step2.name == 'Run tests'
    assert step2.run == 'pytest'
    assert step2.env['DATABASE_URL'] == 'postgres://postgres:postgres@localhost:5432/test'


def test_strategy_workflow():
    with open('../../Yamls/Parser/strategy.yaml', 'r') as file:
        content = file.read()

    action = Action(content=content)
    workflow = action.prepare_for_analysis()

    assert workflow.name == 'Strategy Workflow'
    assert 'push' in workflow.on
    assert 'test_job' in workflow.jobs

    job = workflow.jobs['test_job']
    assert job.name == 'test_job'
    assert job.runs_on == 'ubuntu-latest'
    assert 'matrix' in job.strategy
    assert job.strategy['matrix']['python-version'] == [3.6, 3.7, 3.8, 3.9]

    assert len(job.steps) == 4

    step1 = job.steps[0]
    assert step1.name == 'Checkout code'
    assert step1.uses == 'actions/checkout@v2'

    step2 = job.steps[1]
    assert step2.name == 'Setup Python'
    assert step2.uses == 'actions/setup-python@v2'
    assert step2.with_params['python-version'] == '${{ matrix.python-version }}'

    step3 = job.steps[2]
    assert step3.name == 'Install dependencies'
    assert step3.run == 'pip install -r requirements.txt'

    step4 = job.steps[3]
    assert step4.name == 'Run tests'
    assert step4.run == 'pytest'


def test_timeout_workflow():
    with open('../../Yamls/Parser/timeout.yaml', 'r') as file:
        content = file.read()

    action = Action(content=content)
    workflow = action.prepare_for_analysis()

    assert workflow.name == 'Timeout Workflow'
    assert 'push' in workflow.on
    assert 'test_job' in workflow.jobs

    job = workflow.jobs['test_job']
    assert job.name == 'test_job'
    assert job.runs_on == 'ubuntu-latest'
    assert job.timeout_minutes == 10

    assert len(job.steps) == 2

    step1 = job.steps[0]
    assert step1.name == 'Checkout code'
    assert step1.uses == 'actions/checkout@v2'

    step2 = job.steps[1]
    assert step2.name == 'Run long task'
    assert step2.run == 'sleep 600'
