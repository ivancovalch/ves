from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivy.utils import get_color_from_hex

class ContentNavigationDrawer(MDBoxLayout):
    pass

class Container ():
    pass


class MainApp(MDApp):
    def build(self):
        return Builder.load_file("main.kv")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MainApp().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
