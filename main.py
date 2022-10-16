from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.menu import MDDropdownMenu



import spotipy 
import spotipy.util as util 
import os 
import pandas as pd
import requests




from Tools.CreatePlaylist import create_playlist
from Tools.getPlaylistInfo_features import get_features_for_playlist, get_playlist_info
from Tools.getSong_genres import get_song_genres
from Tools.Query import spotify_recommend
from Tools.RecommendSongs import recommend_songs





class  rootScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    

    def runApp(self):
        username = os.environ.get('SPOTIFY_USERNAME')
        Id = os.environ.get('SPOTIFY_CLIENT_ID')
        secret = os.environ.get('SPOTIFY_CLIENT_SECRET')  
        redirect_uri = 'https://unheard-login.com/callback/'
        token = util.prompt_for_user_token(username=username,
                                        scope='playlist-modify-private', 
                                        client_id=Id, 
                                        client_secret=secret, 
                                        redirect_uri=redirect_uri)
        sp = spotipy.Spotify(auth=token)


        playlist_uri = self.manager.get_screen('main').ids.playlist_uri.text

        df = pd.DataFrame(columns=['name', 'artist', 'track_URI', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'playlist'])
        df = get_features_for_playlist(df, username, playlist_uri, sp)


        uri_songs = df['track_URI'].tolist()
        uri=[]
        for i in range(len(uri_songs)):
            uri_split = uri_songs[i].split(':')[2]
            uri.append(uri_split)
        
        result = recommend_songs(num_songs=int(self.manager.get_screen('main').ids.num_songs.text), 
               token=token, uri=uri, df=df)

        create_playlist(result, sp,username=username, playlistName=self.manager.get_screen('main').ids.playlist_name.text)
        return popFun()

class P(FloatLayout):
    pass

class PopWindow(Widget):
    def btn(self):
        popFun()

def popFun():
    show = P()
    window = Popup(title = "popup", content = show,
                   size_hint = (None, None), size = (300, 300))
    window.open()
    
class MainApp(MDApp):
    def build(self):
        self.screen = Builder.load_file('rootScreen2.kv')
        sm = ScreenManager()
        sm.add_widget(rootScreen(name='main'))
        return sm


if __name__ == "__main__":
    MainApp().run()