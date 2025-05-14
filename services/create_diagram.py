from github import Repository
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
import numpy as np

class CreateDiagram:
    @staticmethod
    def get_contributor_data(login, repo: Repository.Repository):
        data = {
            'total_commits': 0,
            'total_lines_added': 0,
            'total_lines_deleted': 0,
            'total_files_changed': 0,
            'avg_lines_per_commit': 0,
            'first_commit_date': None,
            'last_commit_date': None,
            'commit_frequency': None,
            'most_changed_files': {},
            'commits_by_date': []
        }

        seen_shas = set()
        all_commits = []

        branches = list(repo.get_branches())

        for branch in branches:
            try:
                commits = repo.get_commits(author=login, sha=branch.name)
                for commit in commits:
                    if commit.sha not in seen_shas:
                        seen_shas.add(commit.sha)
                        all_commits.append(commit)
            except Exception as e:
                print(f"[ERROR] Помилка при обробці гілки '{branch.name}': {e}")

        if not all_commits:
            return data

        # Сортуємо коміти за датою
        all_commits.sort(key=lambda c: c.commit.author.date, reverse=True)

        data['total_commits'] = len(all_commits)
        data['first_commit_date'] = all_commits[-1].commit.author.date
        data['last_commit_date'] = all_commits[0].commit.author.date

        for commit in all_commits:
            stats = commit.stats
            commit_date = commit.commit.author.date.date()

            data['commits_by_date'].append({
                'date': commit_date,
                'additions': stats.additions,
                'deletions': stats.deletions,
                'changes': stats.additions + stats.deletions
            })

            data['total_lines_added'] += stats.additions
            data['total_lines_deleted'] += stats.deletions

            for file in commit.files:
                filename = file.filename
                if filename not in data['most_changed_files']:
                    data['most_changed_files'][filename] = 0
                data['most_changed_files'][filename] += 1
                data['total_files_changed'] += 1

        data['avg_lines_per_commit'] = round(
            (data['total_lines_added'] + data['total_lines_deleted']) / data['total_commits'], 2
        )

        days_active = (data['last_commit_date'] - data['first_commit_date']).days
        data['commit_frequency'] = round(data['total_commits'] / max(1, days_active), 2)

        data['most_changed_files'] = dict(
            sorted(data['most_changed_files'].items(), key=lambda item: item[1], reverse=True)[:5]
        )

        return data

    @staticmethod
    def create_figures(data):
        sns.set_theme(style="whitegrid")
        figures = {}

        if not data.get("commits_by_date"):
            return figures

        df = pd.DataFrame(data['commits_by_date'])
        df = df.groupby("date").sum().reset_index()

        # Фигура 1: Изменения по датам
        fig1 = Figure(figsize=(5, 4))
        ax1 = fig1.subplots()
        sns.lineplot(data=df, x='date', y='changes', marker='o', ax=ax1)
        ax1.set_title('Зміни в комітах по датам')
        ax1.set_xlabel('Дата')
        ax1.set_ylabel('Кількість змін (додавання та видалення)')
        ax1.tick_params(axis='x', rotation=45)
        fig1.tight_layout()
        figures['Зміни за весь час'] = fig1

        # Фигура 2: Частота коммитов
        fig2 = Figure(figsize=(5, 4))
        ax2 = fig2.subplots()
        sns.barplot(x=["Коміти у день"], y=[data['commit_frequency']], ax=ax2,
                    color=sns.color_palette("Blues_d")[0])
        ax2.set_title("Частота комітів")
        figures['Частота комітів'] = fig2

        # Фигура 3: Добавленные/удаленные строки за последние 4 недели (столбцы рядом)
        fig3 = Figure(figsize=(5, 4))  # Увеличим размер ещё больше
        ax3 = fig3.subplots()

        # Фильтруем данные за последние 4 недели
        end_date = pd.to_datetime('today')
        start_date = end_date - pd.Timedelta(weeks=4)
        last_4_weeks = df[(pd.to_datetime(df['date']) >= start_date) &
                          (pd.to_datetime(df['date']) <= end_date)]

        if not last_4_weeks.empty:
            # Группируем по неделям
            last_4_weeks['week'] = pd.to_datetime(last_4_weeks['date']).dt.to_period('W')
            weekly_data = last_4_weeks.groupby('week').sum().reset_index()
            weekly_data['week_str'] = weekly_data['week'].astype(str)

            # Логируем данные для проверки
            print("\nДанные для графика за последние 4 недели:")
            print(weekly_data[['week_str', 'additions', 'deletions']])
            print(
                f"\nМаксимальные значения: Добавлено - {weekly_data['additions'].max()}, Удалено - {weekly_data['deletions'].max()}")

            # Позиции для столбцов
            bar_width = 0.4  # Увеличим ширину столбцов
            x = np.arange(len(weekly_data))

            # Рисуем столбцы рядом с прозрачностью
            ax3.bar(x - bar_width / 2, weekly_data['additions'], width=bar_width,
                    color='green', label='Додані рядки', alpha=0.8)
            ax3.bar(x + bar_width / 2, weekly_data['deletions'], width=bar_width,
                    color='red', label='Видалені рядки', alpha=0.8)

            ax3.set_title('Додані та видалені рядки за останні 4 тижні (порівняння)', pad=20)
            ax3.set_xlabel('Тиждень', labelpad=10)
            ax3.set_ylabel('Кількість рядків', labelpad=10)
            ax3.set_xticks(x)
            ax3.set_xticklabels(weekly_data['week_str'], rotation=45, ha='right')

            # Настроим масштаб оси Y, если удалений мало
            y_max = max(weekly_data['additions'].max(), weekly_data['deletions'].max()) * 1.2
            ax3.set_ylim(0, y_max)

            # Добавим значения поверх столбцов
            for i in range(len(weekly_data)):
                ax3.text(x[i] - bar_width / 2, weekly_data['additions'][i] + y_max * 0.02,
                         str(weekly_data['additions'][i]), ha='center', fontsize=9)
                ax3.text(x[i] + bar_width / 2, weekly_data['deletions'][i] + y_max * 0.02,
                         str(weekly_data['deletions'][i]), ha='center', fontsize=9)

            ax3.legend(loc='upper right')
            ax3.grid(axis='y', linestyle='--', alpha=0.5)

            fig3.tight_layout()
        else:
            print("\nНемає даних за останні 4 тижні")
            ax3.text(0.5, 0.5, 'Немає даних за останні 4 тижні',
                     ha='center', va='center', transform=ax3.transAxes)

        figures['Зміни за останні 4 тижні (порівняння)'] = fig3

        return figures