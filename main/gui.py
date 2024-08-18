import tkinter as tk
from spotify_integration import SpotifyClient
from visualizations.py import plot_spectrum

class VisualizerGUI:
    def __init__(self, spotify_client: SpotifyClient):
        self.spotify_client = spotify_client
        self.root = tk.Tk()
        self.root.title("Spotify Visualizer")
        # Set up GUI components
    
    def run(self):
        self.root.mainloop()
