import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id='8459e30ab26b4e60add49be13e82fade',
            client_secret='df71b47380ff4543875f6d42e0b43b83',
            redirect_uri='http://127.0.0.1:5500',
            scope='user-read-playback-state')) 
    def get_current_playing_track(self):
        current_playback = self.sp.current_playback()
        if current_playback and current_playback['is_playing']:
            track = current_playback['item']
            track_info = {
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']],
                'album': track['album']['name'],
                'album_art': track['album']['images'][0]['url']
            }
            return track_info
        return None

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
        print(f"Album Art: {current_track['album_art']}")
    else:
        print("No track is currently playing.")


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
    
 