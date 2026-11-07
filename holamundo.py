from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class MiPrimeraApp(App):
    def build(self):
        # Crear un contenedor vertical
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Agregar elementos
        self.etiqueta = Label(text="¡Hola desde Kivy en CachyOS!", font_size='20sp')
        boton = Button(text="Haz clic aquí", size_hint=(1, 0.3))
        
        # Conectar el botón a una función
        boton.bind(on_press=self.al_hacer_clic)
        
        layout.add_widget(self.etiqueta)
        layout.add_widget(boton)
        
        return layout

    def al_hacer_clic(self, instance):
        self.etiqueta.text = "¡El botón funciona correctamente!"

if __name__ == '__main__':
    MiPrimeraApp().run()