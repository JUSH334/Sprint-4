import unittest
from unittest.mock import patch
from player import ComputerPlayer
from game_manager import GameManager
from sos_gui import SOSGameGUI
import tkinter as tk

class TestSOSGame(unittest.TestCase):
    
    def setUp(self):
        """Initialize GUI and game manager for testing."""
        self.root = tk.Tk()
        self.gui = SOSGameGUI(self.root)
        self.gui.create_board()
        self.game_manager = GameManager(board_size=3, game_mode="Simple", gui=self.gui)

    def tearDown(self):
        """Destroy the Tkinter root window after each test."""
        self.root.destroy()

    # User Story 1: Choose a board size
    def test_valid_board_size_selection(self):
        """Test setting a valid board size."""
        self.gui.board_size_var.set(10)
        self.assertEqual(self.gui.board_size_var.get(), 10)

    def test_invalid_board_size(self):
        """Test setting an invalid board size outside the allowed range."""
        self.gui.board_size_var.set(25)
        is_valid = self.gui.validate_board_size(self.gui.board_size_var.get())
        self.assertFalse(is_valid)

    # User Story 2: Choose the game mode of a chosen board
    def test_game_mode_selection(self):
        """Test selecting the game mode."""
        self.gui.radio_var.set("General Game")
        self.assertEqual(self.gui.radio_var.get(), "General Game")

    # User Story 3: Start a new game of the chosen board size and game mode
    def test_start_game(self):
        """Test starting a game with specified settings."""
        self.gui.board_size_var.set(5)
        self.gui.radio_var.set("Simple Game")
        self.gui.start_game()
        self.assertTrue(self.gui.is_game_active)
        self.assertEqual(self.gui.board_size, 5)
        self.assertEqual(self.gui.game_manager.mode, "Simple")

    # User Story 4: Make a move in a simple game
    def test_valid_simple_move(self):
        """Test making a valid move in Simple Game mode."""
        self.gui.on_board_click(0, 0)
        self.assertEqual(self.gui.board_buttons[0][0].cget("text"), "S")  
    
    def test_invalid_simple_move(self):
        """Test making an invalid move in an already occupied cell in Simple Game mode."""
        self.gui.on_board_click(0, 0)
        initial_text = self.gui.board_buttons[0][0].cget("text")
        self.gui.on_board_click(0, 0)  
        self.assertEqual(self.gui.board_buttons[0][0].cget("text"), initial_text)  

    # User Story 5: Simple Game is Over
    def test_simple_mode_win_with_first_sos(self):
        """Simulate moves to create the first SOS in Simple mode and check for winner."""
            
        self.gui.board_buttons[0][0].config(text="S")
        self.gui.board_buttons[0][1].config(text="O")
        self.gui.board_buttons[0][2].config(text="S")
        
        self.assertTrue(self.simple_mode.check_for_winner())
        self.assertEqual(self.game_manager.get_winner(), self.game_manager.current_player)

    def test_no_sos_no_win(self):
        """Fill the board without forming an SOS and confirm the game continues with no winner."""
        self.gui.board_buttons[0][0].config(text="S")
        self.gui.board_buttons[0][1].config(text="O")
        self.gui.board_buttons[0][2].config(text="O")
        self.gui.board_buttons[1][0].config(text="O")
        self.gui.board_buttons[1][1].config(text="S")
        self.gui.board_buttons[1][2].config(text="O")
        self.gui.board_buttons[2][0].config(text="S")
        self.gui.board_buttons[2][1].config(text="S")
        self.gui.board_buttons[2][2].config(text="O")
        
        self.assertFalse(self.simple_mode.check_for_winner())
        self.assertIsNone(self.game_manager.get_winner())

    # User Story 6: Make a move in a general game
    def test_valid_general_move(self):
        """Test making a valid move in General Game mode."""
        self.gui.radio_var.set("General Game")
        self.gui.start_game()
        self.gui.on_board_click(1, 1)
        self.assertNotEqual(self.gui.board_buttons[1][1].cget("text"), " ")  
        

    # Test for 7.1: Additional Turn in General Mode after SOS Formation
    def test_general_mode_sos_additional_turn(self):
        """Check if creating an SOS grants an extra turn in General mode."""

        self.gui.board_buttons[0][0].config(text="S")
        self.gui.board_buttons[0][1].config(text="O")
        
        self.general_mode.make_move(0, 2, "S")  
        
        self.assertEqual(self.game_manager.get_current_player(), self.game_manager.current_player)

    # Test for 7.2: No SOS formation, game continues with next turn
    def test_no_sos_game_continues(self):
        """Simulate moves without forming an SOS and confirm game continues with the next turn."""
        self.gui.board_buttons[0][0].config(text="S")
        self.gui.board_buttons[0][1].config(text="O")
        self.gui.board_buttons[1][0].config(text="O")
        
        self.general_mode.make_move(1, 1, "S")
        
        self.assertNotEqual(self.game_manager.get_current_player(), self.game_manager.current_player)

    # Test for 7.3: Initial Game State in General Mode
    def test_initial_game_state_general_mode(self):
        """Verify General mode initializes correctly with the expected settings."""
        self.assertTrue(self.general_mode.is_active)
        self.assertEqual(self.game_manager.mode, "General")

    # Test for 7.4: End Game Restart Option in GUI
    def test_end_game_restart_option(self):
        """Check if restart/end options appear after game completion in GUI."""
        self.general_mode.end_game() 
        
        restart_button_state = self.gui.restart_button["state"] 
        self.assertEqual(restart_button_state, "normal")

if __name__ == '__main__':
    unittest.main()

