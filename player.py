import random

class BasePlayer:
    """Base class for a player in the SOS game."""

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.choice = "S"  # Default choice

    def get_choice(self):
        """Returns the current choice ('S' or 'O')."""
        return self.choice

    def make_move(self, game_mode, row=None, col=None):
        """Method to make a move. Specific to each subclass."""
        choice = self.get_choice()
        if choice:
            row, col = choice
            game_mode.make_move(row, col, "S")


class HumanPlayer(BasePlayer):
    """Represents a human player."""

    def __init__(self, name, color, gui):
        super().__init__(name, color)
        self.gui = gui

    def make_move(self, game_mode, row, col):
        self.choice = getattr(self.gui, f"{self.color.lower()}_controls").get()
        game_mode.make_move(row, col, self.choice)


class ComputerPlayer(BasePlayer): 
    """Represents a computer player."""

    def __init__(self, name, color, gui):
        super().__init__(name, color)
        self.gui = gui

    def make_move(self, game_mode):
        """Automatically make a move using a basic strategy."""
        
        # 1. Check for immediate SOS opportunities
        move = self.find_sos_opportunity(game_mode)
        if move:
            row, col, self.choice = move  # Unpack move details
            game_mode.make_move(row, col, self.choice)
            return

        # 2. Block the human player's SOS opportunities
        move = self.find_block_opportunity(game_mode)
        if move:
            row, col, self.choice = move
            game_mode.make_move(row, col, self.choice)
            return

        # 3. Default to a random move
        empty_cells = self.gui.get_empty_cells()
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.choice = "S" if random.choice([True, False]) else "O"  # Randomly choose S or O
            game_mode.make_move(row, col, self.choice)

    def find_sos_opportunity(self, game_mode):
        """Find a cell that would complete an SOS sequence for the computer."""
        for row in range(self.gui.board_size):
            for col in range(self.gui.board_size):
                # Check if placing "S" or "O" at (row, col) completes an SOS
                if self.gui.board_buttons[row][col].cget("text") == " ":
                    # Try placing "S"
                    if self.check_sos(row, col, "S", game_mode):
                        return (row, col, "S")
                    # Try placing "O"
                    if self.check_sos(row, col, "O", game_mode):
                        return (row, col, "O")
        return None

    def find_block_opportunity(self, game_mode):
        """Find a cell that would block the human player from creating an SOS."""
        for row in range(self.gui.board_size):
            for col in range(self.gui.board_size):
                # Check if placing "S" at (row, col) blocks a potential SOS by the human player
                if self.gui.board_buttons[row][col].cget("text") == " ":
                    if self.check_opponent_sos(row, col, "S", game_mode):
                        return (row, col, "S")
        return None

    def check_sos(self, row, col, character, game_mode):
        """Check if placing a character at (row, col) would create an SOS."""
        # Temporarily place the character in the empty cell
        self.gui.board_buttons[row][col].config(text=character)
        # Check for SOS patterns (horizontal, vertical, diagonal)
        is_sos = game_mode.is_sos_sequence(row, col)
        # Reset the cell to empty after checking
        self.gui.board_buttons[row][col].config(text=" ")
        return is_sos

    def check_opponent_sos(self, row, col, character, game_mode):
        """Check if placing 'S' in (row, col) could block an opponent's potential SOS."""
        # Temporarily place the character in the empty cell
        self.gui.board_buttons[row][col].config(text=character)
        is_sos = game_mode.is_sos_sequence(row, col)
        self.gui.board_buttons[row][col].config(text=" ")
        return is_sos
