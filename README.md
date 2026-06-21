# Cloud Resource Provisioning Engine — GitHub API

A **Pytest automation framework** for testing GitHub repository operations via the GitHub REST API, built with Python and the `requests` library. The framework includes structured logging, fallback handling, HTML test reporting, and a GitLab CI pipeline.

---

## Project Structure

```
├── api/
│   ├── __init__.py
│   ├── base_api.py                        # BaseAPI class with generic HTTP methods
│   └── github_repo_api.py                 # GitHubRepoAPI class with repo operations, logging, and fallbacks
├── tests/
│   └── test_create_delete_github_repo.py  # Smoke test suite covering all status code scenarios
├── utils/
│   └── logger.py                          # Logger factory — writes to a dated log file
├── logs/                                  # Auto-created at runtime
│   └── execution_YYYY-MM-DD.log
├── .env                                   # Local credentials (not committed to Git)
├── .gitignore
├── .gitlab-ci.yml                         # GitLab CI pipeline definition
├── pytest.ini                             # Pytest configuration with HTML report settings
├── report.html                            # Auto-generated HTML test report (after each run)
└── requirements.txt                       # Python dependencies
```

---

## Architecture

### `BaseAPI` (`api/base_api.py`)

The parent class responsible for authentication and generic HTTP communication.

- Accepts a `token` in its constructor and sets the `Authorization` and `Accept` headers required by the GitHub API.
- Provides three reusable methods:

| Method | HTTP Verb | Description |
|---|---|---|
| `_execute_get(endpoint, params)` | GET | Sends a GET request |
| `_execute_post(endpoint, payload)` | POST | Sends a POST request with a JSON body |
| `_execute_delete(endpoint)` | DELETE | Sends a DELETE request |

---

### `GitHubRepoAPI` (`api/github_repo_api.py`)

Inherits from `BaseAPI`. Adds repository-specific methods with logging and fallback handling at each status code.

**`__init__(token)`**
- Calls `super().__init__(token)` to set up headers.
- Validates the token via `GET /user`. Logs an error if the response is `401`.

**`create_repository(repo_name, private=True)`**

| Response | Action |
|---|---|
| `201` | Logs success |
| `422` | Logs a warning — repository already exists |

**`delete_repository(owner, repo_name)`**

| Response | Action |
|---|---|
| `204` | Logs success |
| `404` | Logs a warning — repository not found |

---

### `get_logger` (`utils/logger.py`)

A simple factory function using the standard `logging` library.

- Creates the `logs/` directory if it does not exist.
- Writes logs to `logs/execution_YYYY-MM-DD.log` with the format:
  ```
  TIMESTAMP | LEVEL | LOGGER_NAME | MESSAGE
  ```
- Guards against duplicate handlers so loggers are safe to import across modules.

---

## Prerequisites

- Python 3.9+
- A GitHub Personal Access Token (classic) with the following scopes:
  - `repo` — full control of private repositories
  - `delete_repo` — permission to delete repositories

---

## Setup

**1. Clone the repository**

```bash
git clone <your-repo-url>
cd "Cloud Resource Provisioning Engine (GitHub API)"
```

**2. Install dependencies**

```bash
pip3 install -r requirements.txt
```

**3. Configure credentials**

Create a `.env` file in the project root (already gitignored):

```
GITHUB_TOKEN=your_personal_access_token_here
GITHUB_USERNAME=your_github_username_here
```

---

## Running Tests

Always run pytest from the **project root** directory.

**Run all smoke tests:**

```bash
pytest tests/ -m smoke -v
```

**Run without the marker filter (all tests):**

```bash
pytest tests/ -v
```

> **Note:** If `pytest` is not found, use `python3 -m pytest` instead. To fix permanently, add the Python user bin to your PATH:
> ```bash
> echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
> ```

After each run, two outputs are automatically generated:
- **`report.html`** — a self-contained HTML test report in the project root
- **`logs/execution_YYYY-MM-DD.log`** — a structured log file of all API interactions

---

## Test Cases

All tests are in `tests/test_create_delete_github_repo.py` and tagged `@pytest.mark.smoke`.

| Test | Status Codes Asserted | Scenario |
|---|---|---|
| `test_lifecycle_create_and_delete` | `201`, `204` | Creates a private repo, then deletes it — validates the full happy-path lifecycle |
| `test_create_duplicate_repository` | `422` | Creates a repo, then tries to create it again — validates the duplicate fallback |
| `test_delete_non_existent_repo` | `404` | Attempts to delete a repo that does not exist — validates the not-found fallback |
| `test_invalid_token_returns_401` | `401` | Uses a bad token to attempt repo creation — validates the auth failure fallback |

### Fixtures

| Fixture | Description |
|---|---|
| `repo_api` | Initialises `GitHubRepoAPI` using the token from `.env` |
| `invalid_repo_api` | Initialises `GitHubRepoAPI` with a hardcoded invalid token for 401 testing |

---

## HTML Report

`pytest.ini` is configured to automatically generate a self-contained HTML report on every run:

```ini
addopts = --html=report.html --self-contained-html
```

Open `report.html` in any browser after a run to see a full breakdown of passed, failed, and skipped tests.

---

## GitLab CI Pipeline

The `.gitlab-ci.yml` defines a single `test` stage using the `python:3.9` Docker image.

```yaml
stages:
  - test

test:
  stage: test
  image: python:3.9
  script:
    - pip install -r requirements.txt
    - pytest -m smoke
  artifacts:
    expire_in: 1 week
    paths:
      - report.html
      - logs/
```

**Artifacts saved for 1 week after each pipeline run:**
- `report.html` — the HTML test report
- `logs/` — the full execution log directory

---

## Dependencies

| Package | Purpose |
|---|---|
| `requests` | HTTP client for GitHub API calls |
| `pytest` | Test runner and assertion framework |
| `python-dotenv` | Loads credentials from the `.env` file |
| `pytest-html` | Generates self-contained HTML test reports |
