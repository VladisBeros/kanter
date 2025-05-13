from dotenv import load_dotenv, set_key
import os

ENV_PATH = ".env"

class EnvService:
    @staticmethod
    def load_env():
        load_dotenv(ENV_PATH)

    @staticmethod
    def get_var(key):
        EnvService.load_env()
        return os.getenv(key)

    @staticmethod
    def set_var(key, value):
        EnvService.load_env()
        set_key(ENV_PATH, key, value)