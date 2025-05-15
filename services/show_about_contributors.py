import datetime
from tkinter import messagebox

def not_active_contributors(repo):
    contributors = list(repo.get_contributors())
    inactive_logins = []
    one_week_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    for contributor in contributors:
        try:
            commits = list(repo.get_commits(author=contributor.login, since=one_week_ago))
            if not commits:
                inactive_logins.append(contributor.login)
        except Exception as e:
            print(f"[ERROR] Помилка при обробці користувача {contributor.login}: {e}")

    if inactive_logins:
        inactive_list = "\n".join(inactive_logins)
        messagebox.showwarning(
            "Неактивні розробники",
            f"Протягом останнього тижня не було комітів від наступних розробників:\n\n{inactive_list}"
        )