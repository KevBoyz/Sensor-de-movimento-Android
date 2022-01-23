from kivymd.app import MDApp
from kivymd.uix.floatlayout import FloatLayout


class Root(FloatLayout):
    ...


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.theme_style = 'Dark'
        return Root()


MainApp().run()
