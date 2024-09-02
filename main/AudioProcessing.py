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
        plt.plot(np.abs(fft_result),
color='b')
        plt.title('Fourier Transform')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.grid()
        
        plt.tight_layout()
        plt.show()
    else:
        print("No audio analysis found for the track.")























#Not fully functional code

def plot_loudness(AA, sample_rate, target_rate):
    """
    Plot the loudness over time, with sampling applied.

    Parameters:
    AA : audio_analysis (dict): Dictionary containing audio analysis data.
    sample_rate (int): Original sample rate of the audio analysis data.
    target_rate (int): Target sample rate for sampling.
    """
    if audio_analysis:
        # Extract times and loudness values
        times = [segment['start'] for segment in audio_analysis['segments']]
        loudness = [segment['loudness_max'] for segment in audio_analysis['segments']]

        # Convert lists to numpy arrays for processing
        times = np.array(times)
        loudness = np.array(loudness)

        # Perform sampling
        sampled_times = sample_audio_signal(times, sample_rate, target_rate)
        sampled_loudness = sample_audio_signal(loudness, sample_rate, target_rate)

        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(sampled_times, sampled_loudness, label='Loudness (Sampled)')
        plt.title('Loudness Over Time (Sampled)')
        plt.xlabel('Time (s)')
        plt.ylabel('Loudness (dB)')
        plt.grid()
        plt.legend()
        plt.show()
    else:
        print("No audio analysis found.")


def sample_audio_signal(signal, original_rate, target_rate):
    """
    Sample the audio signal to a target sample rate.

    Parameters:
    signal (numpy.array): The audio signal to sample.
    original_rate (int): The original sample rate of the audio signal.
    target_rate (int): The target sample rate to downsample or upsample.

    Returns:
    numpy.array: The resampled audio signal.
    """
    if original_rate == target_rate:
        return signal

    # Calculate the resampling factor
    factor = target_rate / original_rate

    # Use numpy's array slicing for downsampling or upsampling
    indices = np.arange(0, len(signal), factor)
    indices = np.round(indices).astype(int)
    indices = indices[indices < len(signal)]

    return signal[indices]

# Assuming original sample rate and target rate for demonstration
original_sample_rate = 1  # 1 sample per second for the example
target_sample_rate = 1  # Example target rate (adjust as needed)

plot_loudness(audio_analysis, original_sample_rate, target_sample_rate)

def plotfft(audio_analysis):
    if audio_analysis:
        # Extract loudness data
        times = [section['start'] for section in audio_analysis['sections']]
        loudness = [section['loudness'] for section in audio_analysis['sections']]
        
        
        # Extract audio signal for FFT
        # Placeholder: Replace with actual audio signal extraction logic
        audio_signal =sample_audio_signal(loudness)
        
        # Perform FFT
        freqs, fft_result = perform_fft(audio_signal)
        
        # Plot FFT
        plt.subplot(2, 1, 2)
        
        plt.plot(freqs, color='r')
        plt.plot(np.abs(fft_result),
color='b')
        plt.title('Fourier Transform')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.grid()
        
        plt.tight_layout()
        plt.show()
    else:
        print("No audio analysis found for the track.")
plotfft(audio_analysis)