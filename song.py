from kivy.properties import BooleanProperty, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang.builder import Builder
from kivy.uix.button import Button

from db import Database

Builder.load_string("""
#:import Clipboard kivy.core.clipboard.Clipboard
#:import toast kivymd.toast.toast
<SongContent>:
    app:app
    orientation:'vertical'
    MDBoxLayout:
        orientation:'horizontal'
        size_hint_y:None
        height:dp(50)
        md_bg_color:245/255, 133/255, 76/255,1
        padding:0,0,10,0
        
        MDIconButton:
            icon:'arrow-left'
            theme_text_color:'Custom'
            text_color:1,1,1,1
            on_release:app.root.ids.mainscreen.current='content'
            pos_hint:{'center_y':.5}
        MDLabel:
            id:title
            color:1,1,1,1
            size_hint_x:1
            
        MDIconButton:
            icon:'heart' if root.isFavorite else 'heart-outline'
            theme_text_color:'Custom'
            text_color:1,1,1,1
            on_release:root.add_to_favorite()
            pos_hint:{'center_y':.5}
            
        MDIconButton:
            icon:'content-copy'
            theme_text_color:'Custom'
            text_color:1,1,1,1
            user_font_size:18
            pos_hint:{'center_y':.5}
            on_release:
                Clipboard.copy(strof.text)
                toast('Voadika')
    MDFloatLayout:
        ScrollView:
            do_scroll_y:True
            do_scroll_x:False
            pos_hint:{'x':0, 'y':0}
            size_hint:1,1
            MDBoxLayout:
                padding:20
                orientation:'vertical'
                spacing:30
                size_hint_y:None
                height:self.minimum_height
                id:box
                
                MDBoxLayout:
                    orientation:'horizontal'
                    size_hint:1, None
                    height:60
                    Widget:
                    MDBoxLayout:
                        orientation:'vertical'
                        adaptive_width:True
                        MDLabel:
                            id:num
                            halign:'right'
                            color:132/255, 138/255, 148/255,1
                            font_size:14
                        MDLabel:
                            id:cle
                            halign:'right'
                            color:132/255, 138/255, 148/255,1
                            font_size:14
                            
                MDLabel:
                    id:strof
                    color:0,0,0,1
                    adaptive_height:True
                    font_size:14
                    
                MDBoxLayout:
                    orientation:'vertical'
                    size_hint_y:None
                    height:40
                    
                
                    MDLabel:
                        id:compositeur
                        color:132/255, 138/255, 148/255,1
                        font_size:14
                        halign:'right'
                        
                    MDLabel:
                        id:author
                        color:132/255, 138/255, 148/255,1
                        font_size:14
                        halign:'right'
                
        MDBoxLayout:
            orientation:'vertical'
            pos_hint:{'center_x':.9, 'center_y':.15}
            spacing:7
            size_hint:None, None
            adaptive_height:True
            width:40
            
            MDCard:
                size_hint:None, None
                size:40,40
                radius:7
                ripple_behavior:True
                on_release:strof.font_size+=1
                Label:
                    text:'A+'
                    color:0,0,0,1
                    
            MDCard:
                size_hint:None, None
                size:40,40
                radius:7
                ripple_behavior:True
                on_release:strof.font_size-=1
                Label:
                    text:'A-'
                    color:0,0,0,1
        
""")


class SongContent(MDBoxLayout):
    isFavorite = BooleanProperty(False)
    id = NumericProperty()

    def return_screen(self):
        self.parent.parent.current = 'content'

    def show_song(self, num):
        self.db = Database()
        song = self.db.get_song(num)
        self.ids.strof.text = song[6]
        self.ids.num.text = f'Laharana: {num}'
        self.id = int(num)
        self.ids.cle.text = f'Clé: {song[4]}'
        self.ids.author.text = f'Mpanoratra:{song[3]}'
        self.ids.compositeur.text = f'Feo:{song[2]}'
        self.ids.title.text = song[1]
        self.isFavorite = int(song[5]) == 1

    def add_to_favorite(self):
        self.db.add_to_favorites(self.id, self.isFavorite)
        if self.isFavorite:
            self.isFavorite = False
        else:
            self.isFavorite = True

        self.app.root.ids.favorie.children[0].get_song()
        self.app.root.ids.home.children[0].get_song()
