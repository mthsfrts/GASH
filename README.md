# GASH - GitHub Actions Smells Hunter
## Overview

GASH (GitHub Actions Smell Hunter) is a Python-based tool primarily devoted to identifying configuration smells in CI/CD pipelines deployed on GitHub Actions. It can parser YAML files describing CI/CD workflows looking at identifying the presence of configuration smells. Overall, GASH outputs a report containing which smells were found and their occurrences in the YAML file.

GASH can be used in two ways:

YAML Analysis: Users can provide a path to a single YAML file or a directory of YAML files. GASH analyzes these files and outputs a report detailing the smells found and their locations. This is ideal for assessing the current pipeline configurations of a single project.

Repository Analysis: Users can provide a GitHub repository URL or a CSV file of URLs. GASH downloads each repository, inspects commits that affect YAML files, and analyzes these files. It outputs a CSV report summarizing commit details (e.g., committer name, date, issue linkage) and detected smells (e.g., type, occurrences). This supports researchers in analyzing pipeline history across multiple projects.

## Usage
GASH is used through a CLI with five options, covering both research and development scenarios.

### Summary of GASH CLI Options

| **Group**   | **Option**          | **Description**                                                                         |
|-------------|---------------------|-----------------------------------------------------------------------------------------|
| Research    | `repo`              | Mines repositories based on a search idea, used when a specific repository is not identified. |
|             | `commits`           | Analyzes a specific repository's commits for configuration smells.                      |
|             | `batch-commits`     | Studies multiple repositories listed in a CSV file.                                     |
| Analysis    | `analyze`           | Performs single mode analysis on a specific YAML file, providing the file path.         |
|             | `batch-analyze`     | Analyzes multiple YAML files within a specified directory.                              |

To use GASH, you need to create a token on GitHub and install the required dependencies listed in the requirements file. This token is necessary for the tool's proper execution, as it is used for validating parameters such as rate limits and accessing the GitHub Advisory Database (GAD). The token will be stored locally for future use.

1. Clone the repository:
    ```bash
    git clone git@github.com:mthsfrts/GASH.git
    ```
2. Enter the repository's root directory:
    ```bash
    cd GASH
    ```
3. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```

After installing the requirements, run `GASH.py` in the terminal:
```bash
python3 GASH.py
```

# GitHub Actions Syntax

## GitHub Actions Configuration Structure

In GitHub, actions configurations are defined at three levels: **workflow**, **job**, and **step**. Below is a detailed description of the possible configurations at each level.

### Workflow

#### At the workflow level, you define general settings that apply to the entire workflow:

```yaml
name: [workflow_name]

on:
  [push|pull_request|schedule|workflow_dispatch|workflow_call]: ...
  workflow_call:
    secrets:
      SECRET_NAME:
        required: true

env: # Global environment variables
  GLOBAL_VAR: value

defaults: # Default settings for all jobs and steps
  run:
    shell: bash
    working-directory: scripts

inputs: # Inputs for the workflow (especially with workflow_dispatch and workflow_call)
  input_name:
    description: 'Description of the input'
    required: true
    default: 'default_value'
    type: string

outputs: # Workflow outputs
  output_name: ${{ jobs.job_id.outputs.output_name }}

concurrency: # Limit concurrent workflow runs
  group: workflow-group
  cancel-in-progress: true

permissions: # GITHUB_TOKEN permissions
  actions: read
  contents: read
```

### Job

##### The job level defines a set of steps that run in a specific environment:

```yaml
jobs:
  [job_id]:
    name: [job_name]
    runs-on: [runner]
    needs: [job_id]
    env: # Job-specific environment variables
      JOB_VAR: value
    secrets: # Job-specific secrets
      SECRET_VAR: ${{ secrets.SECRET_NAME }}
    strategy:
      matrix: ...
      fail-fast: true
      max-parallel: 2
    concurrency: # Limit concurrent job runs
      group: job-group
      cancel-in-progress: true
    steps: ...
    outputs: # Job outputs, can be used by other jobs
      output_id: ${{ steps.step_id.outputs.output_name }}
    timeout-minutes: [minutes]
    continue-on-error: [true|false]
    container: # Docker container to run the job
      image: [docker_image]
    services: # Additional services for the job (e.g., database)
      [service_name]: ...
    retries: # Job retry configuration
      max-attempts: [number]
    permissions: # GITHUB_TOKEN permissions for the job
      actions: read
      contents: read
    status-check: # Status checks
      status: [success|failure|cancelled|skipped|timed_out|completed]
    artifacts: # Artifacts for upload/download
      upload:
        name: [artifact_name]
        path: [file_or_directory]
      download:
        name: [artifact_name]
        path: [destination_path]
