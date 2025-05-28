# nessgen-sales-api-testing

This repository contains automated tests related to Sales project.
These tests cover both API and UI functionalities, implemented using Playwright framework.

### Configuration

In the Environment Variables on your local machine, set the user variables:

- _COGNITO_USERNAME_ = your email address (used to authenticate in Sales app)
- _COGNITO_PASSWORD_ = your password (used to authenticate in Sales app)

**The IDE needs to be closed and opened again to retrieve the newly added variables!**

Install the dependencies:

```bash
poetry install
```

### Running tests

Tests are decorated with a tag/marker (e.g. @pytest.mark.auth) in order to be easily run in groups, by a category (e.g.
test related to authentication).
These custom markers are registered in the `pytest.ini` file.

In the `tests/core/api/runner.py` file, functions which use the custom markers and which can be triggered from the
command
line are created. These functions are invoked by scripts present in the `pyproject.toml` file.

Considering the above information, different options can be used to locally run tests:

- with poetry: `poetry run <function marker>`
    - e.g. `poetry run non-workflow`

- with pytest and custom markers:
    - all tests: `pytest`
    - using markers: `pytest -m "<marker>"`
    - from a module: `pytest <filename>.py::<test_func>`