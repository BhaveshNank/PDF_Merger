import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

class PDFEditorGUI:
    def __init__(self, master):
        self.master = master
        master.title("PDF Editor")

        # Section for inserting a PDF
        tk.Label(master, text="Insert PDF into:").grid(row=0, column=0)
        self.target_pdf_entry = tk.Entry(master)
        self.target_pdf_entry.grid(row=0, column=1)
        tk.Button(master, text="Browse", command=lambda: self.load_pdf(self.target_pdf_entry)).grid(row=0, column=2)

        tk.Label(master, text="PDF to Insert:").grid(row=1, column=0)
        self.insert_pdf_entry = tk.Entry(master)
        self.insert_pdf_entry.grid(row=1, column=1)
        tk.Button(master, text="Browse", command=lambda: self.load_pdf(self.insert_pdf_entry)).grid(row=1, column=2)

        tk.Label(master, text="Insert at page #:").grid(row=2, column=0)
        self.insert_page_number = tk.Entry(master)
        self.insert_page_number.grid(row=2, column=1)

        tk.Button(master, text="Insert PDF", command=self.insert_pdf).grid(row=3, column=1)

        # Section for deleting a page
        tk.Label(master, text="Delete page from:").grid(row=4, column=0)
        self.delete_pdf_entry = tk.Entry(master)
        self.delete_pdf_entry.grid(row=4, column=1)
        tk.Button(master, text="Browse", command=lambda: self.load_pdf(self.delete_pdf_entry)).grid(row=4, column=2)

        tk.Label(master, text="Delete page #:").grid(row=5, column=0)
        self.delete_page_number = tk.Entry(master)
        self.delete_page_number.grid(row=5, column=1)

        tk.Button(master, text="Delete Page", command=self.delete_page).grid(row=6, column=1)

    def load_pdf(self, entry_field):
        filename = filedialog.askopenfilename(filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))
        entry_field.delete(0, tk.END)
        entry_field.insert(0, filename)

    def insert_pdf(self):
        target_pdf = self.target_pdf_entry.get()
        insert_pdf = self.insert_pdf_entry.get()
        insert_page_no = int(self.insert_page_number.get()) - 1

        try:
            merger = PdfMerger()
            merger.append(target_pdf)
            merger.merge(insert_page_no, insert_pdf)

            output_pdf = "modified_output.pdf"
            with open(output_pdf, 'wb') as fout:
                merger.write(fout)
            merger.close()

            messagebox.showinfo("Success", "PDF inserted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_page(self):
        pdf_path = self.delete_pdf_entry.get()
        page_to_delete = int(self.delete_page_number.get()) - 1

        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            for i in range(len(reader.pages)):
                if i != page_to_delete:
                    writer.add_page(reader.pages[i])

            output_pdf = "modified_output.pdf"
            with open(output_pdf, 'wb') as fout:
                writer.write(fout)

            messagebox.showinfo("Success", "Page deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = PDFEditorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
