import chess
import chess.engine
import random
import time
from chess_algo_logger import ChessAlgoLogger
from multiprocessing import Pool

# Piece square tables for pawn, knight, bishop, rook and queen.
# The king has three distinct tables, each map to open, middle and ending phase.
pawn_square_table = [
    0, 0, 0, 0, 0, 0, 0, 0,  
    5, 10, 10, -20, -20, 10, 10, 5,  
    5, -5, -10, 0, 0, -10, -5, 5,   
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5, 
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0    
]

knight_square_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 5, 10, 15, 15, 10, 5, -10,
    -10, 5, 15, 20, 20, 15, 5, -10,
    -10, 5, 15, 20, 20, 15, 5, -10,
    -10, 5, 10, 15, 15, 10, 5, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

bishop_square_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

rook_square_table = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]

queen_square_table = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

king_square_table_opening = [
    -35, -30, -40, -50, -50, -40, -30, -35,
    -35, -30, -40, -50, -50, -40, -30, -35,
    -35, -35, -40, -50, -50, -40, -35, -35,
    -35, -40, -40, -50, -50, -40, -40, -35,
    -35, -40, -40, -50, -50, -40, -40, -35,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 30, 10, 0, 0, 10, 30, 20
]

king_square_table_middlegame = [
    -35, -30, -40, -50, -50, -40, -30, -35,
    -35, -30, -40, -50, -50, -40, -30, -35,
    -35, -35, -40, -50, -50, -40, -35, -35,
    -35, -40, -40, -50, -50, -40, -40, -35,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20, 0, 0, 0, 0, 20, 20,
    20, 30, 10, 0, 0, 10, 30, 20
]

king_square_table_endgame = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -30, 0, 0, 0, 0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50
]

# Maps rach game phase to its corresponding king square value
king_square_tables = {
    "Opening": king_square_table_opening,
    "Middlegame": king_square_table_middlegame,
    "Endgame": king_square_table_endgame
}

# Defines the material value of each piece type
piece_material_scores = {
        chess.PAWN: 10, 
        chess.KNIGHT: 30, 
        chess.BISHOP: 33, 
        chess.ROOK: 50, 
        chess.QUEEN: 90, 
    }

# Path to the Stockfish chess engine executable
path_to_stockfish = "path_to_stockfish"

# Calculates and returns the total material score for the given board position
# This considers the material score for both players
def calculate_piece_material_score(board, minimax_colour, opponent_colour):
    minimax_material_score = 0
    opponent_material_score = 0
    for piece_type, piece_value in piece_material_scores.items():
        minimax_pieces = board.pieces(piece_type, minimax_colour)
        opponent_pieces = board.pieces(piece_type, opponent_colour)

        minimax_material_score += piece_value * len(minimax_pieces)
        opponent_material_score += piece_value * len(opponent_pieces)

    material_score = minimax_material_score - opponent_material_score

    return material_score

# Determines the current phase of the game (opening, middlegame, endgame) based on the pieces on the board
def determine_game_phase(board):
    num_pieces = len(board.piece_map())
    high_value_pieces = len(board.pieces(chess.QUEEN, chess.WHITE)) + len(board.pieces(chess.QUEEN, chess.BLACK)) + len(board.pieces(chess.ROOK, chess.WHITE)) + len(board.pieces(chess.ROOK, chess.BLACK))

    # Initially there are 32 pieces
    # Number of moves is not a bery good sign of game phase
    if num_pieces >= 30:
        return "Opening"
    elif num_pieces < 26 or high_value_pieces < 4:
        return "Endgame"
    else:
        return "Middlegame"

# Calculates the positional score for the given board position
# This considers the piece square tables for both players
def calculate_piece_square_table_score(board, minimax_colour, opponent_colour):
    minimax_piece_square_table_score = 0
    opponent_piece_square_table_score = 0

    # Piece square tables did not initialise as global values because changing tables of the king might affects the multiprocessing behaviour
    piece_square_tables = {
        chess.PAWN: pawn_square_table,
        chess.KNIGHT: knight_square_table,
        chess.BISHOP: bishop_square_table,
        chess.ROOK: rook_square_table,
        chess.QUEEN: queen_square_table,
        chess.KING: None
    }
    
    game_phase = determine_game_phase(board)
    current_king_square_table = king_square_tables[game_phase]

    piece_square_tables[chess.KING] = current_king_square_table


    for piece_type, piece_square_table in piece_square_tables.items():
        minimax_pieces = board.pieces(piece_type, minimax_colour)
        opponent_pieces = board.pieces(piece_type, opponent_colour)

        for square in minimax_pieces:
            # Since minimax is alwasy the maximising player, therefore the square table needs to be mirror when minimax plays black
            if minimax_colour == chess.BLACK:
                square = chess.square_mirror(square)
            minimax_piece_square_table_score += piece_square_table[square]

        for square in opponent_pieces:
            if minimax_colour == chess.WHITE:
                square = chess.square_mirror(square)
            opponent_piece_square_table_score += piece_square_table[square]

    piece_square_table_score = minimax_piece_square_table_score - opponent_piece_square_table_score

    return piece_square_table_score

