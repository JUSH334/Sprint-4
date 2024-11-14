from player import ComputerPlayer

class BaseGameMode:
    """Base class for common game mode functionality."""

    def __init__(self, board_size, game_manager):
        self.board_size = board_size
        self.game_manager = game_manager
        self.is_game_active = False

    def reset_game(self, board_size):
        """Resets the board and game state."""
        self.board_size = board_size
        self.is_game_active = True

    def check_sos(self, row, col):
        """Counts the number of SOS patterns created around the given row, col position."""
        directions = [
            (0, 1),  # Horizontal
            (1, 0),  # Vertical
            (1, 1),  # Diagonal top-left to bottom-right
            (1, -1)  # Diagonal top-right to bottom-left
        ]

        sos_cells = []
        sos_count = 0
        
        for dx, dy in directions:
            # Each call to get_sos_sequence will either add 3 cells for an SOS or an empty list
            sequence1 = self.get_sos_sequence(row - 2 * dx, col - 2 * dy, row - dx, col - dy, row, col)
            sequence2 = self.get_sos_sequence(row - dx, col - dy, row, col, row + dx, col + dy)
            sequence3 = self.get_sos_sequence(row, col, row + dx, col + dy, row + 2 * dx, col + 2 * dy)

            for sequence in [sequence1, sequence2, sequence3]:
                if sequence:
                    sos_cells.extend(sequence) 
                    sos_count += 1               
        return sos_cells, sos_count 
                    
    def get_sos_sequence(self, x1, y1, x2, y2, x3, y3):
        """Helper method to check for 'S-O-S' sequence and return coordinates if found."""
        board_buttons = self.game_manager.gui.board_buttons
        if self.is_valid_position(x1, y1) and self.is_valid_position(x2, y2) and self.is_valid_position(x3, y3):
            if (board_buttons[x1][y1].cget("text") == 'S' and
                board_buttons[x2][y2].cget("text") == 'O' and
                board_buttons[x3][y3].cget("text") == 'S'):
                return [(x1, y1), (x2, y2), (x3, y3)]             
        return []

    def is_valid_position(self, row, col):
        """Checks if the given position is within the board boundaries."""
        return 0 <= row < self.board_size and 0 <= col < self.board_size
    
    def is_valid_move(self, row, col):
        """Check if the specified move is within bounds and on an empty cell."""
        # Check both position bounds and cell content via the GUI's board
        return self.is_valid_position(row, col) and \
               self.game_manager.gui.board_buttons[row][col].cget("text") == " "

    def end_game_with_draw(self):
        """Handle game draw scenario."""
        self.game_manager.gui.turn_label.config(text="The game is a draw!")
        self.game_manager.end_game()
        

class SimpleGameMode(BaseGameMode):
    """Implements the simple game mode."""
    def __init__(self, board_size, game_manager):
        self.board_size = board_size
        self.game_manager = game_manager
        self.board = [[" " for _ in range(board_size)] for _ in range(board_size)]

    def make_move(self, row, col, character):
        if not self.is_valid_move(row, col):
            self.game_manager.gui.turn_label.config(text=f"Invalid move. Try again. Current Turn: {self.game_manager.current_player.color}")
            return

        self.game_manager.gui.update_button(row, col, character, "black")

        # Check for SOS sequences
        sos_cells, sos_count = self.check_sos(row, col)
        if sos_cells:
            # Change color of SOS cells to player's color
            player_color = "blue" if self.game_manager.current_player.color == "Blue" else "red"
            for (sos_row, sos_col) in sos_cells:
                self.game_manager.gui.update_button(sos_row, sos_col, self.game_manager.gui.board_buttons[sos_row][sos_col].cget("text"), player_color)
            self.end_game_with_winner()
        elif self.game_manager.is_board_full():
            self.end_game_with_draw()
        else:
            self.game_manager.switch_turn()
            
    def check_sos(self, row, col):
        return super().check_sos(row, col)

    def end_game_with_winner(self):
        """Declare the current player as winner and end the game."""
        self.game_manager.gui.turn_label.config(text=f"{self.game_manager.current_player.color} wins!")
        self.game_manager.end_game()

    def end_game_with_draw(self):
        """Handle game draw scenario."""
        self.game_manager.gui.turn_label.config(text="The game is a draw! No SOS was created.")
        self.game_manager.end_game()
        
    def is_sos_sequence(self, row, col):
        """Check if placing a character at (row, col) completes an SOS sequence."""
        # Check all possible directions for an SOS pattern
        return (
            self.check_direction(row, col, 0, 1) or   # Horizontal
            self.check_direction(row, col, 1, 0) or   # Vertical
            self.check_direction(row, col, 1, 1) or   # Diagonal /
            self.check_direction(row, col, 1, -1)     # Diagonal \
        )
    
    def check_direction(self, row, col, delta_row, delta_col):
        """Check for an SOS pattern in a specific direction."""
        # Ensure within bounds and check if we have an "S", "O", "S" in the given direction
        try:
            if (
                self.board[row][col] == "S" and
                self.board[row + delta_row][col + delta_col] == "O" and
                self.board[row + 2 * delta_row][col + 2 * delta_col] == "S"
            ):
                return True
        except IndexError:
            # Out of bounds, so no SOS possible in this direction
            return False
        return False


