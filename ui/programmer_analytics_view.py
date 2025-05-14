from tkinter import ttk
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
        back_button = ttk.Button(self, text="Повернутися до списку розробників", command=self.go_back_to_contributors)
        back_button.pack(fill='x')

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

    def go_back_to_contributors(self):
        from ui.contributors_view import ContributorsView

        self.destroy()
        contributors_view = ContributorsView(self.parent, self.repo)
        contributors_view.pack(fill='both', expand=True)