```

### Step

#### The step level defines individual actions or commands to be executed:

```yaml
steps:
  - name: [step_name]
    id: [step_id]
    if: [conditional]
    run: [command]
    uses: [action]
    with: ...
    env: # Step-specific environment variables
      STEP_VAR: value
    continue-on-error: [true|false]
    timeout-minutes: [minutes]
    working-directory: [directory]
    retries: # Step retry configuration
      max-attempts: [number]
    status: [success|failure|cancelled|skipped|timed_out|completed]
    artifacts: # Artifacts for upload/download
      upload:
        name: [artifact_name]
        path: [file_or_directory]
      download:
        name: [artifact_name]
        path: [destination_path]
```

### Configuration Summary

#### Here is a summarized table of possible configurations at each level, in alphabetical order:

| Configuration     | Workflow | Job | Step |
|-------------------|----------|-----|------|
| artifacts         |          | ✔️  | ✔️   |
| concurrency       | ✔️       | ✔️  |      |
| container         |          | ✔️  |      |
| continue-on-error |          | ✔️  | ✔️   |
| defaults          | ✔️       | ✔️  |      |
| env               | ✔️       | ✔️  | ✔️   |
| fail-fast         |          | ✔️  |      |
| if                |          |     | ✔️   |
| inputs            | ✔️       |     |      |
| jobs              | ✔️       |     |      |
| max-parallel      |          | ✔️  |      |
| name              | ✔️       | ✔️  | ✔️   |
| needs             |          | ✔️  |      |
| on                | ✔️       |     |      |
| outputs           | ✔️       | ✔️  |      |
| permissions       | ✔️       | ✔️  |      |
| retries           |          | ✔️  | ✔️   |
| run               |          |     | ✔️   |
| runs-on           |          | ✔️  |      |
| secrets           | ✔️       | ✔️* |      |
| services          |          | ✔️  |      |
| steps             |          | ✔️  | ✔️   |
| strategy          |          | ✔️  |      |
| timeout-minutes   | ✔️       | ✔️  | ✔️   |
| uses              |          | ✔️  | ✔️   |
| with              |          | ✔️  | ✔️   |
| working-directory |          |     | ✔️   |

*Note: `secrets` at the job level is in beta.

#### These configurations are based on information from the official GitHub Actions documentation:
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Contexts](https://docs.github.com/en/actions/learn-github-actions/contexts)
- [Variables](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Workflow commands](https://docs.github.com/en/actions/learn-github-actions/workflow-commands-for-github-actions)
- [Guides for GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/guides-for-github-actions)

# List of Smells

## Summary
1. **Security**
   - Hard-Coded Secret
   - Security Flaws
   - Unsecure Protocol
   - Untrusted Dependencies
   - Admin by Default
   - Remote Triggers

2. **Maintenance and Reliability**
   - Duplicated Code
   - Misconfiguration
   - Lack of Error Handling

3. **Code Quality**
    - Long Code Blocks

   
## Detailed
### Category: Security

1. **Hard-Coded Secret**
   - **Description**: Storing sensitive information like tokens or passwords directly in the code.
   - **Vulnerability Level**: Critical
   - **Mitigation**: Use GitHub secrets to store sensitive information. Regularly check for the presence of secrets in the code.
   - **Justification**: Exposing secrets directly in the code can lead to critical data leaks, making the system vulnerable to attacks.
  
```yaml
    name: Hard-Coded Secrets
    on:
      - push
    env:
      API_KEY: my_secret_key
      SERVER_PASSWORD: SERVER_PASSWORD
    jobs:
      build: null
      runs-on: ubuntu-latest
      env:
        DB_PASSWORD: supersecretpassword
```

2. **Unsecure Protocol**
   - **Description**: Using secure protocol for communication.
   - **Vulnerability Level**: Critical
   - **Mitigation**: Ensure all URLs used in scripts use HTTPS.
   - **Justification**: Unencrypted communications are susceptible to man-in-the-middle attacks, exposing sensitive data.
     
```yaml
    name: Unsecured Protocol
    on:
      - push
    env:
      API_URL: 'http://unsecured-url.com'
    jobs:
      build:
        runs-on: ubuntu-latest
        env:
          API_ENDPOINT: 'http://another-unsecured-url.com'
```
The code above illustrates the lack of TLS or SSL in the URL endpoints. This can leave your pipeline and software vulnerable to attacks.

To ensure security, even if the unsecured protocol is used internally, always use the available security measures to protect your data and communication channels.

3. **Untrusted Dependencies**
   - **Description**: Including dependencies from unverified or untrusted sources.
   - **Vulnerability Level**: Critical
   - **Mitigation**: Verify the reputation and security of dependencies before using them. Keep dependencies up to date.
   - **Justification**: Insecure dependencies can introduce vulnerabilities through third-party code.

```yaml
    name: Dependencies
    on:
      - push
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout code
            uses: CodSpeedHQ/action@v2
