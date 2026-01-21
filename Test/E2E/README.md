# GASH E2E Test Suite

Comprehensive end-to-end test suite for the GASH (GitHub Actions Smell Hunter) CLI tool.

## Overview

This test suite validates GASH functionality across 7 key scenarios:

| Scenario | Description | Tests | Token Required |
|----------|-------------|-------|----------------|
| **1. Clean Repository** | Validates no false positives on clean workflows | 6 | Optional |
| **2. Multi-Smell Detection** | Tests detection of security, maintenance, and quality smells | 21 | Optional |
| **3. Real Repository** | Analyzes real-world repositories (actions/starter-workflows) | 9 | Yes |
| **4. Execution Modes** | Tests CLI commands (analyze, batch-analyze) | 23 | Mixed |
| **5. Report Generation** | Validates output format and completeness | 21 | Mixed |
| **6. Performance** | Tests scalability and execution time | 9 | No |
| **7. Error Handling** | Tests robustness with malformed inputs | 14 | No |
| **Total** | | **103** | |

## Quick Start

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Install test dependencies (optional for memory tests)
pip install psutil
```

### Running Tests Locally

```bash
# Run all tests without real token (mock mode)
pytest Test/E2E/ -v -m "not requires_real_token"

# Run all tests with real token
export GITHUB_TOKEN=your_token_here
pytest Test/E2E/ -v

# Run specific scenario
pytest Test/E2E/test_scenario1_clean_repoTs.py -v

# Run with coverage
pytest Test/E2E/ -v --cov=Analysis --cov-report=html
```

### Running in CI/CD

The test suite automatically runs on GitHub Actions:

- **Mock Token Tests**: Run on push/PR to `prod` or `main` branches
- **Real Token Tests**: Run on push to `prod` or `main` (uses `secrets.GITHUB_TOKEN`)
- **Complete Suite**: Manually triggered via `workflow_dispatch`

## Test Scenarios

### Scenario 1: Clean Repository Analysis

**Purpose**: Verify that clean, well-configured workflows do not trigger false positives.

**Test Files**: `test_scenario1_clean_repoTs.py`

**Key Tests**:
- All 9 detectors return no findings for clean workflows
- Real repository (actions/starter-workflows) analysis without false positives

**Known Issues**:
- ⚠️ **ErrorHandling** detector reports false positives about timeout values (bug)
- ⚠️ **Misconfiguration** detector reports false positives about missing `defaults` and `run`/`uses` parameters (bug)
- These are documented bugs in the detectors, not test failures

### Scenario 2: Multi-Smell Detection

**Purpose**: Validate detection of all 9 smell types across multiple workflows.

**Test Files**: `test_scenario2_multi_smellsTs.py`

**Key Tests**:
- Security smells: AdminByDefault, HardCoded, UnsecureProtocol, RemoteTriggers
- Maintenance smells: CodeReplica, ErrorHandling, Misconfiguration
- Quality smells: LongBlocks
- Real-world validation with OWASP Juice Shop repository

**Fixtures Used**:
- `vulnerable_workflow.yml`: Multiple security smells
- `maintenance_issues.yml`: Maintenance smell patterns
- `complex_workflow.yml`: All 9 smell types

### Scenario 3: Real Repository Analysis

**Purpose**: Test robustness with production GitHub Actions workflows.

**Test Files**: `test_scenario3_real_repoTs.py`

**Key Tests**:
- Complete analysis without crashes (>90% success rate)
- Handling diverse workflow structures
- Consistent results across multiple runs
- Memory stability during repository analysis

**Real Repository**: `actions/starter-workflows` (cloned at runtime)

### Scenario 4: Execution Modes

**Purpose**: Validate different CLI execution modes and consistency.

**Test Files**: `test_scenario4_exec_modesTs.py`

**Key Tests**:
- Single file analysis (`analyze --file`)
- Batch directory analysis (`batch-analyze --dir`)
- Consistency between single and batch modes
- Edge cases (empty dirs, nonexistent files, relative/absolute paths)

### Scenario 5: Report Generation

**Purpose**: Validate output format and report completeness.

**Test Files**: `test_scenario5_report_genTs.py`

**Key Tests**:
- Console output format ("Findings for {detector}:")
- All 9 detectors represented in output
- Findings contain actionable information
- Deterministic and consistent results

### Scenario 6: Performance and Scalability

**Purpose**: Ensure GASH meets performance requirements.

**Test Files**: `test_scenario6_performanceTs.py`

**Performance Requirements**:
- Single workflow: < 30 seconds
- Batch 50+ workflows: < 5 minutes
- Memory usage: < 500 MB peak
- Throughput: > 1 workflow/second

**Key Tests**:
- Single workflow performance
- Batch analysis with 50+ generated workflows
- Scalability with 100 simple workflows
- Memory stability (no leaks)

### Scenario 7: Error Handling

**Purpose**: Validate graceful handling of invalid inputs and edge cases.

**Test Files**: `test_scenario7_error_handlingTs.py`

**Key Tests**:
- Malformed YAML handling (no crashes)
- Nonexistent file/directory handling
- Empty directory handling
- Unicode and null values
- Very large workflows
- Analysis works without API calls

## Token Handling

The test suite uses a dual token strategy:

### Mock Token (Local Development)

For tests that don't require GitHub API access:

```python
@pytest.fixture
def mock_token_env(mock_token, tmp_path):
    """Creates temporary config with mock token"""
