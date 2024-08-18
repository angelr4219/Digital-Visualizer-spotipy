import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt
from spotifyintegration import SpotifyClient


'''
Audio Processing
This files contains functions for processing audio data, including extracting the audio signal, performing a Fast Fourier Transform (FFT), and plotting the spectrum of the audio signal.
The loudness of the audio signal over time is also visualized using the audio analysis data from Spotify.
The plot_spectrum function takes the frequency data and FFT result and plots the spectrum of the audio signal.


'''
# Extract the audio signal from the audio data
client = SpotifyClient()
current_track = client.get_current_playing_track()
audio_analysis = client.get_audio_analysis(current_track['id'])

# Plot the loudness of the audio signal over time
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


# Perform a Fast Fourier Transform (FFT) on the audio signal
def extract_audio_signal(audio_data):
    # Placeholder function to extract audio signal
    return np.array(audio_data)

# Perform a Fast Fourier Transform (FFT) on the audio signal
def perform_fft(signal):
    fft_result = scipy.fftpack.fft(signal)
    freqs = scipy.fftpack.fftfreq(len(signal))
    return freqs, fft_result

def plot_loudness_and_fft(audio_analysis):
    if audio_analysis:
        # Extract loudness data
        times = [section['start'] for section in audio_analysis['sections']]
        loudness = [section['loudness'] for section in audio_analysis['sections']]
        
        # Plot loudness
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        plt.plot(times, loudness, marker='o', linestyle='-', color='b')
        plt.title('Loudness Over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Loudness (dB)')
        plt.grid()
        
        # Extract audio signal for FFT
        # Placeholder: Replace with actual audio signal extraction logic
        audio_signal = extract_audio_signal(loudness)
        
        # Perform FFT
        freqs, fft_result = perform_fft(audio_signal)
        
        # Plot FFT
        plt.subplot(2, 1, 2)
        
        plt.plot(freqs, color='r')
        plt.plot(np.abs(fft_result),color='b')
        plt.title('Fourier Transform')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.grid()
        
        plt.tight_layout()
        plt.show()
    else:
        print("No audio analysis found for the track.")

plot_loudness_and_fft(audio_analysis)