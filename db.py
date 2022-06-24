import sqlite3

FILE = "book.db"


class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect(FILE)
        except ConnectionError as er:
            print(er)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def get_all_song(self):
        self.cursor.execute(f"select Num, Titre, Compositeur, Auteur, Tonalite, ActiveSong from malagasy")
        return self.cursor.fetchall()

    def get_song_by_filter(self, text):
        try:
            num = int(text)
            self.cursor.execute(
                f"select Num, Titre, Compositeur, Auteur, Tonalite, ActiveSong from malagasy where Num = {num}")
        except:
            self.cursor.execute(
                f"select Num, Titre, Compositeur, Auteur, Tonalite, ActiveSong from malagasy where Titre like '%{text}%'")
        return self.cursor.fetchall()

    def add_to_favorites(self, num, isFavorite):
        self.cursor.execute(f"update malagasy set ActiveSong={0 if isFavorite else 1} where Num={num}")
        self.conn.commit()

    def get_favorites(self):
        self.cursor.execute(
            f"select Num, Titre, Compositeur, Auteur, Tonalite, ActiveSong from malagasy where ActiveSong=1")
        return self.cursor.fetchall()

    def get_favorites_filter(self, text):
        try:
            num = int(text)
            self.cursor.execute(
                f"select Num, Titre, Compositeur, Auteur, Tonalite, ActiveSong from malagasy where Num = {num} and ActiveSong=1")
        except:
            self.cursor.execute(
                f"select Num, Titre, Compositeur, Auteur, Tonalite, ActiveSong from malagasy where Titre like '%{text}%' and ActiveSong")
        return self.cursor.fetchall()

    def get_song(self, num):
        self.cursor.execute(
            f"select Num, Titre, Compositeur, Auteur, Tonalite, ActiveSong, Detail from malagasy where Num={num}")
        return self.cursor.fetchone()
