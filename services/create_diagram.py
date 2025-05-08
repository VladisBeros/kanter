import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import seaborn as sns


class CreateDiagram:
    @staticmethod
    def get_contributor_data(login, repo):
        data = {
            'total_commits': 0,
            'total_lines_added': 0,
            'total_lines_deleted': 0,
            'total_files_changed': 0,
            'avg_lines_per_commit': 0,
            'first_commit_date': None,
            'last_commit_date': None,
            'commit_frequency': None,
            'most_changed_files': {}
        }

        commits = list(repo.get_commits(author=login))

        if not commits:
            return data

        data['total_commits'] = len(commits)    # Всего комитов
        data['first_commit_date'] = commits[-1].commit.author.date  # Дата первого комита
        data['last_commit_date'] = commits[0].commit.author.date    # Дата последнего комита

        for commit in commits:
            stats = commit.stats
            data['total_lines_added'] += stats.additions
            data['total_lines_deleted'] += stats.deletions

            # Анализ файлов
            for file in commit.files:
                filename = file.filename
                if filename not in data['most_changed_files']:
                    data['most_changed_files'][filename] = 0
                data['most_changed_files'][filename] += 1
                data['total_files_changed'] += 1

            print(f"Коміт: {commit.sha}, +{stats.additions}, -{stats.deletions}")

        data['avg_lines_per_commit'] = round(
            (data['total_lines_added'] + data['total_lines_deleted']) / data['total_commits'],
            2
        )   # среднее количество в комите строк

        # Частота коммитов (дней между первым и последним коммитом)
        days_active = (data['last_commit_date'] - data['first_commit_date']).days
        data['commit_frequency'] = round(data['total_commits'] / max(1, days_active), 2)

        # Топ-5 самых изменяемых файлов
        data['most_changed_files'] = dict(
            sorted(data['most_changed_files'].items(),
                   key=lambda item: item[1],
                   reverse=True)[:5]
        )

        return data

    @staticmethod
    def create_figures(data):
        sns.set_theme(style="whitegrid")
        figures = {}

        # Частота коммитов
        fig1 = Figure(figsize=(5, 4))
        ax1 = fig1.subplots()
        sns.barplot(x=["Коміти/день"], y=[data['commit_frequency']], ax=ax1, color=sns.color_palette("Blues_d")[0])
        ax1.set_title("Частота комітів")
        figures['Частота комітів'] = fig1

        # Додано / Видалено рядків
        fig2 = Figure(figsize=(5, 4))
        ax2 = fig2.subplots()
        sns.barplot(x=["Додано", "Видалено"], y=[data['total_lines_added'], data['total_lines_deleted']], ax=ax2,
                    palette=sns.color_palette(["green", "red"]), legend=False)
        ax2.set_title("Зміни рядків коду")
        figures['Зміни рядків'] = fig2

        # Середнє рядків на коміт
        fig3 = Figure(figsize=(5, 4))
        ax3 = fig3.subplots()
        sns.barplot(x=["Середнє рядків/коміт"], y=[data['avg_lines_per_commit']], ax=ax3,
                    color=sns.color_palette("Purples")[2])
        ax3.set_title("Середнє рядків у коміті")
        figures['Середнє на коміт'] = fig3

        # Топ змінених файлів
        if data['most_changed_files']:
            files = list(data['most_changed_files'].keys())
            changes = list(data['most_changed_files'].values())
            df_files = pd.DataFrame({"Файл": files, "Кількість змін": changes})

            fig4 = Figure(figsize=(6, 5))
            ax4 = fig4.subplots()
            sns.barplot(y="Файл", x="Кількість змін", data=df_files, ax=ax4,
                        palette="magma", legend=False)
            ax4.set_title("Найчастіше змінювані файли")
            figures['Топ файлів'] = fig4

        return figures