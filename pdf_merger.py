import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os

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

        # Section for merging multiple PDFs
        tk.Label(master, text="Merge PDFs:").grid(row=7, column=0)
        self.merge_pdfs_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE)
        self.merge_pdfs_listbox.grid(row=7, column=1)
        tk.Button(master, text="Add PDF", command=self.add_pdf_to_merge_list).grid(row=7, column=2)
        tk.Button(master, text="Delete PDF", command=self.delete_selected_pdfs).grid(row=8, column=2)
        tk.Button(master, text="Merge PDFs", command=self.merge_pdfs).grid(row=9, column=1)

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

            output_pdf = self.get_unique_filename("modified_output.pdf")
            with open(output_pdf, 'wb') as fout:
                merger.write(fout)
            merger.close()

            messagebox.showinfo("Success", f"PDF inserted successfully! Saved as {output_pdf}")
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

            base_filename = os.path.splitext(os.path.basename(pdf_path))[0] + "_modified.pdf"
            output_pdf = self.get_unique_filename(base_filename)
            with open(output_pdf, 'wb') as fout:
                writer.write(fout)

            messagebox.showinfo("Success", f"Page deleted successfully! Saved as {output_pdf}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_pdf_to_merge_list(self):
        filenames = filedialog.askopenfilenames(filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))
        for filename in filenames:
            self.merge_pdfs_listbox.insert(tk.END, filename)

    def delete_selected_pdfs(self):
        selected_indices = self.merge_pdfs_listbox.curselection()
        for index in reversed(selected_indices):
            self.merge_pdfs_listbox.delete(index)

    def merge_pdfs(self):
        pdf_files = [self.merge_pdfs_listbox.get(idx) for idx in self.merge_pdfs_listbox.curselection()]

        if not pdf_files:
            messagebox.showerror("Error", "No PDFs selected for merging.")
            return

        try:
            merger = PdfMerger()
            for pdf in pdf_files:
                merger.append(pdf)

            output_pdf = self.get_unique_filename("merged_output.pdf")
            with open(output_pdf, 'wb') as fout:
                merger.write(fout)
            merger.close()

            messagebox.showinfo("Success", f"PDFs merged successfully! Saved as {output_pdf}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_unique_filename(self, base_filename):
        counter = 1
        filename, extension = os.path.splitext(base_filename)
        unique_filename = base_filename
        while os.path.exists(unique_filename):
            unique_filename = f"{filename}_{counter}{extension}"
            counter += 1
        return unique_filename

def main():
    root = tk.Tk()
    app = PDFEditorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
