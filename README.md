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

# List of Smells and Anti-Patterns in GitHub Actions

## Smells Summary
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

   
## Detailed Smells
### Category: Security

1. **Hard-Coded Secret**
   - **Description**: Storing sensitive information like tokens or passwords directly in the code.
   - **Vulnerability Level**: Critical
   - **Mitigation**: Use GitHub secrets to store sensitive information. Regularly check for the presence of secrets in the code.
   - **Justification**: Exposing secrets directly in the code can lead to critical data leaks, making the system vulnerable to attacks.

2. **Unsecure Protocol**
   - **Description**: Using secure protocol for communication.
   - **Vulnerability Level**: Critical
   - **Mitigation**: Ensure all URLs used in scripts use HTTPS.
   - **Justification**: Unencrypted communications are susceptible to man-in-the-middle attacks, exposing sensitive data.

3. **Untrusted Dependencies**
   - **Description**: Including dependencies from unverified or untrusted sources.
   - **Vulnerability Level**: Critical
   - **Mitigation**: Verify the reputation and security of dependencies before using them. Keep dependencies up to date.
   - **Justification**: Insecure dependencies can introduce vulnerabilities through third-party code.

4. **Admin by Default**
    - **Description**: Assigning admin privileges to all users by default.
    - **Vulnerability Level**: Critical
    - **Mitigation**: Assign permissions based on the principle of least privilege.
    - **Justification**: Admin privileges grant extensive control over the repository, increasing the risk of unauthorized access and data breaches.

5. **Remote Triggers**
    - **Description**: Allowing remote triggers without proper configuration.
    - **Vulnerability Level**: Critical
    - **Mitigation**: Implement secure configuration mechanisms for remote triggers.
    - **Justification**: the misconfiguration of remote triggers can be exploited to execute unauthorized actions, compromising the pipeline's integrity.

### Category: Maintenance and Reliability

1. **Replicated Code**
   - **Description**: Replicated code snippets in different parts of the pipeline.
   - **Vulnerability Level**: Low
   - **Mitigation**: Refactor duplicated code into reusable workflows or actions.
   - **Justification**: Increases complexity and hinders maintenance but does not directly compromise security.

2. **Misconfiguration**
   - **Description**: Incorrect configurations causing pipeline execution failures.
   - **Vulnerability Level**: Medium
   - **Mitigation**: Carefully review and test configurations before deployment.
   - **Justification**: Can lead to pipeline execution failures but generally does not directly compromise security.

3. **Lack of Error Handling**
   - **Description**: Absence of proper error checks and handling.
   - **Vulnerability Level**: Critical
   -  **Mitigation**: Implement robust error checks.
   - **Justification**: Can result in broken builds or unexpected behavior, compromising process integrity.

### Category: Code Quality

1. **Long Code Blocks**
   - **Description**: Extensive and hard-to-manage code blocks.
   - **Vulnerability Level**: Medium
   - **Mitigation**: Break long code blocks into smaller, more manageable functions.
   - **Justification**: Increases complexity and hinders maintenance but does not directly compromise security.
