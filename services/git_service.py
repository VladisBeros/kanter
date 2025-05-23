from github import Github
from functools import lru_cache

class GitService:
    @staticmethod
    @lru_cache(maxsize=10)
    def connect(token, repository):
        connect_result = {'message': "З'єднання успішне!", 'success': False, 'repo': None}

        try:
            g = Github(f"{token}")
            repo = g.get_repo(f"{repository}")
            connect_result['success'] = True
            connect_result['repo'] = repo
        except Exception as e:
            connect_result['message'] = f"[ERROR] Невідома помилка: {str(e)}"

        return connect_result