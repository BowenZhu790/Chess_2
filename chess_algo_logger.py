import chess
import chess.engine

# class ChessAlgoLogger:
#     def __init__(self):
#         self.white_moves = []
#         self.black_moves = []
#         self.captured_pieces = {'WHITE':[], 'BLACK':[]}

#     def log_move(self, move, turn):
#         if turn == chess.WHITE:
#             self.white_moves.append(str(move))
#         else:
#             self.black_moves.append(str(move))

#     def log_capture(self, board, move):
#         if board.is_capture(move):
#             captured_piece = board.piece_at(move.to_square)
#             if captured_piece:
#                 color = 'WHITE' if captured_piece.color == chess.WHITE else 'BLACK'
#                 self.captured_pieces[color].append(captured_piece.symbol())

#     def summarize_game(self):
#         print("White Moves:", " ".join(self.white_moves))
#         print("Black Moves:", " ".join(self.black_moves))
#         print("Total Game rounds:", len(self.black_moves) + len(self.white_moves))
#         print("White Game rounds:", len(self.white_moves))
#         print("Black Game rounds:", len(self.black_moves))
#         print("Captured Pieces:")
#         for color, pieces in self.captured_pieces.items():
#             print(f"{color}: {' '.join(pieces)}")

import chess
import chess.engine

class ChessAlgoLogger:
    def __init__(self):
        self.white_moves = []
        self.black_moves = []
        self.captured_pieces_per_game = {'WHITE':[], 'BLACK':[]}
        self.captured_pieces_sum = {'WHITE': {'P': 0, 'N': 0, 'B': 0, 'R': 0, 'Q': 0},
                                'BLACK': {'p': 0, 'n': 0, 'b': 0, 'r': 0, 'q': 0}}
        self.total_games = 0
        self.total_moves = 0
        self.wins = {"WHITE": 0, "BLACK": 0, "DRAW": 0}
        self.game_durations = []

    def log_move(self, move, turn):
        if turn == chess.WHITE:
            self.white_moves.append(str(move))
        else:
            self.black_moves.append(str(move))

    # def log_capture(self, board, move):
    #     if board.is_capture(move):
    #         captured_piece = board.piece_at(move.to_square)
    #         if captured_piece:
    #             color = 'WHITE' if captured_piece.color == chess.BLACK else 'BLACK'  # 注意反转颜色
    #             self.captured_pieces[color][captured_piece.symbol().upper()] += 1

    def log_capture(self, board, move):
        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                capturing_color = 'WHITE' if captured_piece.color == chess.WHITE else 'BLACK'
                self.captured_pieces_per_game[capturing_color].append(captured_piece.symbol())
                self.captured_pieces_sum[capturing_color][captured_piece.symbol()] += 1

    def log_game_result(self, result, game_time):
        self.total_games += 1
        self.game_durations.append(game_time)
        if result == "white win":
            self.wins["WHITE"] += 1
        elif result == "black win":
            self.wins["BLACK"] += 1
        else:
            self.wins["DRAW"] += 1

    def summarise_game(self):
        print("White Moves:", " ".join(self.white_moves))
        print("Black Moves:", " ".join(self.black_moves))
        print("Total Game moves:", len(self.black_moves) + len(self.white_moves))
        print("White Game moves:", len(self.white_moves))
        print("Black Game moves:", len(self.black_moves))
        self.total_moves += (len(self.black_moves) + len(self.white_moves))
        for color, pieces in self.captured_pieces_per_game.items():
            print(f"{color}: {' '.join(pieces)}")

        self.captured_pieces_per_game = {'WHITE':[], 'BLACK':[]}
        self.white_moves = []
        self.black_moves = []
        

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
        for color, count in self.wins.items():
            print(f"{color} Wins: {count}")
        print(f"Average game duration per game: {average_time:.2f} seconds")
        print(f"Average moves per game: {average_moves:.2f}")
        for color, pieces in self.captured_pieces_sum.items():
            print(f"{color}'s captured pieces:")
            for piece, count in pieces.items():
                print(f"  {piece}: {count}")
