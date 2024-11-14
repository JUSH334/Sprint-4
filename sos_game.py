import tkinter as tk
from game_manager import GameManager 
from sos_gui import SOSGameGUI         

def main():
    # Initialize the main Tkinter root window
    root = tk.Tk()
    root.title("SOS Game")

    # Set up the GUI
    gui = SOSGameGUI(root)

    # Initialize the GameManager with the GUI reference and other settings
    game_manager = GameManager(board_size=3, game_mode="Simple", gui=gui)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()

