from github import Repository
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
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
        df['date'] = pd.to_datetime(df['date'])

        df_weekly = df.groupby(pd.Grouper(key='date', freq='W-MON')).agg({
            'additions': 'sum',
            'deletions': 'sum',
            'changes': 'sum'
        }).reset_index()

        fig1 = Figure(figsize=(5, 4))
        ax1 = fig1.subplots()

        sns.lineplot(
            data=df_weekly,
            x='date',
            y='changes',
            marker='o',
            markersize=8,
            ax=ax1
        )

        for i, row in df_weekly.iterrows():
            ax1.text(
                row['date'],
                row['changes'] + max(df_weekly['changes']) * 0.05,
                f"{int(row['changes'])}",
                ha='center',
                va='bottom',
                fontsize=9
            )

        ax1.set_title('Зміни в комітах по тижням')
        ax1.set_xlabel('Тиждень')
        ax1.set_ylabel('Кількість змін')
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.tick_params(axis='x', rotation=45)
        fig1.tight_layout()
        figures['Зміни по тижням'] = fig1

        if data['most_changed_files']:
            fig2 = Figure(figsize=(5, 4))
            ax2 = fig2.subplots()

            files = list(data['most_changed_files'].keys())
            changes = list(data['most_changed_files'].values())

            bars = ax2.barh(files, changes, color=sns.color_palette("Blues_d"))
            ax2.set_title('Найчастіше змінювані файли')
            ax2.set_xlabel('Кількість змін')

            for bar in bars:
                width = bar.get_width()
                ax2.text(width + max(changes) * 0.01, bar.get_y() + bar.get_height() / 2,
                         f'{int(width)}', va='center')

            fig2.tight_layout()
            figures['Найчастіше змінювані файли'] = fig2
        else:
            fig2 = Figure(figsize=(5, 4))
            ax2 = fig2.subplots()
            ax2.text(0.5, 0.5, 'Немає даних про зміни файлів',
                     ha='center', va='center')
            figures['Найчастіше змінювані файли'] = fig2

        fig3 = Figure(figsize=(5, 4))
        ax3 = fig3.subplots()

        last_4_weeks = df[df['date'] >= (pd.to_datetime('today') - pd.Timedelta(weeks=4))]

        if not last_4_weeks.empty:
            weekly_data = last_4_weeks.groupby(
                pd.Grouper(key='date', freq='W-MON')
            ).agg({
                'additions': 'sum',
                'deletions': 'sum'
            }).reset_index()

            weekly_data['week_str'] = weekly_data['date'].dt.strftime('%Y-%m-%d')

            bar_width = 0.35
            x = np.arange(len(weekly_data))

            ax3.bar(x - bar_width / 2, weekly_data['additions'], width=bar_width,
                    color='green', label='Додані рядки')
            ax3.bar(x + bar_width / 2, weekly_data['deletions'], width=bar_width,
                    color='red', label='Видалені рядки')

            ax3.set_title('Зміни за останні 4 тижні')
            ax3.set_xticks(x)
            ax3.set_xticklabels(weekly_data['week_str'], rotation=45)
            ax3.legend()
        else:
            ax3.text(0.5, 0.5, 'Немає даних за останні 4 тижні',
                     ha='center', va='center')

        fig3.tight_layout()
        figures['Останні 4 тижні'] = fig3

        return figures