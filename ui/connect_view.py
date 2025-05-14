from tkinter import ttk, messagebox
from ui.update_view import UpdateView
from services.git_service import GitService

class ConnectView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_connect_widgets()

    def create_connect_widgets(self):
        style = ttk.Style()
        style.configure("Large.TButton", font=("Arial", 16))

        label_token = ttk.Label(self, text="GIT токен", font=("Arial", 16))
        label_token.pack(pady=(20, 0))
        self.token_entry = ttk.Entry(self, width=50, font=("Arial", 16))
        self.token_entry.pack()
        self.token_entry.bind("<KeyRelease>", self.check_entry)

        label_repo = ttk.Label(self, text="Репозіторій", font=("Arial", 16))
        label_repo.pack(pady=(10, 0))
        self.repo_entry = ttk.Entry(self, width=50, font=("Arial", 16))
        self.repo_entry.pack()
        self.repo_entry.bind("<KeyRelease>", self.check_entry)

        self.connect_button = ttk.Button(self, text="Підключитися до Git-репозиторію", style="Large.TButton", command=self.connect_to_repo)
        self.connect_button.pack(pady=(10, 0))
        self.connect_button["state"] = "disabled"

    def check_entry(self):
        if self.token_entry.get() and self.repo_entry.get():
            self.connect_button["state"] = "normal"
        else:
            self.connect_button["state"] = "disabled"

    def connect_to_repo(self):
        token = self.token_entry.get()
        repository = self.repo_entry.get()

        connect_result = GitService.connect(token, repository)

        if connect_result['success']:
            repo = connect_result['repo']

            messagebox.showinfo("Успіх", f"{connect_result['message']}")
            self.destroy()
            update_view = UpdateView(self.parent, repo)
            update_view.pack(fill='both', expand=True)
        else:
            messagebox.showerror("Помилка", f"{connect_result['message']}")