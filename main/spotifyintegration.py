import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt
import requests
from io import BytesIO
from PIL import Image, ImageTk


'''
Spotify Integration
This files contains the SpotifyClient class which is used to interact with the Spotify API. The SpotifyClient class has the following methods:'
get_current_playing_track: Get the currently playing track
get_audio_features: Get the audio features of a track
get_audio_analysis: Get the audio analysis of a track
The main function demonstrates how to use the SpotifyClient class to get the currently playing track, audio features, and audio analysis of a track.

The SpotifyClient class uses the Spotipy library to interact with the Spotify API. The Spotipy library provides a simple interface for the Spotify Web API.

The SpotifyClient class uses the SpotifyOAuth authentication flow to authenticate with the Spotify API. This flow allows the user to grant permission to the application to access their Spotify account.

The SpotifyClient class is designed to be used in conjunction with the VisualizerGUI class in the gui.py file to create a Spotify visualizer application.

The SpotifyClient class can be used to get information about the currently playing track, such as the track name, artists, album, and album art.

The SpotifyClient class can also be used to get the audio features of a track, such as tempo, key, time signature, and more.

The SpotifyClient class can be used to get the audio analysis of a track, which provides detailed information about the audio content of the track, such as loudness, pitch, and timbre.

The SpotifyClient class is designed to be used in conjunction with the VisualizerGUI class in the gui.py file to create a Spotify visualizer application.

The SpotifyClient class uses the Spotipy library to interact with the Spotify API. The Spotipy library provides a simple interface for the Spotify Web API.

'''


class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id='8459e30ab26b4e60add49be13e82fade',
            client_secret='df71b47380ff4543875f6d42e0b43b83',
            redirect_uri='http://127.0.0.1:5500',
            scope='user-read-playback-state user-read-recently-played')) 
       
    
    #get the current playing track. If no track is playing, get the last played track
    def get_current_playing_track(self):
        current_playback = self.sp.current_playback()
        if current_playback and current_playback['is_playing']:
            track = current_playback['item']
            print("Currently playing track:")
            print(self._format_track_info(track, is_playing=True))
            return self._format_track_info(track, is_playing=True)
        else:
            print("No track is currently playing. Fetching last played tracks...")
            print(self.get_last_played())
            return self.get_last_played()   
    
    #get the audio features of the track
    def get_audio_features(self, track_id):
        audio_features = self.sp.audio_features(track_id)
        return audio_features[0] if audio_features else None
    #get the audio analysis of the track
    def get_audio_analysis(self, track_id):
        audio_analysis = self.sp.audio_analysis(track_id)
        return audio_analysis
    def get_saved_tracks(self):
        results = self.sp.current_user_saved_tracks()
        return results
    def get_album_art(self):
        track_info = self.get_current_playing_track()
        if track_info:
            return track_info.get('album_art', None)
        return None
    def get_last_played(self):
        
        # Get the last 2 played tracks
        
        recent_tracks = self.sp.current_user_recently_played(limit=1)
        
        last_played_tracks = []
        
        for item in recent_tracks['items']:
            track = item['track']
            track_info = {
                'id': track['id'],
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']],
                'album': track['album']['name'],
                'album_art': track['album']['images'][0]['url'] if track['album']['images'] else None
            }
            last_played_tracks.append(track_info)

        return last_played_tracks if last_played_tracks else None
    
    def _format_track_info(self, track, is_playing):
        return {
            'id': track['id'],
            'name': track['name'],
            'artists': [artist['name'] for artist in track['artists']],
            'album': track['album']['name'],
            'album_art': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'is_playing': is_playing
        }
    def recent_tracks(self, limit=50):
        # Fetch the most recently played tracks with a limit of 50
        recent_tracks = self.sp.current_user_recently_played(limit=2)
        track_list = []

        for item in recent_tracks['items']:
            track = item['track']
            track_info = {
                
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']],
                'album': track['album']['name'],
                'album_art': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'played_at': item['played_at']
            }
            track_list.append(track_info)
        return track_list
    
    def get_current_playback_info(self):
        current_playback = self.sp.current_playback()
        if current_playback and current_playback['is_playing']:
            track = current_playback['item']
            progress_ms = current_playback['progress_ms']
            duration_ms = track['duration_ms']
            
            return {
                'id': track['id'],
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']],
                'album': track['album']['name'],
                'album_art': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'is_playing': True,
                'progress': progress_ms,
                'progress': progress_ms,
                'duration': duration_ms,
                'progress_formatted': f"{progress_ms // 60000}:{(progress_ms % 60000) // 1000:02d}",
                'duration_formatted': f"{duration_ms // 60000}:{(duration_ms % 60000) // 1000:02d}",
                'progress_percent': (progress_ms / duration_ms) * 100
            }
        else:
            return None

    def get_audio_analysis(self, track_id):
        return self.sp.audio_analysis(track_id)

    
    
print("Spotify Integration")
client = SpotifyClient()

current_track = client.get_current_playing_track()


client_id='8459e30ab26b4e60add49be13e82fade'
client_secret='df71b47380ff4543875f6d42e0b43b83'
redirect_uri='http://127.0.0.1:5500'
scope='user-read-playback-state'

last_played = client.get_last_played()
now = client.get_current_playback_info()
print (now)


    
        
'''
    audio_features = client.get_audio_features(current_track['id'])
    if audio_features:
        print("Audio Features:")
        print(audio_features)
    else:
        print("No audio features found.")
    
    audio_analysis = client.get_audio_analysis(current_track['id'])
    
'''
    

  