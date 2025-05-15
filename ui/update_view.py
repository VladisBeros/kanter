from tkinter import ttk, messagebox
from ui.contributors_view import ContributorsView
from services.show_about_contributors import not_active_contributors

class UpdateView(ttk.Frame):
    def __init__(self, parent, repo):
        super().__init__(parent)
        self.parent = parent
        self.repo = repo
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("Large.TButton", font=("Arial", 14), padding=10)
        button_frame = ttk.Frame(self)
        button_frame.place(relx=0.5, rely=0.5, anchor='center')

        update_data_button = ttk.Button(button_frame, text="Оновити дані", style="Large.TButton", command=self.open_contributors)
        update_data_button.grid(row=0, column=0, sticky='ew', pady=5)

        back_button = ttk.Button(button_frame, text="Повернутися до введення токену та репозиторію", style="Large.TButton", command=self.go_back_to_connect)
        back_button.grid(row=1, column=0, sticky='ew', pady=5)

        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)

    def open_contributors(self):
        messagebox.showinfo("Оновлення", "Дані оновлюються...")
        not_active_contributors(self.repo)

        self.destroy()
        contributors_view = ContributorsView(self.parent, self.repo)
        contributors_view.pack(fill='both', expand=True)

    def go_back_to_connect(self):
        from ui.connect_view import ConnectView

        self.destroy()
        connect_view = ConnectView(self.parent)
        connect_view.pack(fill='both', expand=True)