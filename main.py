from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList
from kivymd.uix.screen import Screen



class MainApp(MDApp):
    def build(self):
        return Builder.load_file("main.kv")

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


