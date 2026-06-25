import os
import pytest
from dotenv import load_dotenv
from api.github_repo_api import GitHubRepoAPI

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "..", "config", ".env")
load_dotenv(dotenv_path=env_path)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
TEST_REPO_NAME = "test-repo-automation-3"


@pytest.fixture
def repo_api():
    return GitHubRepoAPI(token=GITHUB_TOKEN)


@pytest.fixture
def invalid_repo_api():
    return GitHubRepoAPI(token="invalid_token_xyz")


@pytest.mark.smoke
def test_lifecycle_create_and_delete(repo_api):
    create_response = repo_api.create_repository(repo_name=TEST_REPO_NAME, private=True)
    assert create_response.status_code == 201

    delete_response = repo_api.delete_repository(owner=GITHUB_USERNAME, repo_name=TEST_REPO_NAME)
    assert delete_response.status_code == 204


@pytest.mark.smoke
def test_create_duplicate_repository(repo_api):
    repo_api.create_repository(repo_name=TEST_REPO_NAME, private=True)

    duplicate_response = repo_api.create_repository(repo_name=TEST_REPO_NAME, private=True)
    assert duplicate_response.status_code == 422

    repo_api.delete_repository(owner=GITHUB_USERNAME, repo_name=TEST_REPO_NAME)


@pytest.mark.smoke
def test_delete_non_existent_repo(repo_api):
    delete_response = repo_api.delete_repository(owner=GITHUB_USERNAME, repo_name="this-repo-100-percent-does-not-exist")
    assert delete_response.status_code == 404


@pytest.mark.smoke
def test_invalid_token_returns_401(invalid_repo_api):
    response = invalid_repo_api.create_repository(repo_name="any-repo-name", private=True)
    assert response.status_code == 401
