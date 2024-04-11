import chess
import chess.engine

class ChessAlgoLogger:
    def __init__(self):
        # Initialises lists to keep track of moves by white and black.
        self.white_moves = []
        self.black_moves = []

        # Initialises dictionaries to log captured pieces by color.
        self.captured_pieces_per_game = {'WHITE':[], 'BLACK':[]}
        self.captured_pieces_sum = {'WHITE': {'P': 0, 'N': 0, 'B': 0, 'R': 0, 'Q': 0},
                                    'BLACK': {'p': 0, 'n': 0, 'b': 0, 'r': 0, 'q': 0}}
        
        # Initialises counters for games and moves
        self.total_games = 0
        self.total_moves = 0

        # Dictionary to keep track of game results.
        self.results = {"WHITE": 0, "BLACK": 0, "DRAW": 0}

        # List to keep track of the duration of each game.
        self.game_durations = []

    # Logs the move made by the player whose turn it is.
    def log_move(self, move, turn):
        if turn == chess.WHITE:
            self.white_moves.append(str(move))
        else:
            self.black_moves.append(str(move))

    # Logs captures by checking if a move is a capture, then logging the piece.
    def log_capture(self, board, move):
        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                capturing_color = 'WHITE' if captured_piece.color == chess.WHITE else 'BLACK'
                self.captured_pieces_per_game[capturing_color].append(captured_piece.symbol())
                self.captured_pieces_sum[capturing_color][captured_piece.symbol()] += 1

    # Increments the game count and logs the result of the game.
    def log_game_result(self, result, game_time):
        self.total_games += 1
        self.game_durations.append(game_time)
        if result == "white win":
            self.results["WHITE"] += 1
        elif result == "black win":
            self.results["BLACK"] += 1
        else:
            self.results["DRAW"] += 1

    # Outputs a summary of the game including moves and captures.

    def summarise_game(self):
        print("White Moves:", " ".join(self.white_moves))
        print("Black Moves:", " ".join(self.black_moves))
        print("Total Game moves:", len(self.black_moves) + len(self.white_moves))
        print("White Game moves:", len(self.white_moves))
        print("Black Game moves:", len(self.black_moves))
        self.total_moves += (len(self.black_moves) + len(self.white_moves))
        for color, pieces in self.captured_pieces_per_game.items():
            print(f"{color}(captured by the other side): {' '.join(pieces)}")

        # Resets lists for the next game.
        self.captured_pieces_per_game = {'WHITE':[], 'BLACK':[]}
        self.white_moves = []
        self.black_moves = []
        
    # Prints overall statistics including average durations and moves.
    def print_stats(self):

        if self.game_durations: 
            average_time = sum(self.game_durations) / len(self.game_durations) 
        else:
            average_time = 0
            
        if self.total_games > 0:
            average_moves = self.total_moves/self.total_games
        else:
            average_moves = 0

        print("\nStatistics:")
        print("Total games:", self.total_games)
        for color, count in self.results.items():
            print(f"{color} Wins: {count}")
        print(f"Average game duration per game: {average_time:.2f} seconds")
        print(f"Average moves per game: {average_moves:.2f}")
        for color, pieces in self.captured_pieces_sum.items():
            print(f"{color}'s captured pieces (captured by the other side):")
            for piece, count in pieces.items():
                print(f"  {piece}: {count}")
