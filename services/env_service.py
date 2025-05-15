from dotenv import set_key, unset_key
import os

ENV_PATH = ".env"

class EnvService:
    @staticmethod
    def save_to_env(token, repository):
        if not os.path.exists(ENV_PATH):
            with open(ENV_PATH, 'w'):
                pass

        set_key(ENV_PATH, "GIT_TOKEN", f'{token}')
        set_key(ENV_PATH, "REPO_NAME", f'{repository}')
        os.environ["GIT_TOKEN"] = token
        os.environ["REPO_NAME"] = repository

    @staticmethod
    def clear_env():
        if os.path.exists(ENV_PATH):
            unset_key(ENV_PATH, "GIT_TOKEN")
            unset_key(ENV_PATH, "REPO_NAME")
        os.environ.pop("GIT_TOKEN", None)
        os.environ.pop("REPO_NAME", None)