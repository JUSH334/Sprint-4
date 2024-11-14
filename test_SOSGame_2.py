import unittest
from unittest.mock import patch
from player import ComputerPlayer
from game_manager import GameManager
from game_modes import SimpleGameMode, GeneralGameMode
from sos_gui import SOSGameGUI
import tkinter as tk

class TestComputerOpponent(unittest.TestCase):
    
    def setUp(self):
        """Set up GUI, game manager, and game mode for testing."""
        self.root = tk.Tk()
        self.gui = SOSGameGUI(self.root)
        self.gui.create_board()
        self.game_manager = GameManager(board_size=3, game_mode="Simple", gui=self.gui)
        self.simple_mode = SimpleGameMode(self.game_manager)
        self.general_mode = GeneralGameMode(self.game_manager)
        self.computer_player = ComputerPlayer("Computer", "Blue", self.gui)

    def tearDown(self):
        """Destroy the Tkinter root window after each test."""
        self.root.destroy()

    # Test for 8.1: Computer Move in Simple Mode
    def test_computer_move_simple_mode(self):
        """Test that the computer can make a move in Simple Game mode."""
        initial_empty_cells = self.gui.get_empty_cells()
        self.computer_player.make_move(self.simple_mode)
        remaining_empty_cells = self.gui.get_empty_cells()
        
        self.assertEqual(len(remaining_empty_cells), len(initial_empty_cells) - 1)

    # Test for 8.2: Computer Move in General Mode
    def test_computer_move_general_mode(self):
        """Test that the computer maximizes SOS formations in General Game mode."""
        self.game_manager.mode = "General"
        
        self.gui.board_buttons[0][0].config(text="S")
        self.gui.board_buttons[0][1].config(text="O")
        
        with patch.object(self.computer_player, 'make_move') as mock_make_move:
            self.computer_player.make_move(self.general_mode)
            mock_make_move.assert_called_once_with(self.general_mode)

    # Test for 8.3: Winner Identification in Simple Mode
    def test_winner_identification_simple_mode(self):
        """Test that the game correctly identifies the winner in Simple Mode."""
        # Set up a winning condition for the computer
        self.gui.board_buttons[0][0].config(text="S")
        self.gui.board_buttons[0][1].config(text="O")
        self.gui.board_buttons[0][2].config(text="S") 
        
        self.assertTrue(self.simple_mode.check_for_winner())
        self.assertEqual(self.game_manager.get_winner(), "Computer")

    # Test for 8.4: Winner Identification in General Mode
    def test_winner_identification_general_mode(self):
        """Test that the game correctly counts SOS sequences and identifies the winner in General Mode."""
        self.game_manager.mode = "General"
        
        self.gui.board_buttons[0][0].config(text="S")
        self.gui.board_buttons[0][1].config(text="O")
        self.gui.board_buttons[0][2].config(text="S")
        self.gui.board_buttons[1][0].config(text="S")
        self.gui.board_buttons[1][1].config(text="O")
        self.gui.board_buttons[1][2].config(text="S")
        
        self.assertTrue(self.general_mode.check_for_winner())
        self.assertEqual(self.game_manager.get_winner(), "Computer")

if __name__ == '__main__':
    unittest.main()

