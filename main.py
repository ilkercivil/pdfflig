from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class PdfFligApp(App):
    def pdf_sec(self, instance):
        print("PDF Seç butonuna tıklandı!")

    def kashele(self, instance):
        print("Kaşele butonuna tıklandı!")

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Pdf Flig yazısını daha büyük yap
        label = Label(text="Pdf Flig", font_size=50)

        pdf_sec_button = Button(text="PDF Seç", font_size=40)
        kashele_button = Button(text="Kaşele" , font_size=40)

        pdf_sec_button.bind(on_press=self.pdf_sec)
        kashele_button.bind(on_press=self.kashele)

        layout.add_widget(label)
        layout.add_widget(pdf_sec_button)
        layout.add_widget(kashele_button)

        return layout


PdfFligApp().run()
