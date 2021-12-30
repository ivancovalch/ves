from kivymd.app import MDApp
from kivy.lang import Builder
import os
from vars import colors as colors
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.label import MDIcon
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.slider import MDSlider
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList


# ПЕРЕМЕННЫЕ
winautosize = True # флаг с помощью которого выбираем тип  образования окна (для релизов - True, для отладки на ПК - False), затем задаем вручную
#print (colors['yellow'])
class Colorpallet():
    def __init__(self, light = True):
        self.primary = [1,1,0,1]
        self.secondary = [1, 1, 0, 1]
        self.bg = [1, 1, 1, 1]

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        col = Colorpallet()
        print (col.bg)#(dir(MDIcon))
        self.theme_cls.primary_palette = "Brown" # цвет текста
        self.theme_cls.primary_hue = "A400" # оттенок цветовых элементов
        self.theme_cls.theme_style = "Light" # Цвет фона

        self.c_black = [0, 0, 0, 1]  # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.c_white = [1, 1, 1, 1]  # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.c_darkgray = [.3, .3, .3, 1]  # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.c_gray = [.6, .6, .6, 1]  # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА

        self.c_navy = [.25, .2, 1, 1]
        self.c_blue = [.4, .5, .95, 1]
        self.c_lightblue = [.45, .75, .9, 1]
        self.c_green = [.3, .7, .2, 1]
        self.c_yellow = [1, .85, .25, 1]
        self.c_orange = [1, .65, .2, 1]

        self.c_mrestext = [.34, .12, .12, 1]  # основной текстовый цвет
        self.c_unselected = [.7, .7, .7, 1]  # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.c_selected = [.55, .25, .07, 1]  # [.87, .50, .1, 1] # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.c_hint_text = [.8, .8, .8, 1]
        self.c_bg_light = [.98, .98, .98, 1]  # пользовательский цвет ФОНА небольших элементов
        #current_path = os.getcwd() # путь к корневой директории программы
        self.screen = Builder.load_file('basic.kv')

        winsize = Window.size # считываем размер экрана
        winwidth = winsize[0] # ширина экрана
        winheight = winsize[1]# высота экрана
        print (f"Window width {winwidth}")
        print(f"Window width {winheight}")
        #Logger.info(f"Window original size: width {str(winwidth)}, height {str(winheight)}")
        if winautosize == True:
            if winwidth > winheight: #экраны с портрентной ориентацией (desktop, планшет)
                # меняет разметку киви на горизонтальную
                self.screen.ids.main_container.rows = 1
                self.screen.ids.main_container.cols = 2
                #Logger.info("first widget y:" + str(self.root.ids.c_input.size_hint_y))
                if winwidth > 1300:
                    Window.fullscreen = False
                    Window.size = (1100, 800)
                else:
                    Window.fullscreen = "auto"

            else: # смартфоны
                Window.fullscreen = "auto"
                #Window.size = (640, 960)
        else: # winautosize == False:если в стартовых настройках задан ручной режим определения окна
            Window.fullscreen = False
            Window.size = (640,960)

    def build(self):
        return self.screen

    def on_start (self, **kwargs):
        pass

    def f_on_focus(self, instance, s_widgetid): # -- Обработка события фокус на элементе (колбэк возникает при каждой смене фокуса)
        val = str(instance.focus) # получаем значение фокуса - ушел или пришел True
        #Logger.info (f"f_on_focus: widget {s_widgetid} is: {str(instance.focus)}")
        if instance.focus == False: # срабатывание после того как фокус побывал в поле, а затем был переведен на другое поле
            pass # self.calculate () # ДОДЕЛАТЬ
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


