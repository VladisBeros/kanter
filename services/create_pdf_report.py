from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_pdf import PdfPages

class CreateReport(ttk.Frame):
    @staticmethod
    def export_report(figures, login):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Зберегти звіт як PDF")
        if not file_path:
            return

        with PdfPages(file_path) as pdf:
            from matplotlib import pyplot as plt

            fig, ax = plt.subplots(figsize=(8.27, 11.69))
            ax.axis('off')
            ax.text(0.5, 0.9, f"Аналіз роботи розробника {login}", fontsize=16, ha='center', va='top', weight='bold')
            pdf.savefig(fig)
            plt.close(fig)

            for fig in figures.values():
                pdf.savefig(fig)

            messagebox.showinfo("Успіх", f"Звіт про {login} успішно збережено.")