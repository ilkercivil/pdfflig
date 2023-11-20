import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

class PdfFligApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF Flig")
        master.geometry("600x400")  # Pencere boyutu: genişlik x yükseklik

        self.selected_pdf_path = None

        self.label = tk.Label(master, text="Pdf Flig", font=("Helvetica", 24))
        self.label.pack(pady=10)

        self.pdf_sec_button = tk.Button(master, text="PDF Seç", font=("Helvetica", 18), command=self.pdf_sec)
        self.pdf_sec_button.pack(pady=10)

        self.kashele_button = tk.Button(master, text="Kaşele", font=("Helvetica", 18), command=self.kashele)
        self.kashele_button.pack(pady=10)

    def pdf_sec(self):
        self.selected_pdf_path = filedialog.askopenfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if self.selected_pdf_path:
            messagebox.showinfo("Bilgi", f"Seçilen dosya: {self.selected_pdf_path}")

    def kashele(self):
        if self.selected_pdf_path:
            output_pdf_path = self.selected_pdf_path.replace('.pdf', '_watermarked.pdf')

            watermark_path = 'kaşe.png'  # Bu dosyanın mevcut çalışma klasöründe olduğunu varsayalım

            with open(watermark_path, 'rb') as watermark_file:
                watermark_bytes = watermark_file.read()

            packet = io.BytesIO(watermark_bytes)
            can = canvas.Canvas(packet, pagesize=letter)

            # Resmi sağ alt köşede konumlandır
            image_width, image_height = 80, 80  # Resim boyutu
            page_width, page_height = letter
            x = page_width - image_width - 20  # 20 piksel kenar bırak
            y = 0  # 0 piksel kenar bırak

            # Resmi sağ alt köşeye yerleştir, arka planı beyaz değil, şeffaf yap
            can.drawImage(watermark_path, x, y, width=image_width, height=image_height, mask='auto')

            can.save()

            packet.seek(0)
            watermark_pdf = PdfReader(packet)
            input_pdf = PdfReader(self.selected_pdf_path)

            output_pdf = PdfWriter()

            for i in range(len(input_pdf.pages)):
                page = input_pdf.pages[i]
                page.merge_page(watermark_pdf.pages[0])
                output_pdf.add_page(page)

            with open(output_pdf_path, 'wb') as output_file:
                output_pdf.write(output_file)

            messagebox.showinfo("Bilgi", f"Kaşelenmiş PDF dosyası kaydedildi: {output_pdf_path}")
        else:
            messagebox.showwarning("Uyarı", "Lütfen önce bir PDF dosyası seçin.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PdfFligApp(root)
    root.mainloop()
