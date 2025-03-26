# Tests for Tezhire Interview Bot

This directory contains tests for the Tezhire Interview Bot application.

## Test Structure

- `test_ultravox_config.py`: Tests for the Ultravox configuration module
- `test_ultravox_router.py`: Tests for the Ultravox API endpoints
- `test_tezhire_router.py`: Tests for the Tezhire API endpoints

## Running Tests

You can run the tests using the `run_tests.py` script in the root directory:

```bash
python run_tests.py
```

Or you can use pytest directly:

```bash
pytest tests/
```

For coverage reports:

```bash
pytest --cov=app tests/
```

## Writing New Tests

When adding new functionality, please also add corresponding tests. Follow these guidelines:

1. Create a new test file named `test_<module_name>.py`
2. Use the `unittest` framework for consistency
3. Mock external dependencies (like API calls)
4. Test both success and error cases
5. Include docstrings explaining what each test does

## Test Environment

Tests use a simulated environment and do not make actual API calls to Ultravox. All external dependencies are mocked.