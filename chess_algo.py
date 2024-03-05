# import python-chess library
import chess
import chess.engine
import random
import time

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

# 升变，吃子，将军，等等。。。。同时根据不同棋子计算他们独立的分数
def calculate_mobility(board):
    mobility_score = 0

    # 直接遍历所有合法移动
    for move in board.legal_moves:
        moving_piece = board.piece_at(move.from_square)
        
        # 基础分数调整，根据移动的棋子类型
        if moving_piece.piece_type == chess.PAWN:
            mobility_score += 1
        elif moving_piece.piece_type == chess.KNIGHT:
            mobility_score += 3
        elif moving_piece.piece_type == chess.BISHOP:
            mobility_score += 3
        elif moving_piece.piece_type == chess.ROOK:
            mobility_score += 3.5
        elif moving_piece.piece_type == chess.QUEEN:
            mobility_score += 5
        # elif moving_piece.piece_type == chess.KING:
        #     mobility_score += 3
        
        # 特殊操作分数调整
        if board.is_capture(move):
            mobility_score += 10
        if move.promotion is not None:
            if move.promotion == chess.QUEEN:
                mobility_score += 10
            elif move.promotion in [chess.ROOK, chess.BISHOP, chess.KNIGHT]:
                mobility_score += 5
        
    return mobility_score


def evaluate_board(board, minimax_color, opponent_color):
    # board = chess.Board()

    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    
    # Calculate estimate utitliy for each type of pieces
    minimax_pawn = len(board.pieces(chess.PAWN, minimax_color))
    minimax_knight = len(board.pieces(chess.KNIGHT, minimax_color))
    minimax_bishop = len(board.pieces(chess.BISHOP, minimax_color))
    minimax_rook = len(board.pieces(chess.ROOK, minimax_color))
    minimax_queen = len(board.pieces(chess.QUEEN, minimax_color))

    opponent_pawn = len(board.pieces(chess.PAWN, opponent_color))
    opponent_knight = len(board.pieces(chess.KNIGHT, opponent_color))
    opponent_bishop = len(board.pieces(chess.BISHOP, opponent_color))
    opponent_rook = len(board.pieces(chess.ROOK, opponent_color))
    opponent_queen = len(board.pieces(chess.QUEEN, opponent_color))

    pawn_value = 10 * (minimax_pawn - opponent_pawn)
    knight_value = 30 * (minimax_knight - opponent_knight)
    bishop_value = 30 * (minimax_bishop - opponent_bishop)
    rook_value = 50 * (minimax_rook - opponent_rook)
    queen_value = 90 * (minimax_queen - opponent_queen)

    minimax_pawn_score = sum(pawn_square_table[i] for i in board.pieces(chess.PAWN, minimax_color))
    opponent_pawn_score = sum(-pawn_square_table[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, opponent_color))

    minimax_knight_score = sum(knight_square_table[i] for i in board.pieces(chess.KNIGHT, minimax_color))
    opponent_knight_score = sum(-knight_square_table[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, opponent_color))

    minimax_bishop_score = sum(bishop_square_table[i] for i in board.pieces(chess.BISHOP, minimax_color))
    opponent_bishop_score = sum(-bishop_square_table[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, opponent_color))

    minimax_rook_score = sum(rook_square_table[i] for i in board.pieces(chess.ROOK, minimax_color))
    opponent_rook_score = sum(-rook_square_table[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, opponent_color))

    minimax_queen_score = sum(queen_square_table[i] for i in board.pieces(chess.QUEEN, minimax_color))
    opponent_queen_score = sum(-queen_square_table[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, opponent_color))

    # this mobility depends on the depth of the search can be either the mobility of stockfish or the mobility of minimaxalgo
    # if it belongs to sotckfish then should be negative, vice versa
    stockfish_mobility = calculate_mobility(board)

    pieces_value = pawn_value + knight_value + bishop_value + rook_value + queen_value
    white_pieces_square_table_score =  minimax_pawn_score + minimax_knight_score + minimax_bishop_score + minimax_rook_score + minimax_queen_score
    black_pieces_square_table_score = opponent_pawn_score + opponent_knight_score + opponent_bishop_score + opponent_rook_score + opponent_queen_score

    # return the estimate value
    return pieces_value + white_pieces_square_table_score + black_pieces_square_table_score - stockfish_mobility

