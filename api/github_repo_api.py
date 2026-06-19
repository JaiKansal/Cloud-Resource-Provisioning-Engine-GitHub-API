from base_api import BaseAPI
import os
from dotenv import load_dotenv

load_dotenv()

class GitHubRepoAPI(BaseAPI):

    def __init__(self, token):
        super().__init__(token)

    def create_repository(self, repo_name, private=True):
        payload = {
            "name": repo_name,
            "private": private,
            "auto_init": False
        }
        return self._execute_post("/user/repos", payload=payload)

    def delete_repository(self, owner, repo_name):
        return self._execute_delete(f"/repos/{owner}/{repo_name}")

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
REPO_NAME = input("Enter the repository name you want to create: ")

api = GitHubRepoAPI(token=GITHUB_TOKEN)
api.create_repository(REPO_NAME, private=False)