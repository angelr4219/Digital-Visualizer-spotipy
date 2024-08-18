import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scipy.fftpack
from spotifyintegration import SpotifyClient

"""_summary_

   What i need to do is take a song and create an fft in live time as the song plays, Here is a implementation for recording audio that works. 
   To DO:
   I need to basically sample audio from a song, and them perform a fft on that audio. 
"""





# Parameters
CHUNK = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Number of audio channels
RATE = 44100  # Sampling rate (samples per second)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream for playback and recording
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

#Initialize Spotify client
client_id='8459e30ab26b4e60add49be13e82fade'
client_secret='df71b47380ff4543875f6d42e0b43b83'
redirect_uri='http://127.0.0.1:5500'
scope='user-read-playback-state'
client = SpotifyClient()

# Get current playing track
current_track = client.get_current_playing_track()

c = pyaudio.PyAudio()
s = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

# Placeholder function for audio signal extraction from Spotify
def extract_audio_signal(audio_data):
     # Convert the byte buffer to a NumPy array based on audio format
    if format == pyaudio.paInt16:
        # Assuming the audio data is in 16-bit PCM format
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
    elif format == pyaudio.paFloat32:
        # Assuming the audio data is in 32-bit float PCM format
        audio_array = np.frombuffer(audio_data, dtype=np.float32)
    else:
        raise ValueError("Unsupported audio format")
    return audio_array

def perform_fft(signal):
    fft_result = scipy.fftpack.fft(signal)
    freqs = scipy.fftpack.fftfreq(len(signal), 1.0 / RATE)
    return freqs[:len(freqs) // 2], fft_result[:len(fft_result) // 2]



# Set up the plot
fig, ax = plt.subplots()
xdata, ydata = [], []
line, = ax.plot([], [], lw=2)

def init():
    ax.set_xlim(0, RATE / 2)
    ax.set_ylim(0, 1000)
    return line,

def update(frame):
    # Read audio data from the stream
    audio_data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    
    # Play the same audio data (placeholder for actual audio streaming from Spotify)
    stream.write(audio_data.tobytes())
    
    # Apply FFT
    freqs, fft_result = perform_fft(audio_data)
    
    # Update the plot
    line.set_data(freqs, np.abs(fft_result))
    return line,

# Animate the plot
ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=50)

plt.show()

# Clean up
stream.stop_stream()
stream.close()
p.terminate()