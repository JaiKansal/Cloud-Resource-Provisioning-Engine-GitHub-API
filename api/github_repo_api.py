from api.base_api import BaseAPI
from utils.logger import get_logger

logger = get_logger("GitHubRepoAPI")


class GitHubRepoAPI(BaseAPI):

    def __init__(self, token):
        super().__init__(token)
        response = self._execute_get("/user")
        if response.status_code == 401:
            logger.error("Token validation failed: token is expired or invalid")

    def create_repository(self, repo_name, private=True):
        logger.info(f"Attempting to create repository: {repo_name}")
        payload = {
            "name": repo_name,
            "private": private,
            "auto_init": False
        }
        response = self._execute_post("/user/repos", payload=payload)
        if response.status_code == 201:
            logger.info(f"Repository '{repo_name}' created successfully")
        elif response.status_code == 422:
            logger.warning(f"Repository '{repo_name}' already exists")
        return response

    def delete_repository(self, owner, repo_name):
        logger.info(f"Attempting to delete repository: {owner}/{repo_name}")
        response = self._execute_delete(f"/repos/{owner}/{repo_name}")
        if response.status_code == 204:
            logger.info(f"Repository '{owner}/{repo_name}' deleted successfully")
        elif response.status_code == 404:
            logger.warning(f"Repository '{owner}/{repo_name}' not found — nothing to delete")
        return response