import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt
#access to the Spotify API
#is able to get the current playing track
class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id='8459e30ab26b4e60add49be13e82fade',
            client_secret='df71b47380ff4543875f6d42e0b43b83',
            redirect_uri='http://127.0.0.1:5500',
            scope='user-read-playback-state')) 
    #get what is going on in the user's spotify account
    def get_current_playing_track(self):
        current_playback = self.sp.current_playback()
        if current_playback and current_playback['is_playing']:
            track = current_playback['item']
            track_info = {
                'id': track['id'],
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']],
                'album': track['album']['name'],
                'album_art': track['album']['images'][0]['url']
            }
            return track_info
        return None
    
    #get the audio features of the track
    def get_audio_features(self, track_id):
        audio_features = self.sp.audio_features(track_id)
        return audio_features[0] if audio_features else None
    #get the audio analysis of the track
    def get_audio_analysis(self, track_id):
        audio_analysis = self.sp.audio_analysis(track_id)
        return audio_analysis


if __name__ == "__main__":
    client_id='8459e30ab26b4e60add49be13e82fade'
    client_secret='df71b47380ff4543875f6d42e0b43b83'
    redirect_uri='http://127.0.0.1:5500'
    scope='user-read-playback-state'

    client = SpotifyClient()
    current_track = client.get_current_playing_track()
    
    if current_track:
        print(f"Currently playing: {current_track['name']} by {', '.join(current_track['artists'])}")
        print(f"Album: {current_track['album']}")
        print(f"ID: {current_track['id']}")
        print(f"Album Art: {current_track['album_art']}")
    else:
        print("No track is currently playing.")
   
    audio_features = client.get_audio_features(current_track['id'])
    if audio_features:
        print("Audio Features:")
        print(audio_features)
    else:
        print("No audio features found.")
    
    audio_analysis = client.get_audio_analysis(current_track['id'])
def plot_loudness(AA):
    if audio_analysis:
        print("Audio Analysis:")
        times = [segment['start'] for segment in audio_analysis['segments']]
        loudness = [segment['loudness_max'] for segment in audio_analysis['segments']]
        plt.figure(figsize=(12, 6))
        plt.plot(times, loudness, label='Loudness')
        title  = current_track['name'] 
        plt.title(title )
        #plt.title('Loudness Over Time' )
        plt.xlabel('Time (s)')
        plt.ylabel('Loudness (dB)')
        plt.grid()
        plt.show()
    else:
        print("No audio analysis found.")
plot_loudness(audio_analysis)
   
  
  
  
  
  
  
  #new class to get the saved tracks of the user2
'''
class SpotifyLibrary:
    def __init__(self):
        self.sp = self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
            client_id='8459e30ab26b4e60add49be13e82fade',
            client_secret='df71b47380ff4543875f6d42e0b43b83',
            redirect_uri='http://127.0.0.1:5500',scope="user-library-read"))
        self.results = self.sp.current_user_saved_tracks()
    
    def print_saved_tracks(self):
        for idx, item in enumerate(self.results['items']):
            track = item['track']
            print(idx, track['artists'][0]['name'], " – ", track['name'])

# Create an instance of the SpotifyLibrary class
#spotify_library = SpotifyLibrary()

# Print saved tracks
#spotify_library.print_saved_tracks()
    '''
  