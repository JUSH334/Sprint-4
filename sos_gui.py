import tkinter as tk
from game_manager import GameManager
from player import HumanPlayer, ComputerPlayer


class SOSGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Application")
        self.board_size = 3
        self.game_mode = "Simple"
        self.is_game_active = False
        self.board_buttons = [] 
        self.blue_score_label = tk.Label(self.root, text="Blue SOS: 0")
        self.red_score_label = tk.Label(self.root, text="Red SOS: 0")
        self.game_manager = GameManager(self.board_size, self.game_mode, self)  # Pass self as the GUI reference
        self.create_ui()

    def create_ui(self):
        """Sets up the main layout for the game."""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20)

        # Top Frame for mode and size selection
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Set up the game controls (mode and board size)
        self.setup_game_controls(self.top_frame)

        # Player control frames on the left and right
        self.blue_frame = tk.Frame(self.main_frame)
        self.create_player_controls(self.blue_frame, "Blue")
        self.blue_frame.grid(row=1, column=0, padx=20, pady=10, sticky="n")

        self.red_frame = tk.Frame(self.main_frame)
        self.create_player_controls(self.red_frame, "Red")
        self.red_frame.grid(row=1, column=2, padx=20, pady=10, sticky="n")

        # Game board frame in the center
        self.create_scrollable_board_frame()

        # Bottom Frame for the Start/End button and Current Turn label
        self.bottom_frame = tk.Frame(self.main_frame)
        self.bottom_frame.grid(row=2, column=1, padx=20, pady=20)

        # Set up the start/end button and current turn label in the bottom frame
        self.setup_bottom_controls(self.bottom_frame)

        # Initial state: Only game mode and board size options enabled
        self.enable_start_options()

        # Add player score labels to show SOS count in General Game mode
        self.blue_score_label = tk.Label(self.main_frame, text="Blue SOS: 0")
        self.blue_score_label.grid(row=3, column=0, padx=10, pady=5)

        self.red_score_label = tk.Label(self.main_frame, text="Red SOS: 0")
        self.red_score_label.grid(row=3, column=2, padx=10, pady=5)

    def create_board_frame(self):
        """Sets up the frame that will hold the game board and initializes it."""
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.grid(row=1, column=1, padx=20, pady=10)
        self.create_board()

    def create_board(self):
        """Creates the game board dynamically with black text as the initial color."""
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.board_buttons = []
        for i in range(self.board_size):
            row_buttons = []
            for j in range(self.board_size):
                button = tk.Button(
                    self.board_frame,
                    text=' ',
                    width=5,
                    height=2,
                    fg="black",  # Set initial text color to black
                    command=lambda r=i, c=j: self.on_board_click(r, c)
                )
                button.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
                row_buttons.append(button)
            self.board_buttons.append(row_buttons)

        # Configure rows and columns to expand proportionally
        for i in range(self.board_size):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)

    def update_button(self, row, col, text, color="black"):
        """Updates the button text and color at the specified board position."""
        self.board_buttons[row][col].config(text=text, fg=color)

    def disable_buttons(self):
        """Disables all buttons on the board, typically when the game ends."""
        for row in self.board_buttons:
            for button in row:
                button.config(state="disabled")

    def create_player_controls(self, parent, player_name):
        """Creates control buttons for player choice between 'S' and 'O'."""
        label = tk.Label(parent, text=f"{player_name} player")
        label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        choice = tk.StringVar(value="S")
        s_button = tk.Radiobutton(parent, text="S", variable=choice, value="S")
        s_button.grid(row=1, column=0, padx=5, pady=5)
        o_button = tk.Radiobutton(parent, text="O", variable=choice, value="O")
        o_button.grid(row=2, column=0, padx=5, pady=5)

        setattr(self, f"{player_name.lower()}_controls", choice)

    def setup_game_controls(self, parent):
        label = tk.Label(parent, text="SOS")
        label.grid(row=0, column=0, padx=5, pady=1, sticky="w")
        self.radio_var = tk.StringVar(value="Simple Game")

        radio_frame = tk.Frame(parent)
        radio_frame.grid(row=0, column=1, padx=10, pady=1, sticky="w")

        tk.Radiobutton(radio_frame, text="Simple game", variable=self.radio_var, value="Simple Game").grid(row=0,
                                                                                                           column=0)
        tk.Radiobutton(radio_frame, text="General game", variable=self.radio_var, value="General Game").grid(row=0,
                                                                                                             column=1)

        board_size_label = tk.Label(parent, text="Board size")
        board_size_label.grid(row=0, column=2, padx=5, pady=1, sticky="w")
        self.board_size_var = tk.IntVar(value=3)
        vcmd = (self.root.register(self.validate_board_size), '%P')
        self.board_size_spinbox = tk.Spinbox(parent, from_=3, to=20, textvariable=self.board_size_var,
                                             validate="key", validatecommand=vcmd, width=3)
        self.board_size_spinbox.grid(row=0, column=3, padx=5, pady=1, sticky="w")

        # Player Type Selection for Blue Player
        tk.Label(parent, text="Blue Player").grid(row=1, column=0, padx=5, pady=1, sticky="w")
        self.blue_player_type = tk.StringVar(value="Human")
        tk.Radiobutton(parent, text="Human", variable=self.blue_player_type, value="Human").grid(row=1, column=1)
        tk.Radiobutton(parent, text="Computer", variable=self.blue_player_type, value="Computer").grid(row=1, column=2)

        # Player Type Selection for Red Player
        tk.Label(parent, text="Red Player").grid(row=2, column=0, padx=5, pady=1, sticky="w")
        self.red_player_type = tk.StringVar(value="Human")
        tk.Radiobutton(parent, text="Human", variable=self.red_player_type, value="Human").grid(row=2, column=1)
        tk.Radiobutton(parent, text="Computer", variable=self.red_player_type, value="Computer").grid(row=2, column=2)

    def setup_bottom_controls(self, parent):
        """Sets up the bottom controls like Start/End game button and Current Turn label."""
        self.start_button = tk.Button(parent, text="Start Game", command=self.toggle_game)
        self.start_button.grid(row=0, column=0, padx=10, pady=5)

        self.turn_label = tk.Label(parent, text="Current turn: Blue")
        self.turn_label.grid(row=1, column=0, padx=10, pady=5)
        self.turn_label.grid_remove()  # Hide initially until game starts

    def create_scrollable_board_frame(self):
        """Sets up the frame that will hold the game board."""
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.grid(row=1, column=1, padx=20, pady=10)

    def toggle_game(self):
        if self.start_button["text"] == "Start Game":
            self.start_game()
            self.start_button.config(text="End Game")
        else:
            self.end_game()
            self.start_button.config(text="Start Game")

    def start_game(self):
        self.is_game_active = True
        selected_mode = self.radio_var.get().split()[0] 
        self.board_size = self.board_size_var.get()

        # Retrieve player type selections
        blue_type = self.blue_player_type.get() 
        red_type = self.red_player_type.get()  

        # Set up the game manager with player types and game mode
        self.game_manager.reset_game(self.board_size, selected_mode, blue_type, red_type)

        # Display the chosen game mode and board size
        self.turn_label.config(text=f"Game Mode: {selected_mode}, Board Size: {self.board_size}x{self.board_size}")

        # Enable gameplay controls and disable start options
        self.create_board()
        self.enable_gameplay_controls()

        # Update turn label to show initial player turn after mode and size
        initial_turn = self.game_manager.current_player.color
        self.turn_label.config(
            text=f"Game Mode: {selected_mode}, Board Size: {self.board_size}x{self.board_size}\nCurrent turn: {initial_turn}")
        self.turn_label.grid()
        
         # Enable or disable the initial player's controls
        if isinstance(self.game_manager.current_player, HumanPlayer):
            self.set_player_controls_state(self.game_manager.current_player.color, "normal")
        else:
            self.set_player_controls_state(self.game_manager.current_player.color, "disabled")

        # Trigger the first move if the current player is a ComputerPlayer
        if isinstance(self.game_manager.current_player, ComputerPlayer):
            self.game_manager.current_player.make_move(self.game_manager.mode)

    def end_game(self):
        self.is_game_active = False
        self.game_manager.end_game()
        self.disable_buttons()
        self.turn_label.grid_remove()
        self.enable_start_options()

    def enable_start_options(self):
        """Enables game mode selection and board size options; disables other controls."""
        # Enable game mode and board size controls
        for widget in self.top_frame.winfo_children():
            if isinstance(widget, (tk.Radiobutton, tk.Spinbox)):
                widget.config(state="normal")

        # Disable player controls and board
        for widget in self.blue_frame.winfo_children() + self.red_frame.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.config(state="disabled")

        self.disable_buttons()
        self.start_button.config(state="normal")

    def enable_gameplay_controls(self):
        """Enables gameplay controls and disables game mode and board size options."""
        # Disable game mode and board size controls
        for widget in self.top_frame.winfo_children():
            if isinstance(widget, (tk.Radiobutton, tk.Spinbox)):
                widget.config(state="disabled")

        # Enable player controls
        for widget in self.blue_frame.winfo_children() + self.red_frame.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.config(state="normal")

        for row in self.board_buttons:
            for button in row:
                button.config(state="normal")
                
        self.start_button.config(state="normal")

    def on_board_click(self, row, col):
        """Delegates board click handling to the GameManager."""
        if not self.is_game_active:
            return

        # Delegate the click to the GameManager
        self.game_manager.on_board_click(row, col)

    def validate_board_size(self, new_value):
        if new_value.isdigit():
            return 3 <= int(new_value) <= 20
        return False

    def adjust_window_size(self, board_size):
        """Adjusts the window size based on the board size."""
        cell_size = 50
        board_pixel_size = board_size * cell_size
        max_window_size = 700
        self.root.geometry(
            f"{min(board_pixel_size + 100, max_window_size)}x{min(board_pixel_size + 100, max_window_size)}")

    def get_empty_cells(self):
        empty_cells = []
        for i, row in enumerate(self.board_buttons):
            for j, button in enumerate(row):
                if button and button.cget("text") == " ":
                    empty_cells.append((i, j))
        return empty_cells

    def set_player_controls_state(self, player_color, state="normal"):
        """Enable or disable the S and O buttons for the specified player."""
        frame = getattr(self, f"{player_color.lower()}_frame", None)
        if frame:
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Radiobutton):
                    widget.config(state=state)


