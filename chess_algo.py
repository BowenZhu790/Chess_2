# import python-chess library
import chess
import chess.engine
import random

# path_to_stockfish = "D:\stockfish\stockfish\stockfish-windows-x86-64-avx2.exe"
# engine = chess.engine.SimpleEngine.popen_uci(path_to_stockfish)

# engine.configure({"Skill Level": 5})

board = chess.Board()
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

    # return the estimate value
    return pawn_value + knight_value + bishop_value + rook_value + queen_value

def minimax(board, depth):
    # board = chess.Board()
    if depth == 0:
        return evaluate_board(board)

    if board.turn:
        max_value = -9999999
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1)
            board.pop()
            max_value = max(max_value, eval)
        return max_value
    else:
        min_value = 9999999
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1)
            board.pop()
            min_value = max(min_value, eval)
        return min_value


def minimax_algorithm_move(board):
    # board = chess.Board()

    best_move = None
    best_value = -9999999

    for move in board.legal_moves:
        board.push(move)
        move_value = minimax(board, 2)
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
    path_to_stockfish = "D:\stockfish\stockfish\stockfish-windows-x86-64-avx2.exe"
    engine = chess.engine.SimpleEngine.popen_uci(path_to_stockfish)
    engine.configure({"Skill Level": 0})
    game_round = 0
    while not board.is_game_over():
        game_round += 1

        if board.turn:
            move = minimax_algorithm_move(board)
        else:
            move = stock_fish_move(board, engine)

        # move = minimax_algorithm_move(board)
    
        board.push(move)
        print(board, "\n")

    if board.is_checkmate():
        result = "white win" if board.turn == chess.BLACK else "black win"
    elif board.is_stalemate():
        result = "stale mate"
    elif board.is_insufficient_material():
        result = "insufficient material"
    elif board.is_seventyfive_moves() or board.is_fivefold_repetition():
        result = "seventyfive_moves or fivefold_repetition"

    print("Game end! Results:", result)
    print("Game round:", game_round)
    engine.quit()

main()

    
