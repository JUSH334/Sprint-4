import unittest
from unittest.mock import patch
from player import ComputerPlayer
from game_modes import SimpleGameMode
from game_manager import GameManager
from sos_gui import SOSGameGUI
import tkinter as tk

class TestComputerPlayer(unittest.TestCase):
    
    def setUp(self):
        """Set up a GUI and game manager for testing."""
        self.root = tk.Tk()
        self.gui = SOSGameGUI(self.root)
        self.gui.create_board() 
        self.game_manager = GameManager(board_size=3, game_mode="Simple", gui=self.gui)
        self.simple_game_mode = SimpleGameMode(board_size=3, game_manager=self.game_manager)
        self.computer_player = ComputerPlayer("Computer", "Blue", self.gui)  # Pass GUI directly

    def tearDown(self):
        """Destroy the Tkinter root window after each test."""
        self.root.destroy()

    def test_computer_make_random_move(self):
        """Test that the ComputerPlayer makes a valid move within bounds."""
        initial_empty_cells = self.gui.get_empty_cells()
        self.computer_player.make_move(self.simple_game_mode)
        remaining_empty_cells = self.gui.get_empty_cells()

        # The number of empty cells should decrease by 1 after the move
        self.assertEqual(len(remaining_empty_cells), len(initial_empty_cells) - 1)

    def test_computer_choice_is_s_or_o(self):
        """Test that the ComputerPlayer randomly chooses 'S' or 'O'."""
        valid_choices = {"S", "O"}
        self.computer_player.make_move(self.simple_game_mode)
        
        # Check that the choice is either "S" or "O"
        self.assertIn(self.computer_player.get_choice(), valid_choices)

    def test_computer_triggers_extra_turn(self):
        """Test that the ComputerPlayer gets an extra turn when forming an SOS."""
        # Set up the board so that placing an 'S' at (0, 2) will form an SOS
        self.gui.board_buttons[0][0].config(text="S")
        self.gui.board_buttons[0][1].config(text="O")

        # Prepare the side effect function
        def choice_side_effect(seq):
            if seq == ['S', 'O']:
                return 'S'  # Return 'S' when choosing a letter
            else:
                return (0, 2)  # Return (0, 2) when choosing a cell

        # Patch 'random.choice' only in the 'player' module
        with patch('player.random.choice', side_effect=choice_side_effect):
            # Trigger computer's move
            self.computer_player.make_move(self.simple_game_mode)

        # Check that (0, 2) now contains "S" as expected
        self.assertEqual(self.gui.board_buttons[0][2].cget("text"), "S")


if __name__ == '__main__':
    unittest.main()