```
Dependencies in GitHub Actions are specified using the `uses` parameter, which facilitates faster and easier code execution. While leveraging dependencies can enhance workflow efficiency, it also poses risks if unverified sources are used. To mitigate these risks, adhere to the following guidelines:
    
   - Seek out Actions that display the GitHub verified badge. Although this badge does not provide an absolute guarantee of security, it signifies that GitHub endorses the creator and their code.
   - Examine bug reports and potential vulnerabilities using the [GitHub Advisory Database](https://github.com/advisories). This resource helps identify known issues with dependencies.


4. **Admin by Default**
    - **Description**: Assigning admin privileges to all users by default.
    - **Vulnerability Level**: Critical
    - **Mitigation**: Assign permissions based on the principle of least privilege.
    - **Justification**: Admin privileges grant extensive control over the repository, increasing the risk of unauthorized access and data breaches.
  
```yaml
    name: Admin By Default
    on: [push]
    permissions:
       contents: write
    jobs:
       build:
         runs-on: ubuntu-latest
         permissions:
           actions: write-all
         steps:
         - name: Checkout code
           uses: actions/checkout@v2
         - name: Run a command
           run: echo 'Running secure command'
```

Permissions in Github Actions has three values to choose from `read|write|none`, with two variables `read-all|write-all`, to be consider as admin the permission parameter need to be set as `write` or `write-all`.
    
5. **Remote Triggers**
    - **Description**: Allowing remote triggers without proper configuration.
    - **Vulnerability Level**: Critical
    - **Mitigation**: Implement secure configuration mechanisms for remote triggers.
    - **Justification**: the misconfiguration of remote triggers can be exploited to execute unauthorized actions, compromising the pipeline's integrity.

```yaml
name: Remote Trigger Example
on:
   workflow_dispatch:
jobs:
  remote-trigger:
     runs-on: ubuntu-latest
     steps:
       - name: Execute remote command
         run: curl -X POST https://example.com/trigger
```

The code above shows a workflow dispatch with no inputs or any type of configuration. This means that the action could be triggered by anyone at any time, posing a high level of vulnerability, as no security measures are required to run the workflow. While this configuration is sometimes useful, it should generally be avoided for security risks measures.

```yaml
name: Remote Trigger Example
on:
   workflow_call:
     description: This is a call trigger.
     secrets: ${{ secrets.SOME_SECRET }}
     inputs:
       call_input_01:
         description: Input for call.
         type: choice
         options:
           - option1
           - option2
       call_input_02:
         description: Input without type.
       call_input_03:
         type: invalid_type
       call_input_04:
         description: Fourth input.
         type: string
         required: true
```
The code above demonstrates a workflow call that could be dangerous. Using secrets from another workflow, even through the secrets environment, could impose a breach on security protocols. Additionally, having numerous inputs may necessitate a review of the workflow's logic to ensure it is efficient and secure.

```yaml
name: Remote Trigger Example
on:
  workflow_run:
    description: This is a run trigger.
    types:
     - completed
     - requested
    branches:
     - main
    branches-ignore: develop
```

The code above shows a workflow run that lacks proper configuration. The use of conflicting parameters, such as `branches` and `branches-ignore`, combined with the absence of a specified workflow to trigger, can cause significant issues. While this may not lead to a security breach, it can result in substantial maintenance problems or even broken code if not set correctly. Although this trigger is less complex in terms of configuration, improperly managed conditions can lead to intricate and problematic scenarios.

Remote triggers can be a useful and powerful tool in your pipeline, especially in staging or test environments. However, to ensure security and efficiency, proper configuration and cautious usage are essential.

### Category: Maintenance

1. **Replicated Code**
   - **Description**: Replicated code snippets in different parts of the pipeline.
   - **Vulnerability Level**: Medium
   - **Mitigation**: Refactor duplicated code into reusable workflows or actions.
   - **Justification**: Increases complexity and hinders maintenance but does not directly compromise security.
  
```yaml
name: Replicated Code Example

on: [push]

jobs:
   build:
     runs-on: ubuntu-latest
     steps:
       - name: Checkout code
         uses: actions/checkout@v2
       - name: Set up Node.js
         uses: actions/setup-node@v2
         with:
           node-version: '14'
       - name: Install dependencies
         run: npm install

   test:
     runs-on: ubuntu-latest
     steps:
       - name: Checkout code
         uses: actions/checkout@v2
       - name: Set up Node.js
         uses: actions/setup-node@v2
         with:
           node-version: '14'
       - name: Install dependencies
         run: npm install
       - name: Run tests
         run: npm test
