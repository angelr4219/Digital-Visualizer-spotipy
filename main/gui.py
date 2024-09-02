import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser
from spotifyintegration import SpotifyClient
#from AudioProcessing import plot_loudness



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
        self.root.geometry("600x500")  # Increased height for the image
        self.root.configure(bg="#1DB954")  # Spotify green
        
        # Label to display track information
        self.track_info_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#1DB954", fg="white", justify=tk.LEFT)
        self.track_info_label.pack(pady=20)
        
        # Label to display album art
        self.album_art_label = tk.Label(self.root)
        self.album_art_label.pack(pady=10)
        
        # Button to open album art URL
        #self.open_album_art_url = tk.Button(self.root, text="Open Album Art URL", command=self.open_album_art_url)
        #self.open_album_art_url.pack(pady=10)
        
        # Initialize display
        self.display_track_info()  # Display track info on startup
        self.update_track_info_periodically()  # Set up periodic updates
        self.update_album_art()  # Initialize album art update
    
    #Run the GUI
    def run(self):
        self.root.mainloop()
        
    #Button  
    def on_button_click(self):
        self.display_track_info()
        print("Button was clicked!")
        
    # Exit Button
    def exit_app(self):
        self.root.quit()
    
        
    # Display the track information
    def display_track_info(self):
        current_track = client.get_current_playing_track()
        
        if current_track:
            track_name = current_track.get('name', 'Unknown')
            artists = ', '.join(current_track.get('artists', ['Unknown']))
            album = current_track.get('album', 'Unknown')
            album_art_url = current_track.get('album_art')

            self.track_info_label.config(text=f"Currently playing: {track_name} by {artists}\nAlbum: {album}")
            print(  f"Currently playing: {track_name} by {artists}\nAlbum: {album}")
            self.display_album_art(self.current_album_art_url)
            
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
            
    


    # Open the album art URL in the default web browser
    def open_album_art_url(self):
        if self.current_album_art_url:
            webbrowser.open(self.current_album_art_url)
        else:
            print("No album art URL available.")
    # Update Album Art
    def update_album_art(self):
        self.current_album_art_url = self.spotify_client.get_current_playing_track().get('album_art', None)
        self.display_album_art(self.current_album_art_url)
        self.root.after(5000, self.update_album_art)  # Refresh every 5 seconds
        
    # Update track info periodically
    def update_track_info_periodically(self):
        self.display_track_info()  # Update track info
        self.root.after(5000, self.update_track_info_periodically)  # Refresh every 5 seconds
        


gui = VisualizerGUI(client)
gui.run()
print("Hello World")

