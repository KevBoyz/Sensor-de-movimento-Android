from kivymd.app import MDApp
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
import webbrowser


def make_invisible(widget):
    widget.visible = False
    widget.size_hint_x = None
    widget.size_hint_y = None
    widget.height = 0
    widget.width = 0
    widget.text = ""
    widget.opacity = 0


class Root(FloatLayout):
    def hyperlink(self, url):
        webbrowser.open(url)


class Menu(FloatLayout):
    dialog = None

    def HideMenuSection(self):
        make_invisible(self)

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



class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.theme_style = 'Dark'
        return Root()


MainApp().run()
