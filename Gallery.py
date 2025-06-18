from PIL.ImageOps import contain
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.app import runTouchApp
from kivy.lang import Builder
from datetime import date
from datetime import datetime as day
import os

from kivy.uix.widget import Widget


#Builder.load_file('images.kv')

class Gallery(App):
    def build(self):
        Window.size = 450, 900
        self.ImageFolders = ['media']

        self.main_layout = BoxLayout(orientation="vertical")

        self.album_layout = GridLayout(cols=3, spacing=0, size_hint_y=None)
        self.album_layout.row_default_height = 150

        self.image_layout = GridLayout(cols=3, spacing=0, size_hint_y=None)
        self.image_layout.bind(minimum_height=self.image_layout.setter('height'))
        self.image_layout.row_default_height = 150

        commands = []
        for i in os.listdir('images'):
            pa = 'images/' + i
            if pa.rpartition('.')[-1].lower() in supported:
                img = Image(source=pa)
                img.fit_mode = 'cover'
                img.opacity = 1
                commands.append(lambda img=img: self.image_layout.add_widget(img))
            elif os.path.isdir(pa):
                alb = Album(pa)
                img = CoverImage(source=pa + '/' + alb.coverim)
                img.album = alb
                img.fit_mode = 'cover'
                img.opacity = 1
                commands.insert(0, lambda img=img: self.image_layout.add_widget(img))
            else:
                continue
        [p() for p in commands]
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))

        self.main_layout.add_widget(self.album_layout)
        self.main_layout.add_widget(self.image_layout)
        root.add_widget(self.main_layout)
        return root


class Group:
    pass


class Album:
    def __init__(self, folder):
        self.folder = folder
        self.imgs = os.listdir(folder)
        with open('metadata.bin', 'rb') as f:
            self.coverim = pickle.load(f).get(folder, 0)
        if not self.coverim:
            self.coverim = self.imgs[0]


class CoverImage(Image):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == "left":
                print(self.album.folder)
            return True



supported = ['jpg', 'jpeg', 'webp', 'png']

Gallery().run()
