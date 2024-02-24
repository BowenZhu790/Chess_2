# import python-chess library
import chess
import chess.engine
import random

from chess_algo_logger import ChessAlgoLogger
# path_to_stockfish = "D:\stockfish\stockfish\stockfish-windows-x86-64-avx2.exe"
# engine = chess.engine.SimpleEngine.popen_uci(path_to_stockfish)

# engine.configure({"Skill Level": 5})

board = chess.Board()

pawn_square_table = [
    0,   0,   0,   0,   0,   0,  0,   0,
    5,  10,  10, -20, -20,  10, 10,   5,
    5,  -5, -10,   0,   0, -10, -5,   5,
    0,   0,   0,  20,  20,   0,  0,   0,
    5,   5,  10,  25,  25,  10,  5,   5,
    10, 10,  20,  30,  30,  20, 10,  10,
    50, 50,  50,  50,  50,  50, 50,  50,
    0,   0,   0,   0,   0,   0,  0,   0
]

knight_square_table = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,  0,   5,   5,   0,  -20, -40,
    -30,  5,  10,  15,  15,  10,   5,  -30,
    -30,  0,  15,  20,  20,  15,   0,  -30,
    -30,  5,  15,  20,  20,  15,   5,  -30,
    -30,  0,  10,  15,  15,  10,   0,  -30,
    -40, -20,  0,   0,   0,   0,  -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
]

bishop_square_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,  5,   0,   0,   0,   0,   5,  -10,
    -10, 10,  10,  10,  10,  10,  10, -10,
    -10,  0,  10,  10,  10,  10,   0, -10,
    -10,  5,   5,  10,  10,   5,   5, -10,
    -10,  0,   5,  10,  10,   5,   0, -10,
    -10,  0,   0,   0,   0,   0,   0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
]

rook_square_table = [
    0,  0,  0,  5,  5,  0,  0,  0,
    -5, 0,  0,  0,  0,  0,  0, -5,
    -5, 0,  0,  0,  0,  0,  0, -5,
    -5, 0,  0,  0,  0,  0,  0, -5,
    -5, 0,  0,  0,  0,  0,  0, -5,
    -5, 0,  0,  0,  0,  0,  0, -5,
    5, 10, 10, 10, 10, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0,
]

queen_square_table = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0,   0,   0,  0,   0,   0,  -10,
    -10, 0,   5,   5,  5,   5,   0,  -10,
     0,   0,   5,   5,  5,   5,   0,   -5,
    -5,   0,   5,   5,  5,   5,   0,   -5,
    -10,  0,   5,   5,  5,   5,   0,  -10,
    -10,  0,   0,   0,  0,   0,   0,  -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]


def evaluate_board(board):
    # board = chess.Board()

    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    
    # Calculate estimate utitliy for each type of pieces
    white_pawn = len(board.pieces(chess.PAWN, chess.WHITE))
    white_knight = len(board.pieces(chess.KNIGHT, chess.WHITE))
    white_bishop = len(board.pieces(chess.BISHOP, chess.WHITE))
    white_rook = len(board.pieces(chess.ROOK, chess.WHITE))
    white_queen = len(board.pieces(chess.QUEEN, chess.WHITE))

    black_pawn = len(board.pieces(chess.PAWN, chess.BLACK))
    black_knight = len(board.pieces(chess.KNIGHT, chess.BLACK))
    black_bishop = len(board.pieces(chess.BISHOP, chess.BLACK))
    black_rook = len(board.pieces(chess.ROOK, chess.BLACK))
    black_queen = len(board.pieces(chess.QUEEN, chess.BLACK))

    pawn_value = 100 * (white_pawn - black_pawn)
    knight_value = 300 * (white_knight - black_knight)
    bishop_value = 300 * (white_bishop - black_bishop)
    rook_value = 500 * (white_rook - black_rook)
    queen_value = 900 * (white_queen - black_queen)

    white_pawn_score = sum(pawn_square_table[i] for i in board.pieces(chess.PAWN, chess.WHITE))
    black_pawn_score = sum(-pawn_square_table[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK))

    white_knight_score = sum(knight_square_table[i] for i in board.pieces(chess.KNIGHT, chess.WHITE))
    black_knight_score = sum(-knight_square_table[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK))

    white_bishop_score = sum(bishop_square_table[i] for i in board.pieces(chess.BISHOP, chess.WHITE))
    black_bishop_score = sum(-bishop_square_table[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK))

    white_rook_score = sum(rook_square_table[i] for i in board.pieces(chess.ROOK, chess.WHITE))
    black_rook_score = sum(-rook_square_table[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK))

    white_queen_score = sum(queen_square_table[i] for i in board.pieces(chess.QUEEN, chess.WHITE))
    black_queen_score = sum(-queen_square_table[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK))

    # return the estimate value
    return pawn_value + knight_value + bishop_value + rook_value + queen_value + white_pawn_score + black_pawn_score + white_knight_score + black_knight_score + white_bishop_score + black_bishop_score + white_rook_score + black_rook_score + white_queen_score + black_queen_score

def minimax(board, depth, is_maximising_player, alpha, beta):
    # board = chess.Board()
    if depth == 0:
        return evaluate_board(board)

    if is_maximising_player:
        max_value = -9999999
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, False, alpha, beta)
            board.pop()
            max_value = max(max_value, eval)
            alpha = max(alpha, max_value)
            if alpha >= beta:
                break
        return max_value
    else:
        min_value = 9999999
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, True, alpha, beta)
            board.pop()
            min_value = min(min_value, eval)
            beta = min(beta, min_value)
            if alpha >= beta:
                break
        return min_value


def minimax_algorithm_move(board):
    # board = chess.Board()

    best_move = None
    best_value = -9999999

    for move in board.legal_moves:
        board.push(move)
        move_value = minimax(board, 2, True, -9999999, 9999999)
        board.pop()

        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move

    # if board.legal_moves:
    #     return random.choice(list(board.legal_moves))
        
    
    

def stock_fish_move(board, engine):
    result = engine.play(board, chess.engine.Limit(time=0.1))
    return result.move

def main():
    board = chess.Board()
    chess_logger = ChessAlgoLogger()

    path_to_stockfish = "D:\stockfish\stockfish\stockfish-windows-x86-64-avx2.exe"
    engine = chess.engine.SimpleEngine.popen_uci(path_to_stockfish)
    engine.configure({"Skill Level": 0})
    while not board.is_game_over():

        # down white, up black
        if board.turn:
            move = minimax_algorithm_move(board)
        else:
            move = stock_fish_move(board, engine)
            # move = random.choice(list(board.legal_moves))
            # move = minimax_algorithm_move(board)
        
        chess_logger.log_move(move, board.turn)
        chess_logger.log_capture(board, move)
    
        board.push(move)
        print(board, "\n")
    
    chess_logger.summarize_game()

    if board.is_checkmate():
        result = "white win" if board.turn == chess.BLACK else "black win"
    elif board.is_stalemate():
        result = "stale mate"
    elif board.is_insufficient_material():
        result = "insufficient material"
    elif board.is_seventyfive_moves() or board.is_fivefold_repetition():
        result = "seventyfive_moves or fivefold_repetition"

        

    print("Game end! Results:", result)
    engine.quit()

main()

    
