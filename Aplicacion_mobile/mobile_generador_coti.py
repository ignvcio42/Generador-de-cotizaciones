from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class CotizacionApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.folio_input = TextInput(hint_text="Folio", size_hint=(1, None), height=30)
        layout.add_widget(self.folio_input)

        self.atencion_input = TextInput(hint_text="Atención", size_hint=(1, None), height=30)
        layout.add_widget(self.atencion_input)

        self.atencion_input = TextInput(hint_text="Empresa", size_hint=(1, None), height=30)
        layout.add_widget(self.atencion_input)

        self.atencion_input = TextInput(hint_text="Detalle", size_hint=(1, None), height=30)

        self.atencion_input = TextInput(hint_text="Neto", size_hint=(1, None), height=30)
        layout.add_widget(self.atencion_input)

        self.atencion_input = TextInput(hint_text="Iva", size_hint=(1, None), height=30)
        layout.add_widget(self.atencion_input)

        self.atencion_input = TextInput(hint_text="Bruto", size_hint=(1, None), height=30)
        layout.add_widget(self.atencion_input)

        self.atencion_input = TextInput(hint_text="Fecha Evento", size_hint=(1, None), height=30)
        layout.add_widget(self.atencion_input)

        self.atencion_input = TextInput(hint_text="Fecha Montaje", size_hint=(1, None), height=30)
        layout.add_widget(self.atencion_input)

        self.atencion_input = TextInput(hint_text="Fecha Desarme", size_hint=(1, None), height=30)
        layout.add_widget(self.atencion_input)

        self.atencion_input = TextInput(hint_text="Lugar Evento", size_hint=(1, None), height=30)
        layout.add_widget(self.atencion_input)

        self.atencion_input = TextInput(hint_text="Forma Pago", size_hint=(1, None), height=30)
        layout.add_widget(self.atencion_input)



        # Añadir más campos y botones según la funcionalidad de tu app

        generate_button = Button(text="Generar PDF", size_hint=(1, None), height=50)
        generate_button.bind(on_press=self.generar_pdf)
        layout.add_widget(generate_button)

        return layout

    def generar_pdf(self, instance):
        # Lógica para generar el PDF aquí
        pass

if __name__ == "__main__":
    CotizacionApp().run()
