import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack
from spotifyintegration import SpotifyClient
import time

plt.ion()  # Turn on interactive mode for real-time plotting


# Extract the audio signal from the audio data
client = SpotifyClient()
current_track = client.get_current_playing_track()
spotify_analysis = client.get_audio_analysis(current_track['id'])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

while True:
    
    
    if current_track and spotify_analysis:
        print(f"Now playing: {current_track['name']} by {current_track['artists'][0]['name']}")
        
        audio_data = np.frombuffer(stream.read(CHUNK), dtype=np.float32)
        analysis_result = analyze_audio(audio_data, spotify_analysis)
        
        # Update plots
        ax1.clear()
        ax1.plot(analysis_result['freqs'][:len(analysis_result['freqs'])//2], 
                 analysis_result['fft_result'][:len(analysis_result['fft_result'])//2])
        ax1.set_title('Real-time FFT')
        ax1.set_xlabel('Frequency (Hz)')
        ax1.set_ylabel('Magnitude')
        
        ax2.clear()
        ax2.bar(['Real-time', 'Spotify'], 
                [analysis_result['real_time_loudness'], analysis_result['spotify_loudness']])
        ax2.set_title('Loudness Comparison')
        ax2.set_ylabel('Loudness')
        
        plt.tight_layout()
        plt.draw()
        plt.pause(10)
        
    time.sleep(1)  # Adjust the sleep time based on your needs and API rate limits[2]

# Clean up
stream.stop_stream()
stream.close()
p.terminate()