import tkinter as tk
from spotifyintegration import SpotifyClient
#from AudioProcessing import plot_loudness



# Initialize Spotify client
client = SpotifyClient()

class VisualizerGUI:

    def __init__(self, spotify_client: SpotifyClient):
        self.spotify_client = spotify_client
        self.root = tk.Tk()
        self.root.title("Spotify Visualizer")
        
        # Set up GUI components
        self.root.geometry("400x300")  # Width x Height
        label = tk.Label(self.root, text="Hello, Tkinter!")
        label.pack()  # This will place the widget in the window
        
        button = tk.Button(self.root, text="Click Me", command=self.on_button_click)
        button.pack()
        
        self.track_info_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#1DB954", fg="white", justify=tk.LEFT)
        self.root.configure(bg="#1DB954")  # Spotify green
        
        self.display_track_info()  # Display track info on startup
        self.update_track_info_periodically()  # Set up periodic updates
        
    #Run the GUI
    def run(self):
        self.root.mainloop()
        
    #Button  
    def on_button_click(self):
        self.display_track_info()
        
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

            # Load album art
            #response = requests.get(album_art_url)
            #img_data = response.content
            #img = Image.open(BytesIO(img_data))
            #img = img.resize((150, 150), Image.ANTIALIAS)
            #album_art_img = ImageTk.PhotoImage(img)

            #self.album_art_label.config(image=album_art_img)
            #self.album_art_label.image = album_art_img  # Keep a reference to avoid garbage collection
            
        else:
            self.track_info_label.config(text="No track is currently playing.")
            #self.album_art_label.config(image='')
        
    # Update track info periodically
    def update_track_info_periodically(self):
        self.display_track_info()  # Update track info
        self.root.after(5000, self.update_track_info_periodically)  # Refresh every 5 seconds



gui = VisualizerGUI(client)
gui.run()
print("Hello World")

