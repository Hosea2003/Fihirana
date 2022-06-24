from kivy.uix.recycleview import RecycleView
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang.builder import Builder

from db import Database

Builder.load_string("""
<Favorie>:
    orientation:'vertical'
    padding:10
    spacing:10
    id:favorie
    
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
""")


class Favorie(MDBoxLayout):
    def get_song(self, search=False):
        db = Database()
        self.rv:RecycleView = self.ids.rv
        if not search:
            self.rv.data = [
                {"title": str(song[0]) + " " + song[1],
                 "author": song[2] + " " + song[3],
                 "cle": song[4],
                 "id": song[0],
                 "isFavorite": int(song[5]) == 1
                 }
                for song in db.get_favorites()]
        else:
            data = db.get_favorites_filter(self.ids.searchTxt.text)
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
