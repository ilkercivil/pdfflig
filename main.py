from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from kivy.clock import Clock
import io

class PdfFligApp(App):
    def __init__(self, **kwargs):
        super(PdfFligApp, self).__init__(**kwargs)
        self.file_chooser = FileChooserListView()
        self.file_chooser.bind(on_submit=self.on_file_selected)
        self.popup = Popup(title='Select a PDF file', content=self.file_chooser, size_hint=(0.9, 0.9))
        self.watermarked_pdf_path = None
        self.show_popup = None

    def pdf_sec(self, instance):
        self.popup.open()

    def on_file_selected(self, instance, selection, touch):
        if selection:
            print(f"Selected file: {selection[0]}")
            self.selected_pdf_path = selection[0]
        self.popup.dismiss()

    def kashele(self, instance):
        if hasattr(self, 'selected_pdf_path'):
            output_pdf_path = self.selected_pdf_path.replace('.pdf', '_watermarked.pdf')

            watermark_path = 'kaşe.png'  # Bu dosyanın mevcut çalışma klasöründe olduğunu varsayalım

            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)

            # Sağ alt köşede resmi yerleştir
            image_width, image_height = 50, 50  # Resim boyutu
            page_width, page_height = letter
            x = page_width - image_width - 20 # 100 piksel kenar bırak
            y = 0  # 100 piksel kenar bırak

            # Resmi sağ alt köşeye yerleştir
            can.drawImage(watermark_path, x, y, width=image_width, height=image_height)

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

            print(f"Watermarked PDF saved at: {output_pdf_path}")
            self.watermarked_pdf_path = output_pdf_path

            # Kaşeleme işlemi tamamlandı mesajını göstermek için Popup penceresi
            self.show_popup = Popup(title='Kaşeleme Tamamlandı', content=Label(text='Kaşeleme işlemi tamamlandı!'),
                                   size_hint=(None, None), size=(400, 200))
            self.show_popup.open()

            # Pencerenin otomatik kapanması için bir zamanlayıcı ekleyin
            Clock.schedule_once(lambda dt: self.show_popup.dismiss(), 3)  # 3 saniye sonra kapat

        else:
            print("Lütfen önce bir PDF dosyası seçin.")

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Pdf Flig yazısını daha büyük yap
        label = Label(text="Pdf Flig", font_size=50)

        pdf_sec_button = Button(text="PDF Seç", font_size=40)
        kashele_button = Button(text="Kaşele", font_size=40)

        pdf_sec_button.bind(on_press=self.pdf_sec)
        kashele_button.bind(on_press=self.kashele)

        layout.add_widget(label)
        layout.add_widget(pdf_sec_button)
        layout.add_widget(kashele_button)

        return layout


if __name__ == '__main__':
    PdfFligApp().run()