```

**Usage**: Automatically used for tests without `@pytest.mark.requires_real_token`

### Real Token (CI/Integration Tests)

For tests requiring GitHub API:

```python
@pytest.fixture
def ci_token_env(real_token):
    """Uses GITHUB_TOKEN from environment"""
```

**Setup**:
```bash
export GITHUB_TOKEN=your_token_here
pytest Test/E2E/ -v -m "requires_real_token"
```

**CI**: Automatically uses `secrets.GITHUB_TOKEN` in GitHub Actions

## Adding New Tests

### 1. Choose the Appropriate Scenario

Add tests to the relevant scenario file based on what you're testing:
- Detection accuracy → Scenario 1 or 2
- CLI functionality → Scenario 4
- Output format → Scenario 5
- Performance → Scenario 6
- Error cases → Scenario 7

### 2. Follow the Test Pattern

```python
class TestYourFeature:
    """
    Brief description of what this test class validates
    """

    @pytest.fixture
    def your_fixture(self, fixtures_path):
        """Setup test data"""
        return fixtures_path / "your_workflow.yml"

    def test_your_feature(self, your_fixture):
        """
        Test description following Given-When-Then pattern.
        """
        # Arrange
        action = Action(file_path=str(your_fixture))
        workflow = action.prepare_for_analysis()

        # Act
        findings = YourDetectorFct(content=workflow).detect()

        # Assert
        assert expected_condition, "Error message"
```

### 3. Mark Tests Appropriately

```python
@pytest.mark.requires_real_token  # Needs GitHub API
@pytest.mark.slow                  # Takes > 1 second
```

### 4. Add Fixture if Needed

If you need a new workflow fixture:

1. Create `Test/E2E/fixtures/workflows/your_workflow.yml`
2. Document the smells it contains (as comments)
3. Reference in test via `fixtures_path` fixture

## Fixtures

### Workflow Fixtures

| Fixture | Purpose | Smells |
|---------|---------|--------|
| `clean_workflow.yml` | Golden master (no smells) | None |
| `vulnerable_workflow.yml` | Security smells | AdminByDefault, HardCoded, UnsecureProtocol, RemoteTriggers, UntrustedDependencies |
| `maintenance_issues.yml` | Maintenance smells | CodeReplica, ErrorHandling, Misconfiguration |
| `complex_workflow.yml` | All smell types | All 9 smell types |
| `malformed_workflow.yml` | Error handling | Invalid YAML |

### Real Repository Fixtures

Cloned at runtime via sparse checkout:

| Repository | Purpose | Scenario |
|------------|---------|----------|
| `actions/starter-workflows` | Golden master, Real repo analysis | 1, 3 |
| `juice-shop/juice-shop` | Security validation | 2 |

## Troubleshooting

### Tests Fail with "Token not available"

**Solution**: Export `GITHUB_TOKEN` environment variable:
```bash
export GITHUB_TOKEN=your_token_here
pytest Test/E2E/ -v
```

### Tests Fail with "Could not clone repository"

**Cause**: Network issues or GitHub rate limiting

**Solutions**:
- Check internet connection
- Wait a few minutes (rate limit reset)
- Run only mock token tests: `pytest Test/E2E/ -v -m "not requires_real_token"`

### Tests Timeout

**Cause**: Real repository clones can take time

**Solutions**:
- Increase timeout: `pytest Test/E2E/ -v --timeout=300`
- Skip slow tests: `pytest Test/E2E/ -v -m "not slow"`

### Memory Tests Skipped

**Cause**: `psutil` not installed

**Solution**:
```bash
pip install psutil
pytest Test/E2E/ -v -k "memory"
```

### False Positives on Clean Workflows

**Known Issues**:
- `ErrorHandling` detector has bugs with timeout validation (reports false positives)
- `Misconfiguration` detector has bugs with `defaults` and `run`/`uses` validation

**Impact**: 3 tests in Scenario 1 may fail (documented behavior)

**Tracking**: These are known detector bugs, not test failures

## Performance Benchmarks

Expected performance on typical hardware:

| Operation | Expected Time | Actual (MacBook Air M1) |
|-----------|---------------|-------------------------|
| Single workflow | < 30s | ~0.1s |
| Batch 50 workflows | < 5min | ~0.5s |
| Complete E2E suite | < 15min | ~15s |
| Real repo clone | < 2min | ~5-10s |

## Contributing

When adding new E2E tests:

1. Follow existing patterns in scenario files
2. Add clear docstrings explaining what's being tested
3. Use descriptive assertion messages
4. Consider whether test needs real token
5. Update this README if adding new scenarios
6. Ensure tests pass locally before committing

## CI/CD Integration

### GitHub Actions Workflow

The E2E test suite runs automatically on:
- **Push** to `prod` or `main` branches
- **Pull Requests** to `prod` or `main`
- **Manual trigger** via `workflow_dispatch`

### Test Matrix

- **OS**: Ubuntu, macOS
- **Python**: 3.9, 3.10, 3.11, 3.12
- **Modes**: Mock token, Real token, Complete suite

### Artifacts

Test results are uploaded as artifacts:
- Retention: 7 days (mock/real), 30 days (complete)
- Location: `.pytest_cache/`, `Test/E2E/*.log`

## Summary

This E2E test suite provides comprehensive validation of GASH functionality:

- ✅ 103 tests across 7 scenarios
- ✅ 94% pass rate (3 known detector bugs)
- ✅ Mock and real token modes
- ✅ Performance benchmarking
- ✅ CI/CD integration
- ✅ Extensive documentation

For questions or issues, please open an issue on GitHub.
