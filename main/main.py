import tkinter as tk
from spotifyintegration import SpotifyClient
from gui import VisualizerGUI
from AudioProcessing import create_live_audio_plot, real_time_audio_analysis

def test_spotify_integration():
    print("Testing Spotify Integration...")
    client = SpotifyClient()
    current_track = client.get_current_playing_track()
    if current_track:
        print(f"Currently playing: {current_track['name']} by {', '.join(current_track['artists'])}")
        audio_features = client.get_audio_features(current_track['id'])
        if audio_features:
            print("Audio Features:", audio_features)
        audio_analysis = client.get_audio_analysis(current_track['id'])
        if audio_analysis:
            print("Audio Analysis available")
    else:
        print("No track currently playing")
    print("Spotify Integration test complete.")

def test_gui():
    print("Testing GUI...")
    root = tk.Tk()
    client = SpotifyClient()
    gui = VisualizerGUI(client)
    root.after(10000, root.quit)  # Close the window after 10 seconds
    gui.run()
    print("GUI test complete.")

def test_audio_processing():
    print("Testing Audio Processing...")
    client = SpotifyClient()
    current_track = client.get_current_playing_track()
    if current_track:
        audio_analysis = client.get_audio_analysis(current_track['id'])
        if audio_analysis:
            real_time_audio_analysis()
    else:
        print("No track currently playing")
    print("Audio Processing test complete.")

def test_live_audio_plot():
    print("Testing Live Audio Plot...")
    root = tk.Tk()
    client = SpotifyClient()
    canvas, anim = create_live_audio_plot(root, client)
    canvas.get_tk_widget().pack()
    root.after(10000, root.quit)  # Close the window after 10 seconds
    root.mainloop()
    print("Live Audio Plot test complete.")

def main():
    while True:
        print("\nSpotify Visualizer Test Menu:")
        print("1. Test Spotify Integration")
        print("2. Test GUI")
        print("3. Test Audio Processing")
        print("4. Test Live Audio Plot")
        print("5. Run Full Application")
        print("0. Exit")
        
        choice = input("Enter your choice (0-5): ")
        
        if choice == '1':
            test_spotify_integration()
        elif choice == '2':
            test_gui()
        elif choice == '3':
            test_audio_processing()
        elif choice == '4':
            test_live_audio_plot()
        elif choice == '5':
            print("Running full application...")
            client = SpotifyClient()
            gui = VisualizerGUI(client)
            gui.run()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()