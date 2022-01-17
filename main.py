from kivymd.app import MDApp
from kivy.lang import Builder
import os
import configparser
from vars import Colorpallet as Colorpallet
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.label import MDIcon
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.slider import MDSlider
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList

from calculate import Calculate # Расчеты вес-фигура

# ПЕРЕМЕННЫЕ
winautosize = True # флаг с помощью которого выбираем тип  образования окна (для релизов - True, для отладки на ПК - False), затем задаем вручную
#print (colors['yellow'])

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.col = Colorpallet()
        print (self.col.bg)#(dir(MDIcon))
        self.theme_cls.primary_palette = "Brown" # цвет текста
        self.theme_cls.primary_hue = "A400" # оттенок цветовых элементов
        self.theme_cls.theme_style = "Light" # Цвет фона

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

    def calculate(self): #расчеты параметров веса и фигуры
        Calculate(self, self.screen)

    def build(self):
        return self.screen

    def on_start (self, **kwargs):
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
        self.calculate()

    def f_on_focus(self, instance, s_widgetid): # -- Обработка события фокус на элементе (колбэк возникает при каждой смене фокуса)
        val = str(instance.focus) # получаем значение фокуса - ушел или пришел True
        #Logger.info (f"f_on_focus: widget {s_widgetid} is: {str(instance.focus)}")
        if instance.focus == False: # срабатывание после того как фокус побывал в поле, а затем был переведен на другое поле
            self.calculate () # ДОДЕЛАТЬ
        else: # фокус пришел
            self.screen.ids[s_widgetid].text = "" #очищаем текстовое поле

    def choose_metrics(self, metrics): # изменение оформления в зависимости от выбора типа единиц
        b_active = 'b_metric'
        b_passive = 'b_imperial'
        print ("Activate metric system: " + b_active)
        if metrics == False:
            b_active = 'b_imperial'
            b_passive = 'b_metric'
        self.screen.ids[b_active].elevation = 7
        self.screen.ids[b_active].text_color = self.col.selected
        self.screen.ids[b_active].md_bg_color = self.col.bg_light
        self.screen.ids[b_passive].elevation = 4
        self.screen.ids[b_passive].text_color = self.col.gray
        self.screen.ids[b_passive].md_bg_color = self.col.bg_medium

    def choose_gender (self, gender): # установка пола - True - женщина, False - мужчина
        if gender == True:
            self.screen.ids.ic_male.text_color = self.col.selected
            self.screen.ids.ic_female.text_color = self.col.lightray
        else:
            self.screen.ids.ic_male.text_color = self.col.lightray
            self.screen.ids.ic_female.text_color = self.col.selected
        self.calculate() # запускаем функцию для расчета всех параметров

# Create a config file
def createConfig(path):
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set ("Settings", "locale", "ru_RU" ) # локализация используемая по умолчанию
    #config.set("Settings", "font", "Courier")
    #config.set("Settings", "font_size", "10")
    #config.set("Settings", "font_style", "Normal")
    #config.set("Settings", "font_info", "You are using %(font)s at %(font_size)s pt")
    with open(path, "w") as config_file:
        config.write(config_file)
# Create, read, update, delete config
def crudConfig(path):
    if not os.path.exists(path):
        createConfig(path)
    config = configparser.ConfigParser()
    config.read(path)
    # Читаем некоторые значения из конфиг. файла.
    #font = config.get("Settings", "font")
    #font_size = config.get("Settings", "font_size")
    # Меняем значения из конфиг. файла.
    #config.set("Settings", "font_size", "12")
    # Удаляем значение из конфиг. файла.
    #config.remove_option("Settings", "font_style")
    # Вносим изменения в конфиг. файл.
    with open(path, "w") as config_file:
        config.write(config_file)


if __name__ == '__main__':
    MainApp().run()


