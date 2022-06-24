from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang.builder import Builder
from kivy.uix.recycleview import RecycleView
from kivymd.uix.card import MDCard
from db import Database
from song import SongContent

Builder.load_string("""
<Home>:
    orientation:'vertical'
    padding:10
    spacing:10
    
    TextInput:
        id:searchTxt
        size_hint_y:None
        height:40
        padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
        on_text:root.search_song(searchTxt.text)
        

        
    RecycleView:
        viewclass: 'Song'
        id:rv
        RecycleBoxLayout:
            default_size: None, dp(70)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            spacing:7
            
<Song>:
    elevation:5
    radius:5
    orientation:'horizontal'
    size_hint_y:.1
    padding:10
    ripple_behavior:True
    app:app
    MDCard:
        orientation:'vertical'
        spacing:10
        elevation:0
        radius:0
        md_bg_color:0,0,0,0
        on_release:root.select_song()
        MDLabel:
            text:root.title
            bold:True
            font_size:13
        MDLabel:
            text:root.author
            font_size:13
        MDLabel:
            text:root.cle
            font_size:13
            color:180/255, 191/255, 209/255, 1
            
    MDBoxLayout:
        size_hint_x:None
        width:dp(40)
        orientation:'vertical'
        MDIconButton:
            icon:'heart'
            font_size:'13sp'
            pos_hint:{'center_x':.5}
            on_release:root.add_to_favorites()
            id:favoriteBtn
            theme_text_color:'Custom'
""")


class Home(MDBoxLayout):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)
        self.rv: RecycleView = self.ids.rv
        self.get_song()

    def get_song(self, search=False):
        db = Database()
        if not search:
            self.rv.data = [
                {"title": str(song[0]) + " " + song[1],
                 "author": song[2] + " " + song[3],
                 "cle": song[4],
                 "id": song[0],
                 "isFavorite": int(song[5]) == 1
                 }
                for song in db.get_all_song()]
        else:
            data = db.get_song_by_filter(self.ids.searchTxt.text)
            result = []
            if len(data) == 0:
                result.append(
                    {
                        "title": "Aucun résultat",
                        "author": "",
                        "cle": "",
                        "isFavorite": False,
                        "id": -1
                    }
                )
            else:
                for song in data:
                    result.append(
                        {"title": str(song[0]) + " " + song[1],
                         "author": song[2] + " " + song[3],
                         "cle": song[4],
                         "id": song[0],
                         "isFavorite": int(song[5]) == 1
                         }
                    )
            self.rv.data = result

    def search_song(self, text):
        if text == "":
            self.get_song(search=False)
        else:
            self.get_song(search=True)

    def f(self, sv, touch):
        print(touch.ud['sv.824']['dy'])


class Song(MDCard):
    title = StringProperty()
    cle = StringProperty()
    author = StringProperty()
    isFavorite = BooleanProperty(False)
    id = NumericProperty()

    def select_song(self):
        if self.id>0:
            song_screen:SongContent = self.app.root.ids.songcontent.children[0]
            song_screen.show_song(self.id)
            self.app.root.ids.mainscreen.current="song"

    def add_to_favorites(self):
        db = Database()
        db.add_to_favorites(self.id, self.isFavorite)
        if self.isFavorite:
            self.isFavorite = False
        else:
            self.isFavorite = True

        if self.app.root.ids.screenmanger.current=="favorites":
            self.app.root.ids.favorie.children[0].get_song()

    def on_isFavorite(self, *args, **kwargs):
        if self.isFavorite:
            self.ids.favoriteBtn.text_color = (1, 0, 0, 1)
        else:
            self.ids.favoriteBtn.text_color = (0, 0, 0, 1)
