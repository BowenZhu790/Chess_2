import chess
import chess.engine

class ChessAlgoLogger:
    def __init__(self):
        self.white_moves = []
        self.black_moves = []
        self.captured_pieces = {'WHITE':[], 'BLACK':[]}

    def log_move(self, move, turn):
        if turn == chess.WHITE:
            self.white_moves.append(str(move))
        else:
            self.black_moves.append(str(move))

    def log_capture(self, board, move):
        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                color = 'WHITE' if captured_piece.color == chess.WHITE else 'BLACK'
                self.captured_pieces[color].append(captured_piece.symbol())

    def summarize_game(self):
        print("White Moves:", " ".join(self.white_moves))
        print("Black Moves:", " ".join(self.black_moves))
        print("Total Game rounds:", len(self.black_moves) + len(self.white_moves))
        print("White Game rounds:", len(self.white_moves))
        print("Black Game rounds:", len(self.black_moves))
        print("Captured Pieces:")
        for color, pieces in self.captured_pieces.items():
            print(f"{color}: {' '.join(pieces)}")
