# Description: This file contains the GUI for the Spotify Visualizer. It displays the track information and album art for the currently playing track.
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser
from spotifyintegration import SpotifyClient
from AudioProcessing import create_live_audio_plot
import numpy as np

# Initialize Spotify client
client = SpotifyClient()
album_art_url = client.get_album_art()

class VisualizerGUI:
    def __init__(self, spotify_client: SpotifyClient):
        self.spotify_client = spotify_client
        self.current_album_art_url = None

        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Spotify Visualizer")
        self.root.geometry("800x900")  # Increased height for graphs
        self.root.configure(bg="#1db954")  # Spotify green

        # Label to display track information
        self.track_info_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#1DB954", fg="#191414", justify=tk.LEFT)
        self.track_info_label.pack(pady=20)

        # Label to display album art
        self.album_art_label = tk.Label(self.root)
        self.album_art_label.pack(pady=10)

        # Button to start/stop live audio analysis
        self.analysis_button = tk.Button(self.root, text="Start Live Analysis", command=self.toggle_analysis)
        self.analysis_button.pack(pady=10)

        # Frame to hold the live audio analysis plot
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(pady=20, expand=True, fill='both')

        # Initialize display
        self.display_track_info()
        self.update_track_info_periodically()
        self.update_album_art()

        self.analysis_running = False
        self.plot_canvas = None
        self.plot_animation = None

    def toggle_analysis(self):
        if self.analysis_running:
            self.stop_analysis()
        else:
            self.start_analysis()

    def start_analysis(self):
        if not self.analysis_running:
            # Pass the correct arguments to create_live_audio_plot
            self.plot_canvas, self.plot_animation = create_live_audio_plot(self.plot_frame, self.spotify_client, figsize=(4, 4), dpi=100)
            self.plot_canvas.get_tk_widget().pack(fill='both', expand=True)
            self.analysis_running = True
            self.analysis_button.config(text="Stop Live Analysis")

    def stop_analysis(self):
        if self.analysis_running:
            self.plot_animation.event_source.stop()
            self.plot_canvas.get_tk_widget().pack_forget()
            self.analysis_running = False
            self.analysis_button.config(text="Start Live Analysis")

    def run(self):
        self.root.mainloop()

    def on_button_click(self):
        self.display_track_info()
        print("Button was clicked!")

    def exit_app(self):
        self.root.quit()

    def display_track_info(self):
        current_track = self.spotify_client.get_current_playing_track()
        
        if current_track:
            track_name = current_track.get('name', 'Unknown')
            artists = ', '.join(current_track.get('artists', ['Unknown']))
            album = current_track.get('album', 'Unknown')
            album_art_url = current_track.get('album_art')

            self.track_info_label.config(text=f"Currently playing: {track_name} by {artists}\nAlbum: {album}")
            self.display_album_art(album_art_url)
        else:
            self.track_info_label.config(text="No track is currently playing.")
            self.album_art_label.config(image='')

    def display_album_art(self, url):
        if not url:
            print("No URL provided for album art.")
            self.album_art_label.config(image='')
            return
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            img_data = response.content
            img = Image.open(BytesIO(img_data))

            # Resize the image to fit the GUI
            img = img.resize((200, 200), Image.Resampling.LANCZOS)

            # Convert the image to a format Tkinter can use
            album_art_img = ImageTk.PhotoImage(img)

            # Update the album art label with the new image
            self.album_art_label.config(image=album_art_img)
            self.album_art_label.image = album_art_img  # Keep a reference to avoid garbage collection
        except requests.RequestException as e:
            print(f"Error loading album art: {e}")
            self.album_art_label.config(image='')
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.album_art_label.config(image='')

    def open_album_art_url(self):
        if self.current_album_art_url:
            webbrowser.open(self.current_album_art_url)
        else:
            print("No album art URL available.")

    def update_album_art(self):
        self.current_album_art_url = self.spotify_client.get_current_playing_track().get('album_art', None)
        self.display_album_art(self.current_album_art_url)
        self.root.after(5000, self.update_album_art)  # Refresh every 5 seconds

    def update_track_info_periodically(self):
        self.display_track_info()  # Update track info
        self.root.after(5000, self.update_track_info_periodically)  # Refresh every 5 seconds


gui = VisualizerGUI(client)
gui.run()
print("Hello World")

