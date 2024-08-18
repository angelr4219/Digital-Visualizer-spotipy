from spotify_integration import SpotifyClient
from gui import VisualizerGUI

def main():
    spotify_client = SpotifyClient()
    gui = VisualizerGUI(spotify_client)
    gui.run()

if __name__ == "__main__":
    main()
