from api.base_api import BaseAPI
from utils.logger import get_logger

logger = get_logger("GitHubRepoAPI")


class GitHubRepoAPI(BaseAPI):

    def __init__(self, token):
        super().__init__(token)
        response = self._execute_get("/user")
        if response.status_code == 401:
            logger.error("Token validation failed: token is expired or invalid")

    def create_repository(self, repo_name, private=True, description="", auto_init=False):
        logger.info(f"Attempting to create repository: {repo_name}")
        payload = {
            "name": repo_name,
            "private": private,
            "description": description,
            "auto_init": auto_init
        }
        response = self._execute_post("/user/repos", payload=payload)

        if response.status_code >= 500:
            logger.critical(f"GitHub API is down or unavailable (status {response.status_code})")
            response.raise_for_status()

        status_map = {
            201: (logger.info,    f"Repository '{repo_name}' created successfully"),
            422: (logger.warning, f"Repository '{repo_name}' already exists"),
            401: (logger.error,   f"Authentication error creating '{repo_name}'"),
            403: (logger.error,   f"Permissions error creating '{repo_name}'"),
            404: (logger.error,   f"Resource not found when creating '{repo_name}'"),
        }

        log_action, message = status_map.get(
            response.status_code,
            (logger.error, f"Unexpected status code {response.status_code} when creating '{repo_name}'")
        )
        log_action(message)

        return response

    def delete_repository(self, owner, repo_name):
        logger.info(f"Attempting to delete repository: {owner}/{repo_name}")
        response = self._execute_delete(f"/repos/{owner}/{repo_name}")

        if response.status_code >= 500:
            logger.critical(f"GitHub API is down or unavailable (status {response.status_code})")
            response.raise_for_status()

        status_map = {
            204: (logger.info,    f"Repository '{owner}/{repo_name}' deleted successfully"),
            404: (logger.warning, f"Repository '{owner}/{repo_name}' not found — nothing to delete"),
            403: (logger.error,   f"Cannot delete '{owner}/{repo_name}': organization rules prevent deletion or missing scopes"),
            409: (logger.error,   f"Cannot delete '{owner}/{repo_name}': conflict detected"),
        }

        log_action, message = status_map.get(
            response.status_code,
            (logger.error, f"Unexpected status code {response.status_code} when deleting '{owner}/{repo_name}'")
        )
        log_action(message)

        return response