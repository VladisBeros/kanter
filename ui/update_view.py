import tkinter as tk
from tkinter import ttk, messagebox
from ui.contributors_view import ContributorsView

class UpdateView(ttk.Frame):
    def __init__(self, parent, repo):
        super().__init__(parent)
        self.parent = parent
        self.repo = repo
        self.create_widgets()

    def create_widgets(self):
        update_data_button = ttk.Button(self,
                                        text="Оновити дані",
                                        command=self.open_contributors)
        update_data_button.pack(pady=5, fill='x', expand=True)

    def open_contributors(self):
        messagebox.showinfo("Оновлення", "Дані оновлюються...")

        # Создаем новый фрейм для ContributorsView
        self.destroy()  # Уничтожаем текущий фрейм
        contributors_view = ContributorsView(self.parent, self.repo)
        contributors_view.pack(fill='both', expand=True)