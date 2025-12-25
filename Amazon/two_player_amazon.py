import tkinter as tk
from tkinter import messagebox, filedialog
import pickle
import os
from datetime import datetime
import time
import socket
import threading
from tkinter import simpledialog


class AmazonChess:
    """
    Amazon Chess (Game of the Amazons) implementation.
    Rules:
    - Two players (A and B) take turns moving their Amazons and shooting arrows
    - Each turn: Move one Amazon (like a queen in chess) then shoot an arrow from its new position
    - Arrows block cells permanently - no piece can move through or land on them
    - Last player able to make a complete move wins
    """
    
    def __init__(self):
        self.board_size = 10
        self.move_history = []  # Track move history for undo functionality
        self.game_archive = []  # Store complete game for replay
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = self.get_initial_board()
        self.current_player = 'A'  # Player A starts
        self.selected_amazon = None
        self.moved_amazon = None
        self.phase = "select"
        self.move_history = []  # Clear history on reset
        self.game_over = False
        self.winner = None
        self.game_archive = []  # Clear archive on reset
        
        # Record initial state in archive
        self._record_in_archive('initial', None, None, None)
    
    def get_initial_board(self):
        """
        Create and return the initial 10x10 game board.
        Player A Amazons at: (0,3), (0,6), (3,0), (3,9)
        Player B Amazons at: (6,0), (6,9), (9,3), (9,6)
        """
        board = [[None for _ in range(10)] for _ in range(10)]
        
        # Player A initial positions (White Amazons)
        board[0][3] = 'A'
        board[0][6] = 'A'
        board[3][0] = 'A'
        board[3][9] = 'A'
        
        # Player B initial positions (Black Amazons)
        board[6][0] = 'B'
        board[6][9] = 'B'
        board[9][3] = 'B'
        board[9][6] = 'B'
        
        return board
    
    def is_valid_position(self, row, col):
        """Check if position is within board bounds"""
        return 0 <= row < self.board_size and 0 <= col < self.board_size
    
    def get_available_moves(self, start_row, start_col):
        """
        Get all valid move positions for an Amazon at (start_row, start_col)
        Amazons move like queens in chess: straight lines in 8 directions
        Cannot jump over pieces or move to occupied cells
        """
        if not self.is_valid_position(start_row, start_col):
            return []
        
        # Check if there's actually an Amazon at the start position
        if self.board[start_row][start_col] not in ['A', 'B']:
            return []
        
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),  # Up-left, Up, Up-right
            (0, -1),           (0, 1),   # Left, Right
            (1, -1),  (1, 0),  (1, 1)    # Down-left, Down, Down-right
        ]
        
        for dr, dc in directions:
            r, c = start_row + dr, start_col + dc
            
            # Move in this direction until we hit an obstacle or board edge
            while self.is_valid_position(r, c):
                # Stop if cell is occupied
                if self.board[r][c] is not None:
                    break
                
                moves.append((r, c))
                r += dr
                c += dc
        
        return moves
    
    def get_available_shots(self, amazon_row, amazon_col):
        """
        Get all valid arrow shot positions from an Amazon at (amazon_row, amazon_col)
        Arrow shooting follows the same movement rules as Amazons
        """
        return self.get_available_moves(amazon_row, amazon_col)
    
    def _record_in_archive(self, action_type, start_pos, end_pos, arrow_pos):
        """Record a game action in the archive - FIXED to record every action"""
        archive_entry = {
            'type': action_type,
            'player': self.current_player,
            'board': [row[:] for row in self.board],  # Deep copy
            'start_pos': start_pos,
            'end_pos': end_pos,
            'arrow_pos': arrow_pos,
            'phase': self.phase,
            'game_over': self.game_over,
            'winner': self.winner,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'turn_number': self.get_turn_count()
        }
        self.game_archive.append(archive_entry)
        print(f"📝 Recorded {action_type} for player {self.current_player} in archive")
    
    def move_amazon(self, start, end):
        """Move an Amazon from start position to end position"""
        start_row, start_col = start
        end_row, end_col = end
        
        # Validate positions
        if not (self.is_valid_position(start_row, start_col) and 
                self.is_valid_position(end_row, end_col)):
            return False
        
        # Check if start position has an Amazon of current player
        if self.board[start_row][start_col] != self.current_player:
            return False
        
        # Check if end position is empty
        if self.board[end_row][end_col] is not None:
            return False
        
        # Check if move is valid (straight line, no jumping)
        if not self.is_valid_move_path(start, end):
            return False
        
        # Store move in history before executing
        move_data = {
            'type': 'move',
            'player': self.current_player,
            'start': start,
            'end': end,
            'board_state': [row[:] for row in self.board]  # Save board state
        }
        self.move_history.append(move_data)

        # RECORD TURN COMPLETION Nov 22 fixation Archive
        if len(self.game_archive) > 1:
            self._record_in_archive('turn_complete', None, None, None)

        # Record MOVE step in archive (separate from shot)
        self._record_in_archive('move', start, end, None)
        
        # Perform the move
        self.board[end_row][end_col] = self.current_player
        self.board[start_row][start_col] = None
        
        # Store the moved Amazon position for shooting phase
        self.moved_amazon = (end_row, end_col)
        
        return True

    def undo_move(self):
        """Undo the last move and return to move phase"""
        if not self.move_history or self.move_history[-1]['type'] != 'move':
            return False  # Nothing to undo or last action wasn't a move
        
        # Get the last move data
        last_move = self.move_history.pop()
        
        # Restore the board state
        self.board = last_move['board_state']
        
        # Remove the last move from archive (and any subsequent shot)
        # Find the last move entry and remove it and anything after
        for i in range(len(self.game_archive) - 1, -1, -1):
            if self.game_archive[i]['type'] == 'move':
                self.game_archive = self.game_archive[:i]
                break
        
        # Reset game state to move phase
        self.selected_amazon = last_move['start']
        self.moved_amazon = None
        self.phase = "move"
        
        return True
    
    def shoot_arrow(self, amazon_pos, arrow_pos):
        """Shoot an arrow from amazon_pos to arrow_pos"""
        amazon_row, amazon_col = amazon_pos
        arrow_row, arrow_col = arrow_pos
        
        # Validate positions
        if not (self.is_valid_position(amazon_row, amazon_col) and 
                self.is_valid_position(arrow_row, arrow_col)):
            return False
        
        # Check if amazon position has an Amazon of current player
        if self.board[amazon_row][amazon_col] != self.current_player:
            return False
        
        # Check if arrow position is empty
        if self.board[arrow_row][arrow_col] is not None:
            return False
        
        # Check if shot is valid (straight line, no jumping)
        if not self.is_valid_move_path(amazon_pos, arrow_pos):
            return False
        
        # Store shot in history
        shot_data = {
            'type': 'shot',
            'player': self.current_player,
            'arrow_pos': arrow_pos,
            'board_state': [row[:] for row in self.board]  # Save board state
        }
        self.move_history.append(shot_data)
        
        # Record SHOT step in archive (separate from move)
        self._record_in_archive('shot', amazon_pos, None, arrow_pos)
        
        # Place the arrow (block the cell)
        self.board[arrow_row][arrow_col] = 'X'
        
        return True
    
    def is_valid_move_path(self, start, end):
        """
        Check if the path from start to end is a valid straight line move
        with no pieces in between
        """
        start_row, start_col = start
        end_row, end_col = end
        
        # Check if it's a straight line (horizontal, vertical, or diagonal)
        row_diff = end_row - start_row
        col_diff = end_col - start_col
        
        # Not a straight line if neither same row, same column, nor equal absolute differences
        if not (row_diff == 0 or col_diff == 0 or abs(row_diff) == abs(col_diff)):
            return False
        
        # Determine direction increments
        dr = 0 if row_diff == 0 else (1 if row_diff > 0 else -1)
        dc = 0 if col_diff == 0 else (1 if col_diff > 0 else -1)
        
        # Check all cells between start and end (excluding start and end)
        steps = max(abs(row_diff), abs(col_diff))
        for step in range(1, steps):
            r = start_row + step * dr
            c = start_col + step * dc
            
            # If any intermediate cell is occupied, path is blocked
            if self.board[r][c] is not None:
                return False
        
        return True
    
    def check_win_condition(self, player):
        """
        Check if the specified player has any legal moves remaining
        Player loses if they cannot make a complete move (move + shoot)
        Returns True if player has NO legal moves (player loses)
        """
        # Check all Amazons of the player
        for amazon_row in range(self.board_size):
            for amazon_col in range(self.board_size):
                if self.board[amazon_row][amazon_col] == player:
                    # Get all possible moves for this Amazon
                    moves = self.get_available_moves(amazon_row, amazon_col)
                    
                    # For each possible move, check if there's at least one valid shot
                    for move_row, move_col in moves:
                        # Create a temporary board to simulate the move
                        temp_board = [row[:] for row in self.board]  # Deep copy
                        
                        # Simulate the move on temporary board
                        temp_board[amazon_row][amazon_col] = None
                        temp_board[move_row][move_col] = player
                        
                        # Now check if there's at least one valid shot from the new position
                        shots = self.get_available_shots_from_position(temp_board, move_row, move_col)
                        if shots:
                            return False  # Player has at least one complete move
        
        # If we get here, no complete moves were found
        return True  # Player has no legal moves

    def get_available_shots_from_position(self, board_state, amazon_row, amazon_col):
        """
        Get all valid arrow shot positions from an Amazon at (amazon_row, amazon_col)
        using the provided board state
        """
        if not self.is_valid_position(amazon_row, amazon_col):
            return []
        
        # Check if there's actually an Amazon at the start position in this board state
        if board_state[amazon_row][amazon_col] not in ['A', 'B']:
            return []
        
        shots = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),  # Up-left, Up, Up-right
            (0, -1),           (0, 1),   # Left, Right
            (1, -1),  (1, 0),  (1, 1)    # Down-left, Down, Down-right
        ]
        
        for dr, dc in directions:
            r, c = amazon_row + dr, amazon_col + dc
            
            # Move in this direction until we hit an obstacle or board edge
            while self.is_valid_position(r, c):
                # Stop if cell is occupied
                if board_state[r][c] is not None:
                    break
                
                shots.append((r, c))
                r += dr
                c += dc
        
        return shots
    
    def complete_turn(self):
        """Complete the current turn and switch to next player"""
        # Switch player first
        next_player = 'B' if self.current_player == 'A' else 'A'
        
        # Check win condition for the NEXT player (the one about to move)
        if self.check_win_condition(next_player):
            self.game_over = True
            # The next player cannot move, so the CURRENT player wins
            self.winner = self.current_player
            # Record game over in archive
            self._record_in_archive('game_over', None, None, None)
        else:
            # Game continues, switch to next player
            self.current_player = next_player
        
        # Reset for next turn
        self.selected_amazon = None
        self.moved_amazon = None
        self.phase = "select"
        
        # Clear move history for the completed turn
        self.move_history = [move for move in self.move_history if move['player'] == self.current_player]
        
        # RECORD TURN COMPLETION
        if not self.game_over and not self.winner:
            self._record_in_archive('turn_complete', None, None, None)
    
    def get_board_state(self):
        """Return current board state for saving"""
        return {
            'board': [row[:] for row in self.board],  # Deep copy
            'current_player': self.current_player,
            'selected_amazon': self.selected_amazon,
            'moved_amazon': self.moved_amazon,
            'phase': self.phase,
            'game_over': self.game_over,
            'winner': self.winner,
            'game_archive': self.game_archive.copy()
        }
    
    def set_board_state(self, state):
        """Restore board state from saved data"""
        self.board = state['board']
        self.current_player = state['current_player']
        self.selected_amazon = state['selected_amazon']
        self.moved_amazon = state['moved_amazon']
        self.phase = state['phase']
        self.game_over = state.get('game_over', False)
        self.winner = state.get('winner', None)
        self.game_archive = state.get('game_archive', [])
    
    def get_game_archive(self):
        """Return the complete game archive"""
        return self.game_archive.copy()
    
    def set_game_archive(self, archive):
        """Set the game archive for replay"""
        self.game_archive = archive.copy()
    
    def replay_to_move(self, move_index):
        """Replay the game to a specific move index"""
        if move_index < 0 or move_index >= len(self.game_archive):
            return False
        
        # Get the archive state at the specified index
        archive_state = self.game_archive[move_index]
        
        # Restore the board and game state
        self.board = [row[:] for row in archive_state['board']]
        self.current_player = archive_state['player']
        self.phase = archive_state['phase']
        self.game_over = archive_state['game_over']
        self.winner = archive_state['winner']
        
        # Reset selection states for replay
        self.selected_amazon = None
        self.moved_amazon = None
        
        return True
    
    def get_turn_count(self):
        """Get the number of complete turns in the archive"""
        # Count complete moves (each player's move+shot counts as one turn)
        moves = [entry for entry in self.game_archive if entry['type'] == 'move']
        return len(moves)  # Each move represents one player's complete turn


