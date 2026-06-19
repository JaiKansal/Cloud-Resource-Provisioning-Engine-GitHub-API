# Cloud Resource Provisioning Engine — GitHub API

A **Pytest automation framework** for testing GitHub repository operations via the GitHub REST API, built with Python and the `requests` library.

---

## Project Structure

```
├── api/
│   ├── __init__.py
│   ├── base_api.py           # BaseAPI class with generic HTTP methods
│   └── github_repo_api.py    # GitHubRepoAPI class with repo-specific operations
├── tests/
│   └── test_create_delete_github_repo.py   # Smoke test suite
├── .env                      # Local credentials (not committed to Git)
├── .gitignore
├── pytest.ini                # Pytest configuration
└── requirements.txt          # Python dependencies
```

---

## Architecture

### `BaseAPI` (`api/base_api.py`)

The parent class responsible for authentication and generic HTTP communication.

- Accepts a `token` in its constructor and sets the `Authorization` and `Accept` headers required by the GitHub API.
- Provides three reusable methods:
  - `_execute_get(endpoint, params=None)` — sends a GET request
  - `_execute_post(endpoint, payload=None)` — sends a POST request with a JSON body
  - `_execute_delete(endpoint)` — sends a DELETE request

### `GitHubRepoAPI` (`api/github_repo_api.py`)

A child class that inherits from `BaseAPI` and adds GitHub repository-specific methods.

| Method | API Endpoint | Description |
|---|---|---|
| `create_repository(repo_name, private=True)` | `POST /user/repos` | Creates a new repository under the authenticated user |
| `delete_repository(owner, repo_name)` | `DELETE /repos/{owner}/{repo}` | Deletes a repository by owner and name |

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

**Run a specific test file:**

```bash
pytest tests/test_create_delete_github_repo.py -m smoke -v
```

**Run without the marker filter (all tests):**

```bash
pytest tests/ -v
```

> **Note:** If `pytest` is not found, use `python3 -m pytest` instead. To fix permanently, add the Python user bin to your PATH:
> ```bash
> echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
> ```

---

## Test Cases

### `test_create_delete_github_repo.py`

| Test | Mark | Description |
|---|---|---|
| `test_lifecycle_create_and_delete` | `smoke` | Creates a private repo (asserts `201`), then deletes it (asserts `204`). Validates the full create → delete lifecycle. |
| `test_delete_non_existent_repo` | `smoke` | Attempts to delete a repo that does not exist. Asserts `404` to verify correct error handling. |

---

## Dependencies

| Package | Purpose |
|---|---|
| `requests` | HTTP client for GitHub API calls |
| `pytest` | Test runner and assertion framework |
| `python-dotenv` | Loads credentials from the `.env` file |
# Cloud-Resource-Provisioning-Engine-GitHub-API
