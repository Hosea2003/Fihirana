from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivy.lang.builder import Builder

from db import Database
from favorie import Favorie
from home import Home
from song import SongContent

from kivymd.uix.floatlayout import MDFloatLayout

Builder.load_string("""
<MainWidget>:
    orientation:'vertical'
    
    ScreenManager:
        id:mainscreen
        MDScreen:
            name:"content"
            MDBoxLayout:
                orientation:'vertical'
                ScreenManager:
                    id:screenmanger
                    MDScreen:
                        name:'home'
                        id:home
                    MDScreen:
                        name:'favorites'
                        id:favorie
                        on_enter:favorie.children[0].get_song()
                    MDScreen:
                        name:'programs'
                        MDLabel:
                            text:'programs'
                    MDScreen:
                        name:'about'
                        MDLabel:
                            text:'about'
                            
                NavBar:
                    size_hint:.9, None
                    height:60
                    elevation:10
                    radius:[16]
                    id:navbar
                    pos_hint:{'center_x':.5}
                    
                    MDGridLayout:
                        padding:5
                        cols:4
                        id:navgrid
                        
                        NavBarItem:
                            icon:'home'
                            screen:'home'
                        NavBarItem:
                            icon:'heart'
                            screen:'favorites'
                        NavBarItem:
                            icon:'list'
                            screen:'programs'
                        NavBarItem:
                            icon:'home'
                            screen:'about'
                        
        MDScreen:
            name:'song'
            id:songcontent
            
<NavBarItem>:
    size_hint_x:1
    MDIconButton:
        id:iconbtn
        icon:root.icon
        pos_hint:{'center_x':.5, 'center_y':.5}
        theme_text_color:'Custom'
        on_release:
            app.switch_screen(self)
            root.switch_screen(self)
""")


class NavBar(MDCard):
    current = StringProperty('')

    def __init__(self, **kwargs):
        super(NavBar, self).__init__(**kwargs)

    def on_current(self, *args, **kwargs):
        for item in self.children[0].children:
            _ = item.ids.iconbtn
            if item.screen == self.current:
                _.text_color = (1, 0, 0, 1)
            else:
                _.text_color = (0, 0, 0, 1)


class NavBarItem(MDFloatLayout):
    icon = StringProperty()
    screen = StringProperty()

    def switch_screen(self, instance):
        pass


class MainWidget(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.home.add_widget(Home())
        self.ids.favorie.add_widget(Favorie())
        self.ids.songcontent.add_widget(SongContent())


class Application(MDApp):
    def __init__(self, **kwargs):
        super(Application, self).__init__(**kwargs)
        Window.size = (400, 700)

    def on_start(self):
        self.root.ids.navbar.current='home'
        self.root.ids.mainscreen.current = 'content'

    def build(self):
        return MainWidget()

    def switch_screen(self, instance):
        navbar = self.root.ids.navbar
        screen = instance.parent.screen
        navbar.current = screen
        self.root.ids.screenmanger.current = navbar.current


if __name__ == "__main__":
    Application().run()
