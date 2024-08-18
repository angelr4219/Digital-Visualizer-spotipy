import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id='8459e30ab26b4e60add49be13e82fade',
            client_secret='df71b47380ff4543875f6d42e0b43b83',
            redirect_uri='YOUR_REDIRECT_URI',
            scope='user-read-playback-state'))
    
    def get_current_track(self):
        return self.sp.current_playback()
