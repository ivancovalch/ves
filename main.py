from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.slider import MDSlider
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList


# ПЕРЕМЕННЫЕ

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #print (dir(MDSlider))
        self.theme_cls.primary_palette = "Brown" # цвет текста
        self.theme_cls.primary_hue = "A400" # оттенок цветовых элементов
        self.theme_cls.theme_style = "Light" # Цвет фона
        self.c_white = [0, 0, 0, 1]  # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.c_black = [1, 1, 1, 1]  # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.c_unselected = [.7, .7, .7, 1]  # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.c_selected = [.87, .50, .1, 1] # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.c_bg_light = [.98, .98, .98, 1] # пользовательский цвет ФОНА небольших элементов

        #return Builder.load_file('basic.kv')  # аргумент не нужен т.к. имя файла basic.kv совпадает с именем проекта и поэтому он будет загружен по умолчанию
        self.screen = Builder.load_file('basic.kv')

    def build(self):
        # self.theme_cls.primary_palette = "Brown"
        # self.theme_cls.primary_hue = "A100"
        #self.theme_cls.theme_style = "Light"  # "Dark"  # "Light"
        # return Builder.load_string(KV)
        return self.screen

        # -- Обработка события фокус на элементе (колбэк возникает при каждой смене фокуса)
    def f_on_focus(self, instance, s_widgetid):
        val = str(instance.focus) # получаем значение фокуса - ушел или пришел True
        #Logger.info (f"f_on_focus: widget {s_widgetid} is: {str(instance.focus)}")
        if instance.focus == False: # срабатывание после того как фокус побывал в поле, а затем был переведен на другое поле
            pass # self.calculate ()
        else: # фокус пришел
            self.screen.ids[s_widgetid].text = "" #очищаем текстовое поле

    def on_start(self):
        icons_item = {
            "folder": "My files",
            "account-multiple": "Shared with me",
            "star": "Starred",
            "history": "Recent",
            "checkbox-marked": "Shared with me",
            "upload": "Upload",
        }
        # for icon_name in icons_item.keys():
        #     self.root.ids.content_drawer.ids.md_list.add_widget(
        #         ItemDrawer(icon=icon_name, text=icons_item[icon_name])
        #     )


if __name__ == '__main__':
    MainApp().run()


