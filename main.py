from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import sqlite3 as sql
import cv2
import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))


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
    def get_alarm(self, text=False):
        config = conn.execute('SELECT alarm, delay FROM config')
        for row in config:
            alarm = row[0]
        if not alarm:
            alarm = True
        else:
            alarm = False
        if not text:
            return alarm
        else:
            if not alarm:
                return 'Alarme: Desabilitado'
            else:
                return 'Alarme: Habilitado'

    def update_alarm(self):
        alarm = self.get_alarm()
        conn.execute(f'UPDATE config SET alarm = {alarm}')
        conn.commit()
        self.alarmbtn.text = self.get_alarm(text=True)

    def update_delay(self, delay):
        conn.execute(f'UPDATE config SET delay = {delay}')
        conn.commit()


class ThirdWindow(Screen):
    def start(self):
        Clock.schedule_interval(self.load_video, 1.0 / 38.0)

    def load_video(self, *args):
        ret, frame1 = cap.read()
        ret, frame2 = cap.read()
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 900:
                continue
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        frame1 = cv2.resize(frame1, (frame1.shape[1] * 2, frame1.shape[0] * 2))
        frame1 = cv2.flip(frame1, 1, 0)
        buffer = cv2.flip(frame1, 0).tostring()
        texture = Texture.create(size=(frame1.shape[1], frame1.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.camera.texture = texture


class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.theme_style = 'Dark'
        global conn
        conn = sql.connect('data_base.db')
        self.texture = Texture.create(size=(1000, 1000), colorfmt='bgr')
        scream = cv2.imread('AppScream.png')
        buffer = cv2.flip(scream, 0).tostring()
        self.texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        global cap
        cap = cv2.VideoCapture(0)
        return WindowManager()


MainApp().run()
