import tkinter as tk
from ui.connect_view import ConnectView

def main():
    root = tk.Tk()
    root.title("Kanter")
    root.state('zoomed')

    app = ConnectView(root)
    app.pack(fill='both', expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()