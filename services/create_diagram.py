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
            'most_changed_files': {},
            'commits_by_date': []
        }

        commits = list(repo.get_commits(author=login))

        if not commits:
            return data

        data['total_commits'] = len(commits)
        data['first_commit_date'] = commits[-1].commit.author.date
        data['last_commit_date'] = commits[0].commit.author.date

        for commit in commits:
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

            # Rest of your existing file analysis code...
            for file in commit.files:
                filename = file.filename
                if filename not in data['most_changed_files']:
                    data['most_changed_files'][filename] = 0
                data['most_changed_files'][filename] += 1
                data['total_files_changed'] += 1

        data['avg_lines_per_commit'] = round(
            (data['total_lines_added'] + data['total_lines_deleted']) / data['total_commits'],
            2
        )

        days_active = (data['last_commit_date'] - data['first_commit_date']).days
        data['commit_frequency'] = round(data['total_commits'] / max(1, days_active), 2)

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

        if not data.get("commits_by_date"):
            return figures  # нет данных — ничего не строим

        df = pd.DataFrame(data['commits_by_date'])
        df = df.groupby("date").sum().reset_index()

        fig1 = Figure(figsize=(5, 4))
        ax1 = fig1.subplots()
        sns.lineplot(data=df, x='date', y='changes', marker='o', ax=ax1)
        ax1.set_title('Зміни в комітах по датам')
        ax1.set_xlabel('Дата')
        ax1.set_ylabel('Кількість змін (додавання та видалення)')
        ax1.tick_params(axis='x', rotation=45)
        fig1.tight_layout()
        figures['changes_over_time'] = fig1

        fig2 = Figure(figsize=(5, 4))
        ax2 = fig2.subplots()
        sns.barplot(x=["Коміти у день"], y=[data['commit_frequency']], ax=ax2,
                    color=sns.color_palette("Blues_d")[0])
        ax2.set_title("Частота комітів")
        figures['commit_frequency'] = fig2

        return figures