class GeneralGameMode(BaseGameMode):
    """Implements the general game mode."""

    def __init__(self, board_size, game_manager):
        super().__init__(board_size, game_manager)
        self.sos_count = {"Blue": 0, "Red": 0}
        self.board_size = board_size
        self.game_manager = game_manager
        self.board = [[" " for _ in range(board_size)] for _ in range(board_size)]

    def reset_game(self, board_size):
        """Resets the board, game state, and scores."""
        super().reset_game(board_size)
        self.sos_count = {"Blue": 0, "Red": 0}
        self.update_score_display()

    def update_score_display(self):
        """Updates the SOS count labels."""
        self.game_manager.gui.blue_score_label.config(text=f"Blue SOS: {self.sos_count['Blue']}")
        self.game_manager.gui.red_score_label.config(text=f"Red SOS: {self.sos_count['Red']}")

    def make_move(self, row, col, character):
        if not self.is_valid_move(row, col):
            self.game_manager.gui.turn_label.config(text=f"Invalid move. Try again. Current Turn: {self.game_manager.current_player.color}")
            return

        self.game_manager.gui.update_button(row, col, character, "black")

        # Check for SOS formations
        sos_cells, sos_count = self.check_sos(row, col)
        if sos_cells:
            player_color = "blue" if self.game_manager.current_player.color == "Blue" else "red"    
            for (sos_row, sos_col) in sos_cells:
                current_text = self.game_manager.gui.board_buttons[sos_row][sos_col].cget("text")
                self.game_manager.gui.update_button(sos_row, sos_col, current_text, player_color)
            
            sos_count_increment = sos_count  
            self.sos_count[self.game_manager.current_player.color] += sos_count_increment
            self.update_score_display()

            self.game_manager.gui.turn_label.config(
                text=f"{self.game_manager.current_player.color} formed {sos_count_increment} SOS! They get an extra turn!"
            )
            
            # Check if the board is full after an SOS
            if self.game_manager.is_board_full():
                self.end_game_based_on_score() 
                return

            # If the current player is a ComputerPlayer, make an extra move automatically
            if isinstance(self.game_manager.current_player, ComputerPlayer):
                self.game_manager.gui.root.after(4000, lambda: self.game_manager.current_player.make_move(self))
                return 
            else:
                return

        if self.game_manager.is_board_full():
            self.end_game_based_on_score()
        else:
            self.game_manager.switch_turn()

    def update_score_display(self):
        """Updates the SOS count labels."""
        self.game_manager.gui.blue_score_label.config(text=f"Blue SOS: {self.sos_count['Blue']}")
        self.game_manager.gui.red_score_label.config(text=f"Red SOS: {self.sos_count['Red']}")

    def handle_extra_turn(self, sos_formed):
        """Notify player of an extra turn for forming SOS."""
        self.game_manager.gui.turn_label.config(
            text=f"{self.game_manager.current_player.color} formed {sos_formed} SOS! They get an extra turn!"
        )

        # If the current player is a ComputerPlayer, make the move automatically
        self.extra_turn = True
        
    def is_sos_sequence(self, row, col):
        """Check if placing a character at (row, col) completes an SOS sequence."""
        # Check all possible directions for an SOS pattern
        return (
            self.check_direction(row, col, 0, 1) or   # Horizontal
            self.check_direction(row, col, 1, 0) or   # Vertical
            self.check_direction(row, col, 1, 1) or   # Diagonal /
            self.check_direction(row, col, 1, -1)     # Diagonal \
        )
    
    def check_direction(self, row, col, delta_row, delta_col):
        """Check for an SOS pattern in a specific direction."""
        # Ensure within bounds and check if we have an "S", "O", "S" in the given direction
        try:
            if (
                self.board[row][col] == "S" and
                self.board[row + delta_row][col + delta_col] == "O" and
                self.board[row + 2 * delta_row][col + 2 * delta_col] == "S"
            ):
                return True
        except IndexError:
            # Out of bounds, so no SOS possible in this direction
            return False
        return False

    def end_game_based_on_score(self):
        """Determine winner based on SOS count or declare a draw."""
        blue_score, red_score = self.sos_count["Blue"], self.sos_count["Red"]
        if blue_score > red_score:
            self.game_manager.gui.turn_label.config(text="Blue wins!")
        elif red_score > blue_score:
            self.game_manager.gui.turn_label.config(text="Red wins!")
        else:
            self.end_game_with_draw()
        self.game_manager.end_game()

