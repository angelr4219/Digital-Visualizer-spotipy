import numpy as np
import scipy.fftpack

from spotifyintegration import SpotifyClient
from spotifyintegration import plot_loudness



client = SpotifyClient()
current_track = client.get_current_playing_track()\
    
print(f"Currently playing: {current_track['name']} by {', '.join(current_track['artists'])}")
print(f"Album: {current_track['album']}")
print(f"ID: {current_track['id']}")
print(f"Album Art: {current_track['album_art']}")
    
    
audio_analysis = client.get_audio_analysis(current_track['id'])


plot_loudness(audio_analysis)

def extract_audio_signal(audio_data):
    # Placeholder function to extract audio signal
    return np.array(audio_data)

def perform_fft(signal):
    fft_result = scipy.fftpack.fft(signal)
    freqs = scipy.fftpack.fftfreq(len(signal))
    return freqs, fft_result
