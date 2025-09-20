from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.tab import MDTabsPrimary, MDTabsItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.filemanager import MDFileManager

from kivy.uix.widget import Widget
Window.size = (1480, 320)

import test

class BypassButton(MDButton):
    bypass = BooleanProperty(False)
    def toggle(self):
        self.bypass = not self.bypass
        print(f"Bypassing changed...{self.bypass}")
        if(self.bypass):
            self.style = "filled"
        else:
            self.style = "elevated"

        
            

class BaseMDTabsItem(MDTabsItem):
    icon = StringProperty()
    text = StringProperty()

class AmpScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            search ='files',
            selector = "file",
            ext = [".nam"],
            exit_manager = self.close_file_manager,
            select_path = self.select_patch,
            current_path = '/home/jona/Desktop/NAM'
        )
    def toggle_bypass(self):
        test.amp.toggle() 
        pass       
        
    def select_patch(self, value):
        print(value)
        test.amp.patch('model', value)
    def set_input_value(self, value):
        print(value)        
        test.amp.param('input_level', value)
    def set_output_value(self, value):
        print(value)
        test.amp.param('output_level', value)
    def show_file_manager(self):
        self.file_manager.show('/home/jona/Desktop/NAM')
    def close_file_manager(self, *args):
        self.file_manager.close()

class CabScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            search ='files',
            selector = "file",
            ext = [".wav"],
            exit_manager = self.close_file_manager,
            select_path = self.select_patch,
            current_path = '/home/jona/Desktop/IRs'
        )
    def toggle_bypass(self):
        test.cab.toggle()        
    def show_file_manager(self):
        self.file_manager.show('/home/jona/Desktop/IRs')
    def close_file_manager(self, *args):
        self.file_manager.close()
    def select_patch(self, value):
        test.cab.patch('ir', value)
        pass
    def set_output_value(self, value):
        test.cab.param('Gain', value-90)
        pass
        
class ReverbScreen(MDScreen):
    def toggle_bypass(self):
        test.hallReverb.toggle()        
class BaseScreen(MDScreen):
    image_size = StringProperty()


class MainApp(MDApp):
    def init(self, rig):
        self.rig = rig
    def build(self):
        # self.theme_cls.primary_palette = "Silver"
        self.theme_cls.theme_style = "Light"  # "Dark"
        self.root.ids.tabs.switch_tab(text="Amp")
        # self.root.ids.
    # def on_switch_tabs(
    #     self,
    #     bar: MDNavigationBar,
    #     item: MDNavigationItem,
    #     item_icon: str,
    #     item_text: str,
    # ):
        # self.root.ids.screen_manager.current = item_text






MainApp().run()