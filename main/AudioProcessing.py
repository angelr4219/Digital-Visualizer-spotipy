import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt
from spotifyintegration import SpotifyClient
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



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

def real_time_audio_analysis(update_interval=1000):  # update_interval in milliseconds
    client = SpotifyClient()
    
    # Set up the plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Initialize empty data
    times = []
    loudness = []
    
    # Initialize plot lines
    line1, = ax1.plot([], [], 'b-', label='Loudness')
    line2, = ax2.plot([], [], 'r-', label='FFT')
    
    # Set up plot labels and titles
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Loudness (dB)')
    ax1.set_title('Loudness Over Time')
    ax1.grid(True)
    ax1.legend()
    
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Magnitude')
    ax2.set_title('Real-time Fourier Transform')
    ax2.grid(True)
    ax2.legend()
    
    def update_plot(frame):
        nonlocal times, loudness
        
        # Get current playback info
        playback_info = client.get_current_playback_info()
        if not playback_info:
            return line1, line2
        
        # Get audio analysis for the current track
        audio_analysis = client.get_audio_analysis(playback_info['id'])
        if not audio_analysis:
            return line1, line2
        
        # Update loudness data
        current_time = playback_info['progress'] / 1000  # Convert to seconds
        current_loudness = next((segment['loudness_max'] for segment in audio_analysis['segments'] 
                                 if segment['start'] <= current_time < segment['start'] + segment['duration']), 
                                None)
        
        if current_loudness is not None:
            times.append(current_time)
            loudness.append(current_loudness)
            
            # Keep only the last 60 seconds of data
            if len(times) > 60:
                times = times[-60:]
                loudness = loudness[-60:]
            
            line1.set_data(times, loudness)
            ax1.relim()
            ax1.autoscale_view()
            
            # Update track info in title
            ax1.set_title(f"Loudness Over Time - {playback_info['name']} by {', '.join(playback_info['artists'])}")
        
        # Perform FFT on the recent loudness data
        if len(loudness) > 1:
            fft_result = np.fft.fft(loudness)
            fft_freqs = np.fft.fftfreq(len(loudness), d=1)  # Assuming 1 second intervals
            fft_magnitudes = np.abs(fft_result)
            
            # Plot only the positive frequencies
            positive_freq_idxs = fft_freqs > 0
            line2.set_data(fft_freqs[positive_freq_idxs], fft_magnitudes[positive_freq_idxs])
            ax2.relim()
            ax2.autoscale_view()
        
        return line1, line2
    
    # Set up the animation
    anim = FuncAnimation(fig, update_plot, frames=np.arange(0, 100), interval=update_interval, blit=True)
    
    plt.tight_layout()
    plt.show()
    
    
def create_live_audio_plot(master, spotify_client, figsize=(4, 4), dpi=100):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, dpi=dpi)
    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()

    ax1.set_title('Loudness Over Time')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Loudness (dB)')
    ax1.grid(True)

    ax2.set_title('Fourier Transform')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Amplitude')
    ax2.grid(True)

    line1, = ax1.plot([], [], 'b-')
    line2, = ax2.plot([], [], 'r-')

    times = []
    loudness = []

    def animate(frame):
        nonlocal times, loudness
        current_track = spotify_client.get_current_playing_track()
        if not current_track:
            return line1, line2

        audio_analysis = spotify_client.get_audio_analysis(current_track['id'])
        if not audio_analysis:
            return line1, line2

        # Update loudness data
        current_time = current_track['progress'] / 1000  # Convert to seconds
        current_loudness = next((segment['loudness_max'] for segment in audio_analysis['segments'] 
                                 if segment['start'] <= current_time < segment['start'] + segment['duration']), 
                                None)

        if current_loudness is not None:
            times.append(current_time)
            loudness.append(current_loudness)

            # Keep only the last 60 seconds of data
            if len(times) > 60:
                times = times[-60:]
                loudness = loudness[-60:]

            line1.set_data(times, loudness)
            ax1.relim()
            ax1.autoscale_view()

        # Perform FFT
        if len(loudness) > 1:
            fft_result = np.fft.fft(loudness)
            fft_freqs = np.fft.fftfreq(len(loudness), d=1)
            fft_magnitudes = np.abs(fft_result)

            positive_freq_idxs = fft_freqs > 0
            line2.set_data(fft_freqs[positive_freq_idxs], fft_magnitudes[positive_freq_idxs])
            ax2.relim()
            ax2.autoscale_view()

        return line1, line2

    anim = animation.FuncAnimation(fig, animate, frames=None, interval=1000, blit=True)
    return canvas, anim


# Run the real-time analysis
real_time_audio_analysis()
print ("Real Time Audio Analysis")
#create_live_audio_plot()
















'''#Not fully functional code

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

#plot_loudness(audio_analysis, original_sample_rate, target_sample_rate)

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
#plotfft(audio_analysis)
# '''