```

The code above shows an example of replicated code in a GitHub Actions workflow, where the same steps are repeated in both the build and test jobs. This can lead to inconsistencies and maintenance difficulties.

2. **Misconfiguration**
   - **Description**: Incorrect configurations causing pipeline execution failures.
   - **Vulnerability Level**: Medium
   - **Mitigation**: Carefully review and test configurations before deployment.
   - **Justification**: Can lead to pipeline execution failures but generally does not directly compromise security.

Common misconfigurations include:
   - Missing Parameters: Essential parameters such as `name`, `runs-on` are often omitted, leading to potential issues during execution.
   - Fuzzy Versions: Use of unspecified or fuzzy versions in the `uses` declarations can introduce inconsistencies and unexpected behavior.
   - Unnecessary Complexity: Overly complex conditions in `if` statements can make workflows harder to read and maintain.
   - Concurrency Issues: Incorrect concurrency settings can cause workflow conflicts and unpredictable behavior.

```yaml
name: Misconfiguration Example

on: [push]

# Incorrect concurrency
concurrency:
  cancel-in-progress: false

jobs:
   # Missing Runs-on
  build:
    env:
      NODE_VERSION: '14'
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
        environment: staging

      - name: Setup Node.js
        
        # Fuzzy Versions
        uses: actions/setup-node@v2.*

      - name: Install dependencies
        run: npm install

      - name: DataStruct
        run: npm test
        if: branch == 'main' && tag == 'v1.0' && (event == 'push' || status == fail())

  deploy:
    steps:
      - name: Deploy
        run: echo "Deploying"
        
        # Complex conditionals
        if: branch == 'main' && tag == 'v1.0' && (event == 'push' || status == success())

  test:
    runs-on: ubuntu-latest
    env:
      NODE_VERSION: '14'

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2.x

      - name: Install dependencies
        run: npm install

      - name: DataStruct
        run: npm test
        if: branch == 'main' && event == 'push'
```
The previous code demonstrates various misconfigurations, including missing parameters, ambiguous versions, and overly complex conditions. 
While the absence of parameters may not directly result in a security breach, it is a significant issue. Failure to properly configure the pipeline can lead to hidden failures and make maintenance more challenging.

3. **Lack of Error Handling**
   - **Description**: Absence of proper error checks and handling.
   - **Vulnerability Level**: Critical
   -  **Mitigation**: Implement robust error checks.
   - **Justification**: Can result in broken builds or unexpected behavior, compromising process integrity.
  
```yaml
name: ErrorHandling
on: [push]
jobs:
   build:
     continue-on-error: true
     runs-on: ubuntu-latest
     timeout-minutes: 1
     strategy:
       fail-fast: false
       matrix:
         node-version: [10.x, 12.x, 14.x]
     steps:
       - name: Checkout
         uses: actions/checkout@v2
         continue-on-error: true
         timeout-minutes: 10
```

In the configuration shown in the previous code snippet, several potential issues are present:

- Timeout Settings: The job's timeout is set to 1 minute, which is insufficient for jobs requiring extensive processing time. This can lead to premature job termination and incomplete execution.
- Fail-Fast Strategy: The `fail-fast` parameter is set to false, allowing the job to continue running even if one of the matrix configurations fails. This can result in wasted resources and prolonged pipeline execution.
- Continue-on-Error: Both the job and a step within the job are configured with `continue-on-error: true`, allowing the pipeline to proceed despite encountering errors. This can mask underlying issues that require attention.

### Category: Code Quality

1. **Long Code Blocks**
   - **Description**: Extensive and hard-to-manage code blocks.
   - **Vulnerability Level**: Medium
   - **Mitigation**: Break long code blocks into smaller, more manageable functions.
   - **Justification**: Increases complexity and hinders maintenance but does not directly compromise security.
     
```yaml
name: Long Code Blocks Example

on: [push]

jobs:
   large-job:
     runs-on: ubuntu-latest
     steps:
        - name: Step 1
          run: |
           command1
           command2
           ...
           command20
        - name: Step 2
          run: |
           command1
           command2
           ...
           command20

        - ...

        - name: Step 11
          run: echo "This is a long block example."
```
The code above illustrates a workflow with a job containing more than 10 steps and individual steps with numerous commands, making the job complex to maintain.

o enhance the maintainability of the workflow, consider splitting large jobs into multiple workflows and breaking down steps with excessive commands into smaller units. This approach not only improves readability but also aids in debugging and long-term maintenance.


