import os
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
from pdf2image import convert_from_path
import fitz  # PyMuPDF
from docx2pdf import convert as docx_to_pdf

# Setup GUI
root = Tk()
root.title("PDF Magic Tool")
root.geometry("400x400")

def jpg_to_pdf():
    file = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg")])
    if file:
        image = Image.open(file)
        pdf_path = file.replace(".jpg", ".pdf")
        image.save(pdf_path, "PDF")
        messagebox.showinfo("Done", f"Saved PDF: {pdf_path}")

def pdf_to_jpg():
    file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file:
        images = convert_from_path(file)
        base = os.path.splitext(file)[0]
        for i, img in enumerate(images):
            img.save(f"{base}_page_{i+1}.jpg", "JPEG")
        messagebox.showinfo("Done", "PDF pages saved as JPGs!")

def docx_to_pdf_func():
    file = filedialog.askopenfilename(filetypes=[("Word files", "*.docx")])
    if file:
        docx_to_pdf(file)
        messagebox.showinfo("Done", f"Converted to PDF!")

def extract_text():
    file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file:
        doc = fitz.open(file)
        text = ""
        for page in doc:
            text += page.get_text()
        with open("extracted_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        messagebox.showinfo("Done", "Text saved to 'extracted_text.txt'!")

def extract_images():
    file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file:
        doc = fitz.open(file)
        image_count = 0
        for page_index in range(len(doc)):
            page = doc[page_index]
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                img_bytes = base_image["image"]
                img_ext = base_image["ext"]
                with open(f"page{page_index+1}_img{img_index+1}.{img_ext}", "wb") as f:
                    f.write(img_bytes)
                image_count += 1
        messagebox.showinfo("Done", f"{image_count} image(s) extracted!")

# GUI Buttons
Label(root, text="PDF Utility Tool", font=("Helvetica", 16)).pack(pady=10)

Button(root, text="JPG to PDF", width=25, command=jpg_to_pdf).pack(pady=5)
Button(root, text="PDF to JPG", width=25, command=pdf_to_jpg).pack(pady=5)
Button(root, text="DOCX to PDF", width=25, command=docx_to_pdf_func).pack(pady=5)
Button(root, text="Extract Text from PDF", width=25, command=extract_text).pack(pady=5)
Button(root, text="Extract Images from PDF", width=25, command=extract_images).pack(pady=5)

root.mainloop()

