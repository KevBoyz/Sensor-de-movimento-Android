from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivymd.app import MDApp


class MainWindow(Screen):
    dialog = None

    def open_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Manual de instruções",
                type="custom",
                content_cls=HelpContent()
            )
        self.dialog.open()


class HelpContent(BoxLayout):
    pass


class SecondWindow(Screen):
    pass


class ThirdWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("main.kv")


class MyMainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.theme_style = 'Dark'
        return WindowManager()


MyMainApp().run()