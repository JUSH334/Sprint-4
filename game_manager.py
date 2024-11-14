from game_modes import SimpleGameMode, GeneralGameMode
from player import HumanPlayer, ComputerPlayer


class GameManager:
    """Manages the game state, player turns, and game logic for SOS."""

    def __init__(self, board_size=3, game_mode="Simple", gui=None):
        self.board_size = board_size
        self.gui = gui
        self.is_game_active = True
        self.players = {"Blue": None, "Red": None}  # Stores player instances
        self.set_game_mode(game_mode)
        
        # Ensure players and current_player are initialized
        self.initialize_players()  

    def initialize_players(self, blue_type="Human", red_type="Human"):
        """Initialize players as human or computer based on GUI selection."""        
        # Create HumanPlayer or ComputerPlayer based on type
        self.players["Blue"] = HumanPlayer("Blue", "Blue", self.gui) if blue_type == "Human" else ComputerPlayer(
            "Blue", "Blue", self.gui)
        self.players["Red"] = HumanPlayer("Red", "Red", self.gui) if red_type == "Human" else ComputerPlayer(
            "Red","Red",self.gui)

        self.current_player = self.players["Blue"]  # Start with Blue player

    def set_game_mode(self, game_mode):
        """Sets the game mode and initializes the appropriate game mode class."""
        self.game_mode = game_mode
        if game_mode == "Simple":
            self.mode = SimpleGameMode(self.board_size, self)
            if self.gui:
                self.gui.blue_score_label.grid_remove()
                self.gui.red_score_label.grid_remove()
        elif game_mode == "General":
            self.mode = GeneralGameMode(self.board_size, self)
            if self.gui:
                self.gui.blue_score_label.grid()
                self.gui.red_score_label.grid()

    def on_board_click(self, row, col):
        """Handles a click on the board for a human player's move."""
        if isinstance(self.current_player, HumanPlayer):
            self.current_player.make_move(self.mode, row, col)  # Delegates move to game mode

    def switch_turn(self):
        """Switches the turn between players and updates the GUI."""
        self.current_player = self.players["Red"] if self.current_player == self.players["Blue"] else self.players[
            "Blue"]
        self.gui.turn_label.config(text=f"Current turn: {self.current_player.color}")

         # Enable or disable controls based on the player type
        if isinstance(self.current_player, HumanPlayer):
            self.gui.set_player_controls_state(self.current_player.color, "normal")
        else:  # Disable controls for ComputerPlayer
            self.gui.set_player_controls_state(self.current_player.color, "disabled")

        # If the current player is a ComputerPlayer, trigger their move
        if isinstance(self.current_player, ComputerPlayer):
            self.gui.root.after(1000, lambda: self.current_player.make_move(self.mode))

    def reset_game(self, board_size, game_mode, blue_type="Human", red_type="Human"):
        """Resets the game with a new board size, game mode, and player types."""
        self.board_size = board_size
        self.set_game_mode(game_mode)
        self.initialize_players(blue_type, red_type)  # Initialize players based on GUI selection
        self.mode.reset_game(board_size)  # Reset the game mode-specific logic
        self.current_player = self.players["Blue"]  # Start with Blue player

    def end_game(self):
        """Ends the game by disabling interactions and setting the game state."""
        self.is_game_active = False
        self.mode.is_game_active = False
        self.gui.disable_buttons()

    def is_board_full(self):
        """Checks if the entire board is filled."""
        return all(
            button.cget("text") != ' ' 
            for row in self.gui.board_buttons 
            for button in row
        )

