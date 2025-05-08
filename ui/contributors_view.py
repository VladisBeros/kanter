import tkinter as tk
from tkinter import ttk, messagebox
from ui.programmer_analytics_view import AnalyticsView

class ContributorsView(ttk.Frame):
    def __init__(self, parent, repo):
        super().__init__(parent)
        self.parent = parent
        self.repo = repo
        self.create_widgets()

    def create_widgets(self):
        # Создаем Canvas и Scrollbar
        self.canvas = tk.Canvas(self, borderwidth=5)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Настраиваем Canvas
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Упаковываем Scrollbar и Canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Добавляем кнопки в scrollable_frame
        contributors = list(self.repo.get_contributors())
        logins = [c.login for c in contributors]

        for login in logins:
            btn = ttk.Button(
                self.scrollable_frame,
                text=login,
                command=lambda l=login: self.open_analytics(l),  # Фиксируем login через l
                padding=(10, 10),
                width=20
            )
            btn.pack(pady=5, fill='x', expand=True)

    def open_analytics(self, login):
        messagebox.showinfo(f"Обран {login}", "Будується аналітика...")
        self.destroy()
        programmer_analytics_view = AnalyticsView(self.parent, login, self.repo)
        programmer_analytics_view.pack(fill='both', expand=True)