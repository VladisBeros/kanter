import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from services.create_diagram import CreateDiagram
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AnalyticsView(ttk.Frame):
    def __init__(self, parent, login, repo):
        super().__init__(parent)
        self.parent = parent
        self.login = login
        self.repo = repo
        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self, text=f"Аналітика праці користувача {self.login}")
        label.pack(pady=10)

        data = CreateDiagram.get_contributor_data(self.login, self.repo)
        figures = CreateDiagram.create_figures(data)

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        for title, fig in figures.items():
            frame = ttk.Frame(notebook)
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            notebook.add(frame, text=title)