def minimax(board, minimax_color, opponent_color, depth, is_maximising_player, alpha, beta):
    # board = chess.Board()
    if depth == 0:
        return evaluate_board(board, minimax_color, opponent_color)

    if is_maximising_player:
        max_value = -9999999
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, minimax_color, opponent_color, depth-1, False, alpha, beta)
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
            eval = minimax(board, minimax_color, opponent_color, depth-1, True, alpha, beta)
            board.pop()
            min_value = min(min_value, eval)
            beta = min(beta, min_value)
            if alpha >= beta:
                break
        return min_value


def minimax_algorithm_move(board, minimax_color):
    # board = chess.Board()

    best_move = None
    best_value = -9999999
    if minimax_color == chess.WHITE:
        opponent_color = chess.BLACK
    else:
        opponent_color = chess.WHITE

    for move in board.legal_moves:
        board.push(move)
        move_value = minimax(board, minimax_color, opponent_color, 4, True, -9999999, 9999999)
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

def play_game(minimax_color):
    board = chess.Board()
    chess_logger = ChessAlgoLogger()

    path_to_stockfish = "D:\stockfish\stockfish\stockfish-windows-x86-64-avx2.exe"
    engine = chess.engine.SimpleEngine.popen_uci(path_to_stockfish)
    engine.configure({"Skill Level": 0})
    while not board.is_game_over():

        # chess board down white, up black
        if board.turn == minimax_color:
            print(board.legal_moves)
            move = minimax_algorithm_move(board, minimax_color)
            # move = stock_fish_move(board, engine)
        else:
            move = stock_fish_move(board, engine)
            # move = minimax_algorithm_move(board, chess.BLACK)
            # move = random.choice(list(board.legal_moves))
        
        chess_logger.log_move(move, board.turn)
        if board.is_capture(move):
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
    return {"result": result, "captured": chess_logger.captured_pieces}


def update_stats(game_result, wins, captured_pieces_counter):
    if game_result["result"] == "white win":
        wins["WHITE"] += 1
    elif game_result["result"] == "black win":
        wins["BLACK"] += 1
    else:
        wins["DRAW"] += 1
    
    for color, pieces in game_result["captured"].items():
        for piece in pieces:
            captured_pieces_counter[color][piece] += 1

def print_stats(total_games, wins, captured_pieces_counter, color, average_time):
    print(f"\n\nStatistics when minimax algo plays {color}: ")
    print("Total games:", total_games)
    print("Wins for WHITE:", wins["WHITE"])
    print("Winning rate for WHITE:", wins["WHITE"] / total_games)
    print("Wins for BLACK:", wins["BLACK"])
    print("Winning rate for BLACK:", wins["BLACK"] / total_games)
    print("Draws:", wins["DRAW"])
    for color, counts in captured_pieces_counter.items():
        print(f"Captured pieces for {color}:")
        for piece, count in counts.items():
            print(f"{piece}: {count}")
    
    print(f"Average game duration: {average_time:.2f} seconds\n")

def play_and_collect_stats(total_games, player_color):
    wins = {"WHITE": 0, "BLACK": 0, "DRAW": 0}
    captured_pieces_counter = {"WHITE":{"P": 0, "N": 0, "B": 0, "R": 0, "Q": 0},
                               "BLACK":{"p": 0, "n": 0, "b": 0, "r": 0, "q": 0}}
    
    total_time = 0

    for _ in range(total_games):

        start_time = time.time()

        game_result = play_game(player_color)

        end_time = time.time()
        game_time = end_time - start_time
        total_time += game_time

        update_stats(game_result, wins, captured_pieces_counter)
    
    average_time = total_time / total_games

    return wins, captured_pieces_counter, average_time

def main():
    total_games = 3

    wins_white, captured_pieces_counter_white, average_time_white = play_and_collect_stats(total_games, chess.WHITE)
    wins_black, captured_pieces_counter_black, average_time_black = play_and_collect_stats(total_games, chess.BLACK)

    print_stats(total_games, wins_white, captured_pieces_counter_white, "white", average_time_white)
    print_stats(total_games, wins_black, captured_pieces_counter_black, "black", average_time_black)

main()

    
