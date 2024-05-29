# GitHub Actions Syntax

## GitHub Actions Configuration Structure

In GitHub Actions, workflow configurations are defined at three levels: **workflow**, **job**, and **step**. Below is a detailed description of the possible configurations at each level.

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

# List of Smells and Anti-Patterns in GitHub Actions

## Smells Summary
1. **Security**
   - Hard-Coded Secret
   - Security Flaws
   - Unsecure Protocol
   - Untrusted Dependencies
   - Admin by Default
   - Use of Weak Cryptography Algorithms

2. **Maintenance and Reliability**
   - Duplicated Code
   - Hard-Coded Values
   - Configuration Errors
   - Lack of Error Handling
   - Fake Success
   - Retry Failure
   - Fuzzy Version

3. **Code Quality**
    - Long Code Blocks
    - Clear Variable and Function Names
    - Adequate Documentation
    - Code Quality Checks
    - 
## Detailed Smells
### Category: Security

1. **Hard-Coded Secret**
   - **Description**: Storing sensitive information like tokens or passwords directly in the code.
   - **Vulnerability Level**: Critical
   - **Mitigation**: Use GitHub secrets to store sensitive information. Regularly check for the presence of secrets in the code.
   - **Justification**: Exposing secrets directly in the code can lead to critical data leaks, making the system vulnerable to attacks.

2. **Security Flaws**
   - **Description**: Improper configurations that allow unauthorized access or compromise the pipeline's integrity.
   - **Vulnerability Level**: Critical
   - **Mitigation**: Regularly review security configurations and permissions. Implement robust security practices.
   - **Justification**: Insecure configurations can open doors to a wide range of attacks, compromising the pipeline's integrity and data.

3. **Unsecure Protocol**
   - **Description**: Using secure protocol for communication.
   - **Vulnerability Level**: Critical
   - **Mitigation**: Ensure all URLs used in scripts use HTTPS.
   - **Justification**: Unencrypted communications are susceptible to man-in-the-middle attacks, exposing sensitive data.

4. **Untrusted Dependencies**
   - **Description**: Including dependencies from unverified or untrusted sources.
   - **Vulnerability Level**: Critical
   - **Mitigation**: Verify the reputation and security of dependencies before using them. Keep dependencies up to date.
   - **Justification**: Insecure dependencies can introduce vulnerabilities through third-party code.

5. **Admin by Default**
   - **Description**: Using unnecessary administrative tokens and permissions.
   - **Vulnerability Level**: Critical
   - **Mitigation**: Use tokens and permissions with the least privileges possible.
   - **Justification**: Using unnecessary administrative permissions exposes the system to high risks, violating the principle of least privilege.

6. **Use of Weak Cryptography Algorithms**
   - **Description**: Using outdated or weak cryptographic algorithms.
   - **Vulnerability Level**: Critical
   - **Mitigation**: Use robust and updated cryptographic algorithms.
   - **Justification**: Weak algorithms can be easily broken, compromising data security.

### Category: Maintenance and Reliability

1. **Duplicated Code**
   - **Description**: Duplicated code snippets in different parts of the pipeline.
   - **Vulnerability Level**: Medium
   - **Mitigation**: Refactor duplicated code into reusable workflows or actions.
   - **Justification**: Increases complexity and hinders maintenance but does not directly compromise security.

2. **Hard-Coded Values**
   - **Description**: Using fixed values in the code instead of configurable variables.
   - **Vulnerability Level**: Medium
   - **Mitigation**: Use environment variables to store configurations.
   - **Justification**: Hinders code maintenance and flexibility but does not directly expose security.

3. **Configuration Errors**
   - **Description**: Incorrect configurations causing pipeline execution failures.
   - **Vulnerability Level**: Medium
   - **Mitigation**: Carefully review and test configurations before deployment.
   - **Justification**: Can lead to pipeline execution failures but generally does not directly compromise security.

4. **Lack of Error Handling**
   - **Description**: Absence of proper error checks and handling.
   - **Vulnerability Level**: Critical
   -  **Mitigation**: Implement robust error checks and provide clear error messages.
   - **Justification**: Can result in broken builds or unexpected behavior, compromising process integrity.

5. **Fake Success**
   - **Description**: Configurations that mask failures, such as `continue-on-error: true`.
   - **Vulnerability Level**: Medium
   - **Mitigation**: Avoid indiscriminate use of `continue-on-error: true`.
   - **Justification**: Masking failures can make real problems harder to detect, increasing technical debt.

6. **Retry Failure**
   - **Description**: Automatic retries that hide underlying issues.
   - **Vulnerability Level**: Medium
   - **Mitigation**: Limit the use of automatic retries and investigate underlying failures.
   - **Justification**: Can hide real problems and complicate debugging but does not directly compromise security.

7. **Fuzzy Version**
   - **Description**: Using non-specific versions for dependencies.
   - **Vulnerability Level**: Medium
   - **Mitigation**: Use specific and precise versions for all dependencies.
   - **Justification**: Can lead to non-reproducible builds and compatibility issues.

### Category: Code Quality

1. **Long Code Blocks**
   - **Description**: Extensive and hard-to-manage code blocks.
   - **Vulnerability Level**: Medium
   - **Mitigation**: Break long code blocks into smaller, more manageable functions.
   - **Justification**: Increases complexity and hinders maintenance but does not directly compromise security.

2. **Clear Variable and Function Names**
   - **Description**: Using unclear or meaningless variable and function names.
   - **Vulnerability Level**: Low
   - **Mitigation**: Adopt clear and consistent naming conventions.
   - **Justification**: Impacts readability and maintenance but does not directly compromise security.

3. **Adequate Documentation**
   - **Description**: Lack of meaningful comments and insufficient documentation.
   - **Vulnerability Level**: Low
   - **Mitigation**: Include meaningful comments and maintain updated documentation.
   - **Justification**: Facilitates maintenance but does not directly compromise security.

4. **Code Quality Checks**
   - **Description**: Absence of linting tools and static code analysis.
   - **Vulnerability Level**: Medium
   - **Mitigation**: Integrate linting tools and static code analysis.
   - **Justification**: Helps ensure code meets quality standards but does not directly compromise security.