import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from io import BytesIO
import os

# -------------------------------
# 🔐 ENCRYPT PDF  (Your logic inside this function)
# -------------------------------
def encrypt_pdf():
    # GUI Part: File chooser + password prompt
    path = filedialog.askopenfilename(title="Select PDF to Encrypt", filetypes=[("PDF files", "*.pdf")])
    if not path:
        return

    password = simpledialog.askstring("Password", "Enter password to set:", show="*")
    if not password:
        return

    try:
        # ✅ Your Logic Starts
        reader = PdfReader(path)
        writer = PdfWriter()

        if reader.is_encrypted:
            messagebox.showinfo("Info", "This file is already encrypted!")
            return

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)
        # ✅ Your Logic Ends

        # GUI Part: Ask where to save file
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Encrypted PDF")
        if save_path:
            with open(save_path, "wb") as f:
                writer.write(f)
            messagebox.showinfo("Success", f"File encrypted and saved as:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# -------------------------------
# 🔓 DECRYPT PDF (Your logic inside this function)
# -------------------------------
def decrypt_pdf():
    # GUI Part: File chooser + password prompt
    path = filedialog.askopenfilename(title="Select PDF to Decrypt", filetypes=[("PDF files", "*.pdf")])
    if not path:
        return

    password = simpledialog.askstring("Password", "Enter password of file:", show="*")
    if not password:
        return

    try:
        # ✅ Your Logic Starts
        reader = PdfReader(path)
        if not reader.is_encrypted:
            messagebox.showinfo("Info", "This file is not encrypted.")
            return

        result = reader.decrypt(password)
        if result == 0:
            messagebox.showerror("Error", "Invalid Password!")
            return

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        # ✅ Your Logic Ends

        # GUI Part: Ask where to save file
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Decrypted PDF")
        if save_path:
            with open(save_path, "wb") as f:
                writer.write(f)
            messagebox.showinfo("Success", f"File decrypted and saved as:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# -------------------------------
# 📑 MERGE PDFs  (Your logic inside this function)
# -------------------------------
def merge_pdfs():
    # GUI Part: Multiple file chooser
    paths = filedialog.askopenfilenames(title="Select PDFs to Merge", filetypes=[("PDF files", "*.pdf")])
    if len(paths) < 2:
        messagebox.showerror("Error", "Please select 2 or more PDF files.")
        return

    try:
        # ✅ Your Logic Starts
        merger = PdfMerger()
        for file in paths:
            merger.append(file)

        merged_file = BytesIO()
        merger.write(merged_file)
        merger.close()
        merged_file.seek(0)

        # Optional encryption logic
        choice = messagebox.askyesno("Encrypt", "Do you want to encrypt the merged PDF?")
        reader = PdfReader(merged_file)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        if choice:
            password = simpledialog.askstring("Password", "Enter password for merged PDF:", show="*")
            if not password:
                return
            writer.encrypt(password)
        # ✅ Your Logic Ends

        # GUI Part: Save file dialog
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Merged PDF")
        if save_path:
            with open(save_path, "wb") as f:
                writer.write(f)
            messagebox.showinfo("Success", f"File saved as:\n{save_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# -------------------------------
# 🖥️ GUI SETUP  (ChatGPT wrote this part)
# -------------------------------
root = tk.Tk()
root.title("PDF Tool")
root.geometry("300x200")
root.resizable(False, False)

title = tk.Label(root, text="PDF Tool", font=("Helvetica", 16, "bold"))
title.pack(pady=10)

btn_encrypt = tk.Button(root, text="Encrypt PDF", width=20, command=encrypt_pdf)
btn_encrypt.pack(pady=5)

btn_decrypt = tk.Button(root, text="Decrypt PDF", width=20, command=decrypt_pdf)
btn_decrypt.pack(pady=5)

btn_merge = tk.Button(root, text="Merge PDFs", width=20, command=merge_pdfs)
btn_merge.pack(pady=5)

root.mainloop()