class AmazonChessGUI:
    """GUI for Amazon Chess game using Tkinter"""
    
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.cell_size = 60
        self.colors = {
            'light': '#F0D9B5',  # Light square color
            'dark': '#B58863',   # Dark square color
            'highlight': '#90EE90',  # Highlight color for selected Amazon
            'move_highlight': '#FFFACD',  # Light yellow for available moves
            'shot_highlight': '#E6E6FA',  # Light purple for available shots
            'A': 'white',  # Player A piece color
            'B': 'black',  # Player B piece color
            'arrow': 'darkblue'  # Arrow color
        }
        self.available_moves = []
        self.available_shots = []
        self.replay_mode = False
        self.replay_index = 0
        self.multiplayer_lobby = SimpleMultiplayerLobby(self)
        
        self.create_gui()
        self.setup_mouse_interaction()

    def create_gui(self):
        """Create the main GUI layout with improved button organization"""
        # Configure main window
        self.root.title("Amazon Chess")
        self.root.geometry("800x900")
        self.root.minsize(700, 800)
        self.root.resizable(True, True)
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg='light gray')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create status frame
        self.status_frame = tk.Frame(main_frame, bg='light gray')
        self.status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(
            self.status_frame, 
            text="Player A's Turn - Select an Amazon",
            font=("Arial", 14),
            bg='light gray'
        )
        self.status_label.pack()
        
        # Create board frame
        board_frame = tk.Frame(main_frame, bg='black')
        board_frame.pack(pady=20, anchor='center')
        
        # Create canvas for the game board
        canvas_size = self.cell_size * 10
        self.canvas = tk.Canvas(
            board_frame, 
            width=canvas_size, 
            height=canvas_size,
            bg='white',
            highlightthickness=2,
            highlightbackground='black'
        )
        self.canvas.pack()
        
        # ===== REORGANIZED BUTTON LAYOUT =====
        
        # Row 1: Game Controls + Multiplayer
        control_row1 = tk.Frame(main_frame, bg='light gray')
        control_row1.pack(fill=tk.X, pady=5)
        
        # Left side: Game controls
        left_controls = tk.Frame(control_row1, bg='light gray')
        left_controls.pack(side=tk.LEFT)
        
        # Reset button
        self.reset_button = tk.Button(
            left_controls,
            text="Reset Game",
            font=("Arial", 12),
            command=self.reset_game,
            bg='#FF6B6B'
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Undo button
        self.undo_button = tk.Button(
            left_controls,
            text="Undo Move",
            font=("Arial", 12),
            command=self.undo_move,
            state=tk.DISABLED
        )
        self.undo_button.pack(side=tk.LEFT, padx=5)
        
        # Exit button - ADD THIS
        self.exit_button = tk.Button(
            left_controls,
            text="Exit Game",
            font=("Arial", 12),
            command=self.exit_game,
            bg='#FF4757'
        )
        self.exit_button.pack(side=tk.LEFT, padx=5)
        
        # Right side: Multiplayer controls
        right_controls = tk.Frame(control_row1, bg='light gray')
        right_controls.pack(side=tk.RIGHT)
        
        # Add multiplayer buttons to right side
        self.multiplayer_lobby.create_lobby_buttons(right_controls)
        
        # Row 2: Save/Load + Match Controls
        control_row2 = tk.Frame(main_frame, bg='light gray')
        control_row2.pack(fill=tk.X, pady=5)
        
        # Left side: Save/Load game
        left_controls2 = tk.Frame(control_row2, bg='light gray')
        left_controls2.pack(side=tk.LEFT)
        
        # Save Game button
        self.save_button = tk.Button(
            left_controls2,
            text="Save Game",
            font=("Arial", 12),
            command=self.save_game,
            bg='#4ECDC4'
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Load Game button
        self.load_button = tk.Button(
            left_controls2,
            text="Load Game",
            font=("Arial", 12),
            command=self.load_game,
            bg='#45B7D1'
        )
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        # Right side: Match controls (ALWAYS VISIBLE)
        right_controls2 = tk.Frame(control_row2, bg='light gray')
        right_controls2.pack(side=tk.RIGHT)
        
        # Replay button
        self.replay_button = tk.Button(
            right_controls2,
            text="Replay Game",
            font=("Arial", 12),
            command=self.start_replay,
            bg='#FFD93D',
            state=tk.DISABLED  # Initially disabled
        )
        self.replay_button.pack(side=tk.LEFT, padx=5)
        
        # Save Match button
        self.save_match_button = tk.Button(
            right_controls2,
            text="Save Match",
            font=("Arial", 12),
            command=self.save_match,
            bg='#6BCF7F',
            state=tk.DISABLED  # Initially disabled
        )
        self.save_match_button.pack(side=tk.LEFT, padx=5)
        
        # Load Match button
        self.load_match_button = tk.Button(
            right_controls2,
            text="Load Match",
            font=("Arial", 12),
            command=self.load_match,
            bg='#4D96FF'
        )
        self.load_match_button.pack(side=tk.LEFT, padx=5)
        
        # Create replay controls frame (initially hidden)
        self.replay_frame = tk.Frame(main_frame, bg='light gray')
        
        # Replay controls
        replay_controls = tk.Frame(self.replay_frame, bg='light gray')
        replay_controls.pack(fill=tk.X, pady=5)
        
        tk.Label(replay_controls, text="Replay Controls:", font=("Arial", 12), bg='light gray').pack(side=tk.LEFT, padx=5)
        
        self.prev_button = tk.Button(
            replay_controls,
            text="⏮ Previous",
            font=("Arial", 10),
            command=self.previous_move,
            state=tk.DISABLED
        )
        self.prev_button.pack(side=tk.LEFT, padx=2)
        
        self.next_button = tk.Button(
            replay_controls,
            text="Next ⏭",
            font=("Arial", 10),
            command=self.next_move,
            state=tk.DISABLED
        )
        self.next_button.pack(side=tk.LEFT, padx=2)
        
        self.exit_replay_button = tk.Button(
            replay_controls,
            text="Exit Replay",
            font=("Arial", 10),
            command=self.exit_replay,
            bg='#FF6B6B'
        )
        self.exit_replay_button.pack(side=tk.LEFT, padx=10)
        
        self.replay_label = tk.Label(
            replay_controls,
            text="Move 0/0",
            font=("Arial", 10),
            bg='light gray'
        )
        self.replay_label.pack(side=tk.RIGHT, padx=5)
        
        # Draw the initial board
        self.draw_board()
        self.update_button_states()
    
    def exit_game(self):
        """Exit the game application"""
        if messagebox.askokcancel("Exit Game", "Are you sure you want to exit Amazon Chess?"):
            # Clean up network connections
            if hasattr(self, 'multiplayer_lobby') and self.multiplayer_lobby.connected:
                self.multiplayer_lobby.disconnect()
            
            # Close the application
            self.root.quit()
            self.root.destroy()

    def reset_game(self):
        """Reset the game to initial state and sync with opponent"""
        # Call the game's reset method directly
        self.game.reset_game()
        
        # SYNC RESET WITH OPPONENT IN MULTIPLAYER
        if self.multiplayer_lobby.connected:
            # Send reset state to opponent
            from two_player_amazon_network import create_state_update_message, MessageType
            
            # Create initial board state
            initial_board = self.game.get_initial_board()
            changes = []
            for row in range(10):
                for col in range(10):
                    if initial_board[row][col] is not None:
                        changes.append({
                            "position": [row, col],
                            "to": initial_board[row][col]
                        })
            
            reset_state = create_state_update_message(
                changes,
                'A',  # Player A always starts after reset
                "select",
                0,
                False,  # game_over = False
                None    # winner = None
            )
            self.multiplayer_lobby.network_manager.send_message(MessageType.STATE_UPDATE, reset_state['data'])
            print("🔄 Sent reset state to opponent")
        
        self.available_moves = []
        self.available_shots = []
        self.replay_mode = False
        self.replay_index = 0
        self.replay_frame.pack_forget()
        self.draw_board()
        self.update_status()
        self.update_button_states()  # UPDATE BUTTON STATES AFTER RESET

    def undo_move(self):
        """Handle undo button click"""
        if self.game.phase == "shoot":
            success = self.game.undo_move()
            if success:
                # Recalculate available moves
                if self.game.selected_amazon:
                    self.available_moves = self.game.get_available_moves(
                        self.game.selected_amazon[0], self.game.selected_amazon[1]
                    )
                self.available_shots = []
                self.draw_board()
                self.update_status()
        
        self.update_button_states()

    def update_button_states(self):
        """Enable/disable buttons based on game state"""
        # Undo button
        if self.game.phase == "shoot" and not self.game.game_over and not self.replay_mode:
            self.undo_button.config(state=tk.NORMAL)
        else:
            self.undo_button.config(state=tk.DISABLED)
        
        # Replay and Save Match buttons - enable when there are moves to replay/save
        has_moves = len([entry for entry in self.game.game_archive if entry['type'] in ['move', 'shot']]) > 0
        if has_moves and not self.replay_mode:
            self.replay_button.config(state=tk.NORMAL)
            self.save_match_button.config(state=tk.NORMAL)
        else:
            self.replay_button.config(state=tk.DISABLED)
            self.save_match_button.config(state=tk.DISABLED)
        
        # Load Match button - always enabled
        self.load_match_button.config(state=tk.NORMAL)
        
        # Replay controls
        if self.replay_mode:
            self.replay_frame.pack(fill=tk.X, pady=5)
            self.update_replay_controls()
        else:
            self.replay_frame.pack_forget()

    def has_game_started(self):
        """Check if the game has any moves recorded"""
        return len([entry for entry in self.game.game_archive if entry['type'] in ['move', 'shot']]) > 0
    
    def update_replay_controls(self):
        """Update replay control states"""
        total_actions = len(self.game.game_archive) - 1  # Exclude initial state
        
        # Update replay label with action type
        if self.replay_index < len(self.game.game_archive):
            current_action = self.game.game_archive[self.replay_index]
            action_type = current_action['type']
            player = current_action.get('player', '')
            
            if action_type == 'move':
                action_text = f"Player {player} Move"
            elif action_type == 'shot':
                action_text = f"Player {player} Shoot"
            elif action_type == 'initial':
                action_text = "Start"
            elif action_type == 'game_over':
                action_text = "Game Over"
            else:
                action_text = action_type.capitalize()
            
            # Show turn number for moves (each move starts a new turn)
            turn_number = current_action.get('turn_number', 0)
            if action_type == 'move':
                self.replay_label.config(text=f"{action_text} - Turn {turn_number} - Step {self.replay_index}/{total_actions}")
            else:
                self.replay_label.config(text=f"{action_text} - Step {self.replay_index}/{total_actions}")
        
        # Update button states
        self.prev_button.config(state=tk.NORMAL if self.replay_index > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.replay_index < total_actions else tk.DISABLED)
    
    def save_game(self):
        """Save the current game state to a file"""
        try:
            filename = "amazon_chess_save.pkl"
            game_state = self.game.get_board_state()
            with open(filename, 'wb') as f:
                pickle.dump(game_state, f)
            print(f"Game saved to {filename}")
            messagebox.showinfo("Game Saved", f"Game progress saved to {filename}")
        except Exception as e:
            print(f"Error saving game: {e}")
            messagebox.showerror("Save Error", f"Failed to save game: {e}")
    
    def load_game(self):
        """Load a game state from file"""
        try:
            filename = "amazon_chess_save.pkl"
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    game_state = pickle.load(f)
                self.game.set_board_state(game_state)
                self.available_moves = []
                self.available_shots = []
                self.replay_mode = False
                self.replay_index = 0
                self.replay_frame.pack_forget()
                self.draw_board()
                self.update_status()
                self.update_button_states()
                print(f"Game loaded from {filename}")
                messagebox.showinfo("Game Loaded", f"Game progress loaded from {filename}")
                
                # Check if game was over when saved
                if self.game.game_over:
                    self.show_game_over_dialog()
            else:
                messagebox.showwarning("Load Error", f"No saved game found at {filename}")
        except Exception as e:
            print(f"Error loading game: {e}")
            messagebox.showerror("Load Error", f"Failed to load game: {e}")
    
    def save_match(self):
        """Save the complete match archive to a file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"amazon_chess_match_{timestamp}.pkl"
            match_data = {
                'game_archive': self.game.game_archive,
                'timestamp': timestamp,
                'winner': self.game.winner
            }
            with open(filename, 'wb') as f:
                pickle.dump(match_data, f)
            print(f"Match saved to {filename}")
            messagebox.showinfo("Match Saved", f"Complete match saved to {filename}")
        except Exception as e:
            print(f"Error saving match: {e}")
            messagebox.showerror("Save Error", f"Failed to save match: {e}")

    def load_match(self):
        """Load a complete match from file and start replay"""
        try:
            filename = filedialog.askopenfilename(
                title="Load Match File",
                filetypes=[("Match files", "*.pkl"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'rb') as f:
                    match_data = pickle.load(f)
                
                # Set up replay mode
                self.game.set_game_archive(match_data['game_archive'])
                self.replay_mode = True
                self.replay_index = 0
                
                # Show first move
                self.game.replay_to_move(self.replay_index)
                self.draw_board()
                self.update_status()
                self.update_button_states()
                
                print(f"Match loaded from {filename}")
                messagebox.showinfo("Match Loaded", f"Match loaded from {filename}")
        except Exception as e:
            print(f"Error loading match: {e}")
            messagebox.showerror("Load Error", f"Failed to load match: {e}")
    
    def start_replay(self):
        """Start replaying the current game"""
        if len(self.game.game_archive) > 1:  # Need at least one move to replay
            self.replay_mode = True
            self.replay_index = 0
            self.game.replay_to_move(self.replay_index)
            self.draw_board()
            self.update_status()
            self.update_button_states()
    
    def previous_move(self):
        """Go to previous move in replay"""
        if self.replay_index > 0:
            self.replay_index -= 1
            self.game.replay_to_move(self.replay_index)
            self.draw_board()
            self.update_status()
            self.update_replay_controls()
    
    def next_move(self):
        """Go to next move in replay"""
        if self.replay_index < len(self.game.game_archive) - 1:
            self.replay_index += 1
            self.game.replay_to_move(self.replay_index)
            self.draw_board()
            self.update_status()
            self.update_replay_controls()
    
    def exit_replay(self):
        """Exit replay mode"""
        self.replay_mode = False
        # Restore the current game state (last state in archive)
        if self.game.game_archive:
            last_state = self.game.game_archive[-1]
            self.game.set_board_state({
                'board': last_state['board'],
                'current_player': last_state['player'],
                'selected_amazon': None,
                'moved_amazon': None,
                'phase': "select",
                'game_over': last_state['game_over'],
                'winner': last_state['winner'],
                'game_archive': self.game.game_archive
            })
        self.draw_board()
        self.update_status()
        self.update_button_states()
    
    def draw_board(self):
        """Draw the 10x10 game board with alternating colors and highlights"""
        self.canvas.delete("all")  # Clear canvas
        
        # Draw the grid squares and highlights
        for row in range(10):
            for col in range(10):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Determine base color (chess board pattern)
                if (row + col) % 2 == 0:
                    base_color = self.colors['light']
                else:
                    base_color = self.colors['dark']
                
                # Determine if this cell should be highlighted
                highlight_color = None
                if not self.replay_mode:
                    if self.game.phase == "move" and (row, col) in self.available_moves:
                        highlight_color = self.colors['move_highlight']  # Light yellow
                    elif self.game.phase == "shoot" and (row, col) in self.available_shots:
                        highlight_color = self.colors['shot_highlight']  # Light purple
                
                # Draw the base square
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, 
                    fill=base_color, 
                    outline='black', 
                    width=1,
                    tags=f"square_{row}_{col}"
                )
                
                # Draw highlight overlay if needed (semi-transparent effect)
                if highlight_color:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, 
                        fill=highlight_color, 
                        outline='black', 
                        width=1,
                        tags=f"highlight_{row}_{col}"
                    )
                
                # Draw pieces if present (on top of highlights)
                cell_content = self.game.board[row][col]
                if cell_content == 'A' or cell_content == 'B':
                    self.draw_amazon(row, col, cell_content)
                elif cell_content == 'X':
                    self.draw_arrow(row, col)
        
        # Draw selection borders on top of everything (only in active game)
        if not self.replay_mode:
            self.draw_selection_borders()
        
        # In replay mode, highlight the current action
        if self.replay_mode and self.replay_index < len(self.game.game_archive):
            current_action = self.game.game_archive[self.replay_index]
            if current_action['type'] == 'move' and current_action['end_pos']:
                # Highlight the destination of the move
                end_row, end_col = current_action['end_pos']
                self.draw_cell_border(end_row, end_col, '#FFD700', "replay_highlight")  # Gold for move destination
            elif current_action['type'] == 'shot' and current_action['arrow_pos']:
                # Highlight the arrow position
                arrow_row, arrow_col = current_action['arrow_pos']
                self.draw_cell_border(arrow_row, arrow_col, '#FF4500', "replay_highlight")  # Red for shot

    def draw_selection_borders(self):
        """Draw borders around selected Amazons (on top of everything)"""
        # Clear previous selection borders
        self.canvas.delete("selection_border")
        
        # Highlight selected Amazon if any
        if self.game.selected_amazon:
            row, col = self.game.selected_amazon
            self.draw_cell_border(row, col, self.colors['highlight'], "selection_border")
        
        # Highlight moved Amazon in shooting phase
        if self.game.phase == "shoot" and self.game.moved_amazon:
            row, col = self.game.moved_amazon
            self.draw_cell_border(row, col, self.colors['highlight'], "selection_border")
    
    def draw_amazon(self, row, col, player):
        """Draw an Amazon piece on the board"""
        x_center = col * self.cell_size + self.cell_size // 2
        y_center = row * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 3
        
        # Draw the piece (circle)
        fill_color = self.colors[player]
        outline_color = 'black' if player == 'A' else 'white'
        
        self.canvas.create_oval(
            x_center - radius, y_center - radius,
            x_center + radius, y_center + radius,
            fill=fill_color, outline=outline_color, width=2,
            tags=f"amazon_{row}_{col}"
        )
    
    def draw_arrow(self, row, col):
        """Draw an arrow as a deep blue circle (same size as Amazons)"""
        x_center = col * self.cell_size + self.cell_size // 2
        y_center = row * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 3  # Same size as Amazon pieces
        
        # Draw a deep blue circle to represent an arrow
        self.canvas.create_oval(
            x_center - radius, y_center - radius,
            x_center + radius, y_center + radius,
            fill='darkblue', outline='navy', width=2,
            tags=f"arrow_{row}_{col}"
        )
    
    def draw_cell_border(self, row, col, color, tag):
        """Draw a border around a specific cell"""
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=color,
            width=4,
            tags=tag
        )
    
    def setup_mouse_interaction(self):
        """Set up mouse click event binding for the game board"""
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        print("Mouse interaction system initialized")
    
    def on_canvas_click(self, event):
        """
        Handle mouse clicks on the game board
        Converts pixel coordinates to board coordinates
        """
        # Don't process clicks if game is over or in replay mode
        if self.game.game_over or self.replay_mode:
            return
            
        # Calculate which cell was clicked based on pixel coordinates
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        # Ensure coordinates are within board bounds
        if 0 <= row < 10 and 0 <= col < 10:
            print(f"Cell clicked: row={row}, col={col}, phase={self.game.phase}")
            
            if self.game.phase == "select":
                self.handle_selection_phase(row, col)
            elif self.game.phase == "move":
                self.handle_move_phase(row, col)
            elif self.game.phase == "shoot":
                self.handle_shoot_phase(row, col)
            
            # Update status display and button states
            self.update_status()
            self.update_button_states()
            
            # Check for game over after the move
            if self.game.game_over:
                self.show_game_over_dialog()
        else:
            print(f"Click outside board: x={event.x}, y={event.y}")
    
    def handle_selection_phase(self, row, col):
        """Handle clicks during the selection phase"""
        # Simple turn check
        if self.multiplayer_lobby.connected and not self.multiplayer_lobby.is_my_turn():
            print("Not your turn!")
            return
        
        clicked_piece = self.game.board[row][col]
        
        # Check if player clicked on their own Amazon
        if clicked_piece == self.game.current_player:
            self.game.selected_amazon = (row, col)
            self.available_moves = self.game.get_available_moves(row, col)
            
            # Send selection to opponent
            if self.multiplayer_lobby.connected:
                self.multiplayer_lobby.send_game_action("select_amazon", (row, col), (row, col), f"select_{int(time.time())}")
            
            if self.available_moves:
                self.game.phase = "move"
                print(f"Amazon selected at ({row}, {col})")
            else:
                print("Selected Amazon has no valid moves")
                self.game.selected_amazon = None
        
        self.draw_board()
        """Handle clicks during the selection phase"""
        # Simple turn check
        if self.multiplayer_lobby.connected and not self.multiplayer_lobby.is_my_turn():
            print("Not your turn!")
            return
        
        clicked_piece = self.game.board[row][col]
        
        # Check if player clicked on their own Amazon
        if clicked_piece == self.game.current_player:
            self.game.selected_amazon = (row, col)
            self.available_moves = self.game.get_available_moves(row, col)
            
            # Send selection to opponent
            if self.multiplayer_lobby.connected:
                self.multiplayer_lobby.send_game_action("select_amazon", (row, col), (row, col), f"select_{int(time.time())}")
            
            if self.available_moves:
                self.game.phase = "move"
                print(f"Amazon selected at ({row}, {col})")
            else:
                print("Selected Amazon has no valid moves")
                self.game.selected_amazon = None
        
        self.draw_board()
    
    def handle_move_phase(self, row, col):
        """Handle clicks during the move phase"""
        # Simple turn check
        if self.multiplayer_lobby.connected and not self.multiplayer_lobby.is_my_turn():
            print("Not your turn!")
            return
        
        if (row, col) in self.available_moves:
            success = self.game.move_amazon(self.game.selected_amazon, (row, col))
            if success:
                print(f"Amazon moved from {self.game.selected_amazon} to ({row}, {col})")
                
                # Send move to opponent
                if self.multiplayer_lobby.connected:
                    self.multiplayer_lobby.send_game_action("move_amazon", self.game.selected_amazon, (row, col), f"move_{int(time.time())}")
                
                self.available_shots = self.game.get_available_shots(row, col)
                
                # Send state update
                if self.multiplayer_lobby.connected:
                    self.multiplayer_lobby.send_game_state_update()
                
                if not self.available_shots:
                    print("No available shots - turn ends automatically")
                    self.game.complete_turn()
                    if self.multiplayer_lobby.connected:
                        self.multiplayer_lobby.send_game_state_update()
                    self.available_moves = []
                    self.available_shots = []
                else:
                    self.game.phase = "shoot"
            else:
                print("Move failed")
        else:
            print("Invalid move")
            
            if self.game.board[row][col] == self.game.current_player:
                self.game.selected_amazon = (row, col)
                self.available_moves = self.game.get_available_moves(row, col)
        
        self.draw_board()

    def handle_shoot_phase(self, row, col):
        """Handle clicks during the shoot phase"""
        # Simple turn check
        if self.multiplayer_lobby.connected and not self.multiplayer_lobby.is_my_turn():
            print("Not your turn!")
            return
        
        if (row, col) in self.available_shots:
            success = self.game.shoot_arrow(self.game.moved_amazon, (row, col))
            if success:
                print(f"Arrow shot to ({row}, {col})")
                
                # Send shot to opponent
                if self.multiplayer_lobby.connected:
                    self.multiplayer_lobby.send_game_action("shoot_arrow", self.game.moved_amazon, (row, col), f"shot_{int(time.time())}")
                
                # Complete turn locally
                self.game.complete_turn()
                
                # Send final state update WITH GAME OVER INFO
                if self.multiplayer_lobby.connected:
                    self.multiplayer_lobby.send_game_state_update()
                
                # CHECK FOR GAME OVER IMMEDIATELY
                if self.game.game_over:
                    self.show_game_over_dialog()
                    # Game over state is already sent in send_game_state_update
                
                self.available_moves = []
                self.available_shots = []
            else:
                print("Shot failed")
        else:
            print("Invalid shot - undoing move")
            success = self.game.undo_move()
            if success:
                if self.game.selected_amazon:
                    self.available_moves = self.game.get_available_moves(
                        self.game.selected_amazon[0], self.game.selected_amazon[1]
                    )
                self.available_shots = []
        
        self.draw_board()

    def update_status(self):
        """Update the status label based on current game state"""
        if self.replay_mode:
            if self.replay_index < len(self.game.game_archive):
                current_action = self.game.game_archive[self.replay_index]
                action_type = current_action['type']
                player_name = "Player A (White)" if current_action['player'] == 'A' else "Player B (Black)"
                
                if action_type == 'move':
                    status_text = f"REPLAY: {player_name} moves Amazon"
                elif action_type == 'shot':
                    status_text = f"REPLAY: {player_name} shoots arrow"
                elif action_type == 'initial':
                    status_text = "REPLAY: Initial board setup"
                elif action_type == 'game_over':
                    winner_name = "Player A (White)" if current_action['winner'] == 'A' else "Player B (Black)"
                    status_text = f"REPLAY: Game Over - {winner_name} wins!"
                else:
                    status_text = f"REPLAY: {action_type}"
                
                self.status_label.config(text=status_text)
        elif self.game.game_over:
            winner_name = "Player A (White)" if self.game.winner == 'A' else "Player B (Black)"
            self.status_label.config(text=f"Game Over! {winner_name} Wins!")
        else:
            player_name = "Player A (White)" if self.game.current_player == 'A' else "Player B (Black)"
            
            if self.game.phase == "select":
                status_text = f"{player_name}'s Turn - Select an Amazon"
            elif self.game.phase == "move":
                status_text = f"{player_name}'s Turn - Select destination for Amazon"
            elif self.game.phase == "shoot":
                status_text = f"{player_name}'s Turn - Shoot arrow from moved Amazon"
            else:
                status_text = f"{player_name}'s Turn"
            
            self.status_label.config(text=status_text)
    
    def show_game_over_dialog(self):
        """Show game over message - ensure buttons appear for both players"""
        # Only show if game is actually over and we haven't shown it recently
        if self.game.game_over and self.game.winner:
            # Use a simple flag to prevent multiple dialogs
            if not hasattr(self, '_game_over_shown') or not self._game_over_shown:
                self._game_over_shown = True
                winner_name = "Player A (White)" if self.game.winner == 'A' else "Player B (Black)"
                your_status = "You won!" if ((self.multiplayer_lobby.player_role == self.game.winner) if self.multiplayer_lobby.connected else True) else "You lost!"
                print(f"🎮 Game Over! Winner: {winner_name}")
                messagebox.showinfo("Game Over", f"{winner_name} wins the game!\n\n{your_status}")                
            
            # CRITICAL: Force update of button states to show post-game buttons
            self.update_button_states()
        else:
            # Reset the flag if game is not over
            self._game_over_shown = False

class SimpleMultiplayerLobby:
    """
    Simple lobby system for Amazon Chess
    Perfect for students playing with friends
    """
    
    def __init__(self, game_gui):
        self.game_gui = game_gui
        self.game = game_gui.game
        self.network_manager = None
        self.is_host = False
        self.connected = False
        self.player_role = None  # 'A' or 'B' - my role in the game
        
    def create_lobby_buttons(self, parent_frame):
        """Add multiplayer buttons to the main GUI"""
        multiplayer_frame = tk.Frame(parent_frame, bg='light gray')
        multiplayer_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(multiplayer_frame, text="Multiplayer:", 
                font=("Arial", 10, "bold"), bg='light gray').pack(side=tk.LEFT, padx=5)
        
        self.host_button = tk.Button(
            multiplayer_frame,
            text="Host Game",
            font=("Arial", 10),
            command=self.host_game,
            bg='#4ECDC4',
            width=10
        )
        self.host_button.pack(side=tk.LEFT, padx=2)
        
        self.join_button = tk.Button(
            multiplayer_frame,
            text="Join Game",
            font=("Arial", 10),
            command=self.join_game,
            bg='#45B7D1',
            width=10
        )
        self.join_button.pack(side=tk.LEFT, padx=2)
        
        # ADD DISCONNECT BUTTON
        self.disconnect_button = tk.Button(
            multiplayer_frame,
            text="Disconnect",
            font=("Arial", 10),
            command=self.disconnect,
            bg='#FF6B6B',
            width=10,
            state=tk.DISABLED  # Initially disabled
        )
        self.disconnect_button.pack(side=tk.LEFT, padx=2)
        
        self.connection_label = tk.Label(
            multiplayer_frame,
            text="Offline",
            font=("Arial", 9),
            bg='light gray',
            fg='red'
        )
        self.connection_label.pack(side=tk.RIGHT, padx=5)
        
        return multiplayer_frame
    
    def get_local_ip(self):
        """Get your local IP address to share with friends"""
        try:
            # Connect to a remote address to determine local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except:
            return "127.0.0.1"  # Fallback to localhost
    
    def host_game(self):
        """Start hosting a game"""
        try:
            if self.network_manager and self.connected:
                messagebox.showinfo("Already Connected", "You are already in a multiplayer game!")
                return
            
            # Create network manager as host
            from two_player_amazon_network import NetworkManager, NetworkRole
            self.network_manager = NetworkManager(NetworkRole.HOST, '0.0.0.0', 12345)
            self.setup_network_callbacks()
            self.network_manager.start()
            
            self.is_host = True
            self.update_connection_status("Waiting for player...", "orange")
            
            # Show IP address for friends to connect
            your_ip = self.get_local_ip()
            messagebox.showinfo(
                "Hosting Game", 
                f"Game is now hosting!\n\n"
                f"Your IP: {your_ip}\nPort: 12345\n\n"
                f"Share this with your friend to join."
            )
            
            self.disable_lobby_buttons()
            
        except Exception as e:
            messagebox.showerror("Host Error", f"Failed to host game: {e}")
    
    def join_game(self):
        """Join a friend's game"""
        try:
            if self.network_manager and self.connected:
                messagebox.showinfo("Already Connected", "You are already in a multiplayer game!")
                return
            
            # Ask for friend's IP
            friend_ip = simpledialog.askstring(
                "Join Game", 
                "Enter your friend's IP address:",
                initialvalue="localhost"
            )
            
            if not friend_ip:
                return  # User cancelled
                
            # Create network manager as client
            from two_player_amazon_network import NetworkManager, NetworkRole
            self.network_manager = NetworkManager(NetworkRole.CLIENT, friend_ip, 12345)
            self.setup_network_callbacks()
            self.network_manager.start()
            
            self.is_host = False
            self.update_connection_status("Connecting...", "orange")
            self.disable_lobby_buttons()
            
        except Exception as e:
            messagebox.showerror("Join Error", f"Failed to join game: {e}")
    
    def setup_network_callbacks(self):
        """Setup callbacks for network events"""
        if not self.network_manager:
            return
            
        self.network_manager.on_message_received = self.handle_network_message
        self.network_manager.on_connection_change = self.handle_connection_change
        self.network_manager.on_error = self.handle_network_error
    
    def handle_connection_change(self, connected, info):
        """Handle connection status changes"""
        if connected:
            self.connected = True
            player_role = "HOST" if self.is_host else "PLAYER"
            self.update_connection_status(f"Connected as {player_role}", "green")
            
            if self.is_host:
                # Host starts the game setup
                self.start_multiplayer_game()
            else:
                # Client waits for host to send initial state
                self.update_connection_status("Waiting for host...", "orange")
        
        else:
            self.connected = False
            self.update_connection_status("Disconnected", "red")
            self.enable_lobby_buttons()
    
    def handle_network_message(self, message):
        """Handle incoming network messages"""
        try:
            msg_type = message.get('type')
            data = message.get('data', {})
            
            print(f"📨 Received: {msg_type}")
            
            if msg_type == "game_action":
                self.handle_game_action(data)
            elif msg_type == "state_update":
                self.handle_state_update(data)
            elif msg_type == "chat_message":
                self.handle_chat_message(data)
            elif msg_type == "connection_status":
                self.handle_connection_status(data)
                
        except Exception as e:
            print(f"Error handling network message: {e}")
    
    def handle_network_error(self, error_msg):
        """Handle network errors"""
        messagebox.showerror("Network Error", error_msg)
        self.update_connection_status("Error", "red")
        self.enable_lobby_buttons()
    
    def update_connection_status(self, status, color):
        """Update the connection status label and disconnect button"""
        if hasattr(self, 'connection_label'):
            self.connection_label.config(text=status, fg=color)
        
        # Update disconnect button state
        if hasattr(self, 'disconnect_button'):
            if self.connected:
                self.disconnect_button.config(state=tk.NORMAL)
            else:
                self.disconnect_button.config(state=tk.DISABLED)
    
    def disconnect(self):
        """Disconnect from multiplayer game"""
        if self.network_manager:
            self.network_manager.stop()
        self.connected = False
        self.is_host = False
        self.player_role = None
        self.update_connection_status("Offline", "red")
        self.enable_lobby_buttons()
        
        # Show disconnect message
        messagebox.showinfo("Disconnected", "You have disconnected from the multiplayer game.")
    
    def disable_lobby_buttons(self):
        """Disable lobby buttons when connected"""
        self.host_button.config(state=tk.DISABLED)
        self.join_button.config(state=tk.DISABLED)
    
    def enable_lobby_buttons(self):
        """Enable lobby buttons when disconnected"""
        self.host_button.config(state=tk.NORMAL)
        self.join_button.config(state=tk.NORMAL)
    
    def start_multiplayer_game(self):
        """Initialize multiplayer game session - Host chooses who goes first"""
        if self.is_host:
            choice = messagebox.askquestion(
                "Choose Starting Player", 
                "Do you want to play first (White)?\n\nYes = You play first as White\nNo = Opponent plays first as White"
            )
            host_plays_first = (choice == 'yes')
            
            # Send initial game state to client
            self.send_initial_game_state(host_plays_first)
        else:
            # Client waits for host to send initial state
            print("🔄 Waiting for host to send initial game state...")
    
    def send_initial_game_state(self, host_plays_first):
        """Send initial game state to client"""
        from two_player_amazon_network import MessageType
        
        initial_state = {
            'host_plays_first': host_plays_first,
            'board': [row[:] for row in self.game.board],  # Deep copy
            'current_player': 'A'  # A always starts
        }
        
        state_msg = {
            'type': MessageType.STATE_UPDATE.value,
            'timestamp': time.time(),
            'data': initial_state
        }
        
        self.network_manager.send_message(MessageType.STATE_UPDATE, state_msg['data'])
        
        # Set up local game state
        self.setup_local_game_state(host_plays_first)
    
    def setup_local_game_state(self, host_plays_first):
        """Set up local game state based on host's choice"""
        # Reset game to clean state
        self.game.reset_game()
        
        # A always starts the game
        self.game.current_player = 'A'
        
        # Set player info for display
        if self.is_host:
            self.player_role = 'A' if host_plays_first else 'B'
            player_info = f"You play as {'White (A)' if host_plays_first else 'Black (B)'}"
        else:
            self.player_role = 'B' if host_plays_first else 'A' 
            player_info = f"You play as {'Black (B)' if host_plays_first else 'White (A)'}"
        
        self.game_gui.update_status()
        messagebox.showinfo("Game Started", f"{player_info}\n\nPlayer A (White) always starts first.")
    
    def is_my_turn(self):
        """Simple check: can I move right now?"""
        if not self.connected:
            return True
        
        # I can move if it's my color's turn
        return self.game.current_player == self.player_role
    
    def send_game_action(self, action, from_pos, to_pos, move_id):
        """Send game action to opponent"""
        if self.network_manager and self.connected:
            from two_player_amazon_network import MessageType, create_game_action_message
            
            message = create_game_action_message(
                action, self.game.current_player, from_pos, to_pos, move_id
            )
            self.network_manager.send_message(MessageType.GAME_ACTION, message['data'])
    
    def send_game_state_update(self):
        """Send current game state to opponent"""
        if self.connected:
            from two_player_amazon_network import create_state_update_message, MessageType
            
            # Send complete board state
            changes = []
            for row in range(10):
                for col in range(10):
                    if self.game.board[row][col] is not None:
                        changes.append({
                            "position": [row, col],
                            "to": self.game.board[row][col]
                        })
            
            state_update = create_state_update_message(
                changes,
                self.game.current_player,
                self.game.phase,
                self.game.get_turn_count(),
                self.game.game_over,  # ADD THIS: Include game over status
                self.game.winner      # ADD THIS: Include winner
            )
            self.network_manager.send_message(MessageType.STATE_UPDATE, state_update['data'])
            print(f"📤 Sent complete board state update (game_over: {self.game.game_over}, winner: {self.game.winner})")
    
    def get_board_changes(self):
        """Get current board state as changes"""
        # For simplicity, send key positions
        changes = []
        for row in range(10):
            for col in range(10):
                if self.game.board[row][col] is not None:
                    changes.append({
                        "position": [row, col],
                        "to": self.game.board[row][col]
                    })
        return changes
    
    def handle_game_action(self, action_data):
        """Handle game actions from opponent - JUST FOR VISUAL FEEDBACK, NOT STATE CHANGES"""
        try:
            action = action_data.get('action')
            player = action_data.get('player')
            from_pos = action_data.get('from')
            to_pos = action_data.get('to')
            move_id = action_data.get('move_id')
            
            print(f"🎮 Received opponent action: {action} from {player}")
            
            # ✅ 关键修复：在接收到对手动作时立即记录到archive
            if action == "move_amazon":
                # 记录对手的移动动作
                self.game._record_in_archive('move', from_pos, to_pos, None)
                print(f"📝 Recorded opponent move in archive: {from_pos} → {to_pos} (as {player})")
            elif action == "shoot_arrow":
                # 记录对手的射击动作
                # 注意：这里from_pos是射箭的起始位置（即移动后的位置）
                self.game._record_in_archive('shot', from_pos, None, to_pos)
                print(f"📝 Recorded opponent shot in archive: {from_pos} → {to_pos} (as {player})")
            # DON'T apply the move here - it will be handled by state updates
            # Just update visual feedback if needed
            
            if action == "select_amazon":
                # Just show opponent's selection visually
                self.game.selected_amazon = from_pos
                self.game.phase = "move"
                # Get available moves for visualization only
                self.game_gui.available_moves = self.game.get_available_moves(from_pos[0], from_pos[1])
                
            elif action == "move_amazon":
                # Just show opponent's move visually
                self.game.selected_amazon = from_pos
                self.game.moved_amazon = to_pos
                self.game.phase = "shoot"
                # Get available shots for visualization only
                self.game_gui.available_shots = self.game.get_available_shots(to_pos[0], to_pos[1])
                print(f"👀 Showing opponent move: {from_pos} → {to_pos}")
                
            elif action == "shoot_arrow":
                # Just show opponent's shot visually
                self.game.phase = "select"
                print(f"👀 Showing opponent shot at {to_pos}")
            
            # Update the GUI for visual feedback only
            self.game_gui.draw_board()
            self.game_gui.update_status()
            
        except Exception as e:
            print(f"Error handling game action: {e}")

    def handle_state_update(self, state_data):
        """Handle state updates from opponent"""
        try:
            # If this is an initial state (from host)
            if 'host_plays_first' in state_data:
                host_plays_first = state_data['host_plays_first']
                board = state_data['board']
                current_player = state_data['current_player']
                # Set up local game state
                self.setup_local_game_state(host_plays_first)
                # Apply the board state
                self.game.board = [row[:] for row in board]  # Deep copy
                self.game.current_player = current_player
                self.game_gui.draw_board()
                self.game_gui.update_status()
                return
    
            # Otherwise, it's a normal state update
            changes = state_data.get('changes', [])
            current_player = state_data.get('current_player')
            phase = state_data.get('phase')
            game_over = state_data.get('game_over', False)
            winner = state_data.get('winner', None)
    
            # Apply board changes - CLEAR THE BOARD FIRST to avoid duplicates
            temp_board = [[None for _ in range(10)] for _ in range(10)]
            for change in changes:
                pos = change.get('position')
                to_val = change.get('to')
                if pos and len(pos) == 2:
                    temp_board[pos[0]][pos[1]] = to_val
            
            # Replace the entire board
            self.game.board = temp_board
    
            # Update game state
            if current_player:
                self.game.current_player = current_player
            if phase:
                self.game.phase = phase
            
            # UPDATE GAME OVER STATUS
            self.game.game_over = game_over
            self.game.winner = winner
    
            # CRITICAL: Record opponent's moves in archive
            # Only record if it's NOT our turn (meaning opponent moved)
            if not self.is_my_turn():
                # Determine what type of action this represents
                arrow_positions = [change.get('position') for change in changes if change.get('to') == 'X']
                amazon_moves = [change for change in changes if change.get('to') in ['A', 'B']]
                
                if arrow_positions:
                    # This was a shot action
                    # Correctly match amazon moves with arrow positions in order
                    if len(amazon_moves) != len(arrow_positions):
                        print(f"Mismatched number of amazon moves ({len(amazon_moves)}) and arrow positions ({len(arrow_positions)})")
                    
                    # Match in order (one amazon move per arrow position)
                    for i in range(min(len(amazon_moves), len(arrow_positions))):
                        amazon_move = amazon_moves[i]
                        arrow_pos = arrow_positions[i]
                        from_pos = amazon_move.get('position')
                        #self.game._record_in_archive('shot', from_pos, None, arrow_pos)
                        #print(f"📝 Recorded opponent shot in archive: {from_pos} -> {arrow_pos}")
                
                elif amazon_moves and len(amazon_moves) >= 2:
                    # This was a move action (from->None and to->player)
                    from_change = None
                    to_change = None
                    for change in changes:
                        if change.get('to') is None and change.get('from') in ['A', 'B']:
                            from_change = change
                        elif change.get('to') in ['A', 'B'] and change.get('from') is None:
                            to_change = change
                    
                    if from_change and to_change:
                        self.game._record_in_archive('move', from_change.get('position'), to_change.get('position'), None)
                        print(f"📝 Recorded opponent move in archive: {from_change.get('position')} -> {to_change.get('position')}")
            
            # Clear UI state
            self.game.selected_amazon = None
            self.game.moved_amazon = None
            self.game_gui.available_moves = []
            self.game_gui.available_shots = []
            self.game_gui.draw_board()
            self.game_gui.update_status()
    
            # SHOW GAME OVER DIALOG IF GAME ENDED
            if game_over and winner:
                self.game_gui.show_game_over_dialog()
                # 更新游戏状态
                self.game.game_over = True
                self.game.winner = winner
                # 记录 Game Over 状态
                self.game._record_in_archive('game_over', None, None, None)
                
        except Exception as e:
            print(f"Error applying state update: {e}")

    def handle_connection_status(self, status_data):
        """Handle connection status messages"""
        # Currently not used, but kept for future extensions
        pass
    
    def handle_chat_message(self, chat_data):
        """Handle chat messages"""
        player = chat_data.get('player', 'Opponent')
        message = chat_data.get('message', '')
        print(f"💬 {player}: {message}")
    
    def disconnect(self):
        """Disconnect from multiplayer game"""
        if self.network_manager:
            self.network_manager.stop()
        self.connected = False
        self.is_host = False
        self.player_role = None
        self.update_connection_status("Offline", "red")
        self.enable_lobby_buttons()

def main():
    """Main function to start the application"""
    root = tk.Tk()
    game = AmazonChess()
    gui = AmazonChessGUI(root, game)
    root.mainloop()


# Start the application
if __name__ == "__main__":
    main()
