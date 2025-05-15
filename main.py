import tkinter as tk
from tkinter import messagebox
from ui.connect_view import ConnectView
from services.env_service import EnvService

def on_closing(root):
    if messagebox.askyesno("Вихід", "Бажаєте вийти з облікового запису?"):
        EnvService.clear_env()
        messagebox.showinfo("Вихід", "Облікові дані очищено.")
    root.destroy()

def main():
    root = tk.Tk()
    root.title("Kanter")
    root.state('zoomed')

    app = ConnectView(root)
    app.pack(fill='both', expand=True)

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()

if __name__ == "__main__":
    main()