# Calculates and returns a mobility score based on the number and quality of legal moves available
def calculate_mobility(board, minimax_colour):
    piece_mobility_score = 0
    piece_mobility_score += len(list(board.legal_moves)) * 4

    for move in board.legal_moves:

        if move.promotion is not None:
            # Adjust score based on the promotion type
            piece_mobility_score += 90

        capture = board.is_capture(move)

        board.push(move)
        if capture:
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                captured_piece_type = captured_piece.piece_type
                if captured_piece_type != chess.KING:
                    piece_mobility_score += piece_material_scores[captured_piece_type]

        if board.is_check():
            if board.turn != minimax_colour: # which means the opponent is being check
                piece_mobility_score += 150
            else:
                piece_mobility_score += -150

        if board.is_checkmate():
            if board.turn != minimax_colour:
                piece_mobility_score += 5000
            else:
                piece_mobility_score += -5000
        board.pop()
        
    return piece_mobility_score

# Evaluates the given board position and returns a score
# This score is a combination of material score, positional score, and mobility score
def evaluate_board(board, minimax_colour, opponent_colour):
    piece_material_score = 0
    piece_square_table_score = 0
    piece_mobility_score = 0

    if board.is_checkmate():
        if board.turn == minimax_colour:
            return float('-inf')
        else:
            return float('inf')
        
    piece_material_score = calculate_piece_material_score(board, minimax_colour, opponent_colour)

    piece_square_table_score = calculate_piece_square_table_score(board, minimax_colour, opponent_colour)

    # This mobility depends on the depth of the search can be either the mobility of stockfish or the mobility of minimaxalgo
    # If it belongs to sotckfish then should be negative, vice versa
    piece_mobility_score = calculate_mobility(board, minimax_colour)

    return (piece_material_score + piece_square_table_score + piece_mobility_score)

# Main body of the minimax algorithm with alpha-beta pruning
# Recursively evaluates board positions to find the best move
def minimax_algorithm_main_body(board, minimax_colour, opponent_colour, depth, is_maximising_player, alpha, beta):
    if depth == 0:
        return evaluate_board(board, minimax_colour, opponent_colour)

    if is_maximising_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board_copy = board.copy()
            board_copy.push(move)
            eval = minimax_algorithm_main_body(board_copy, minimax_colour, opponent_colour, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board_copy = board.copy()
            board_copy.push(move)
            eval = minimax_algorithm_main_body(board_copy, minimax_colour, opponent_colour, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Wrapper function for the minimax algorithm to facilitate multiprocessing
def minimax_process_wrapper(args):
    return minimax_algorithm_main_body(*args)

# Initiates the minimax algorithm with the given board, player color, and maximum search depth
# Returns the best move found
def minimax_algorithm_initiate(board, minimax_colour, max_depth):
    best_move = None
    best_eval = float('-inf')
    
    if minimax_colour == chess.WHITE:
        opponent_colour = chess.BLACK
    else:
        opponent_colour = chess.WHITE
    
    tasks = []
    for move in board.legal_moves:
        board_copy = board.copy()
        board_copy.push(move)
        tasks.append((board_copy, minimax_colour, opponent_colour, max_depth - 1, False, float('-inf'), float('inf')))
    
    with Pool(processes=None) as pool: 
        try:
            results = pool.map(minimax_process_wrapper, tasks)
    
            for move, eval in zip(board.legal_moves, results):
                if eval >= best_eval:
                    best_eval = eval
                    best_move = move
        except KeyboardInterrupt:
            print("terminate process")
    return best_move

# Uses the Stockfish chess engine to generate a move for the current board position
def stock_fish_move(board, engine):
    result = engine.play(board, chess.engine.Limit(time=0.1))
    return result.move

# Simulates a chess game between the minimax algorithm and Stockfish
# Logs moves and captures, and prints the final game result
def play_game(minimax_colour, chess_logger):
    board = chess.Board()

    engine = chess.engine.SimpleEngine.popen_uci(path_to_stockfish)
    engine.configure({"Skill Level": 0})
    while not board.is_game_over():
        # chess board down white, up black
        if board.turn == minimax_colour:
            print(board.legal_moves)
            move = minimax_algorithm_initiate(board, minimax_colour, 3)
        else:
            move = stock_fish_move(board, engine)
        
        chess_logger.log_move(move, board.turn)
        if board.is_capture(move):
            chess_logger.log_capture(board, move)
    
        board.push(move)
        print(board, "\n")
    
    chess_logger.summarise_game()

    if board.is_checkmate():
        result = "white win" if board.turn == chess.BLACK else "black win"
    elif board.is_stalemate():
        result = "stale mate"
    elif board.is_insufficient_material():
        result = "insufficient material"
    elif board.is_fivefold_repetition():
        result = "fivefold_repetition"
    elif board.is_seventyfive_moves():
        result = "seventyfive_moves"


    print("Game end! Results:", result)
    engine.quit()
    return result


def main():
    total_games = 10


    logger_white = ChessAlgoLogger()
    logger_black = ChessAlgoLogger()

    for _ in range(total_games):

        start_time = time.time()
        game_result_white = play_game(chess.WHITE, logger_white)
        end_time = time.time()
        game_time_white = end_time - start_time
        logger_white.log_game_result(game_result_white, game_time_white)

    for _ in range(total_games):
        start_time = time.time()
        game_result_black = play_game(chess.BLACK, logger_black)
        end_time = time.time()
        game_time_black = end_time - start_time
        logger_black.log_game_result(game_result_black, game_time_black)

    print("Statistics when playing as WHITE:")
    logger_white.print_stats()
    print("\nStatistics when playing as BLACK:")
    logger_black.print_stats()


if __name__ == "__main__":
    main()

    
