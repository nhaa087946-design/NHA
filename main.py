
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.core.window import Window

Window.clearcolor = (16/255, 16/255, 16/255, 1)


class Crosshair(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cross_size = 15
        self.bind(pos=self.draw, size=self.draw)

    def draw(self, *args):
        self.canvas.clear()

        with self.canvas:
            Color(0.12, 0.12, 0.12, 1)
            Rectangle(pos=self.pos, size=self.size)

            x, y = self.center
            s = self.cross_size

            Color(1, 0, 0, 1)
            Line(circle=(x, y, 15), width=3)

            Color(0, 1, 0, 1)
            Line(points=[x-s, y, x+s, y], width=2)
            Line(points=[x, y-s, x, y+s], width=2)


class NHAApp(App):

    def build(self):
        self.title = "NHA"
        self.enabled = False

        root = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12
        )

        title = Label(
            text="[b]NHA[/b]",
            markup=True,
            font_size=30,
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height=60
        )
        root.add_widget(title)

        self.status = Label(
            text="SYSTEM: OFF",
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=35
        )
        root.add_widget(self.status)

        toggle = Button(
            text="ON / OFF",
            size_hint_y=None,
            height=50,
            background_normal="",
            background_color=(0.8, 0, 0, 1)
        )
        toggle.bind(on_release=self.toggle)
        root.add_widget(toggle)

        self.settings = BoxLayout(
            orientation="vertical",
            spacing=8
        )

        self.settings.add_widget(Label(
            text="[b]AIM SETTINGS[/b]",
            markup=True,
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=40
        ))

        self.settings.add_widget(Label(
            text="SENSITIVITY",
            size_hint_y=None,
            height=25
        ))

        self.sensitivity = Slider(
            min=1,
            max=100,
            value=50
        )
        self.settings.add_widget(self.sensitivity)

        self.settings.add_widget(Label(
            text="CROSSHAIR SIZE",
            size_hint_y=None,
            height=25
        ))

        self.size_slider = Slider(
            min=5,
            max=40,
            value=15
        )
        self.size_slider.bind(value=self.change_size)
        self.settings.add_widget(self.size_slider)

        self.preview = Crosshair()
        self.settings.add_widget(self.preview)

        reset = Button(
            text="RESET SETTINGS",
            size_hint_y=None,
            height=45,
            background_normal="",
            background_color=(0.2, 0.2, 0.2, 1)
        )
        reset.bind(on_release=self.reset)
        self.settings.add_widget(reset)

        root.add_widget(self.settings)

        self.settings.opacity = 0
        self.settings.disabled = True

        return root

    def toggle(self, *args):
        self.enabled = not self.enabled

        if self.enabled:
            self.status.text = "SYSTEM: ON"
            self.status.color = (0, 1, 0, 1)
            self.settings.opacity = 1
            self.settings.disabled = False
        else:
            self.status.text = "SYSTEM: OFF"
            self.status.color = (1, 1, 1, 1)
            self.settings.opacity = 0
            self.settings.disabled = True

    def change_size(self, slider, value):
        self.preview.cross_size = value
        self.preview.draw()

    def reset(self, *args):
        self.sensitivity.value = 50
        self.size_slider.value = 15
        self.change_size(None, 15)

        self.enabled = False
        self.status.text = "SYSTEM: OFF"
        self.status.color = (1, 1, 1, 1)
        self.settings.opacity = 0
        self.settings.disabled = True


if __name__ == "__main__":
    NHAApp().run()
  
