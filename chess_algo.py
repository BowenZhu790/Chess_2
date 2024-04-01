# import python-chess library
import chess
import chess.engine
import random
import time

from chess_algo_logger import ChessAlgoLogger
# path_to_stockfish = "D:\stockfish\stockfish\stockfish-windows-x86-64-avx2.exe"

board = chess.Board()

pawn_square_table = [
    0,   0,   0,   0,   0,   0,  0,   0,
    5,  10,  10, -10, -10,  10, 10,   5,
    5,  -5, -10,   0,   0, -10, -5,   5,
    0,   0,   0,  20,  20,   0,  0,   0,
    5,   5,  10,  25,  25,  10,  5,   5,
    10, 10,  20,  30,  30,  20, 10,  10,
    50, 50,  50,  50,  50,  50, 50,  50,
    0,   0,   0,   0,   0,   0,  0,   0
]

knight_square_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   0,   5,   5,   5,   5,   0, -10,
    -10,   5,  10,  15,  15,  10,   5, -10,
    -10,   5,  15,  20,  20,  15,   5, -10,
    -10,   5,  15,  20,  20,  15,   5, -10,
    -10,   5,  10,  15,  15,  10,   5, -10,
    -10,   0,   5,   5,   5,   5,   0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
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

king_square_table_opening = [
    0,   0,   0, -20, -20,   0,   0,   0,
    0,   0, -10, -20, -20, -10,   0,   0,
    0, -10, -20, -30, -30, -20, -10,   0,
    0, -10, -20, -30, -30, -20, -10,   0,
    0, -10, -20, -30, -30, -20, -10,   0,
    0, -10, -20, -30, -30, -20, -10,   0,
    0,   0, -10, -20, -20, -10,   0,   0,
    0,   0,   0, -20, -20,   0,   0,   0
]

king_square_table_middlegame = [
    -35, -30, -40, -50, -50, -40, -30, -35,
    -35, -30, -40, -50, -50, -40, -30, -35,
    -35, -35, -40, -50, -50, -40, -35, -35,
    -35, -40, -40, -50, -50, -40, -40, -35,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
     20,  20,   0,   0,   0,   0,  20,  20,
     20,  30,  10,   0,   0,  10,  30,  20
]

king_square_table_endgame = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10,   0,   0, -10, -20, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -30,   0,   0,   0,   0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50
]

king_square_tables = {
    "Opening": king_square_table_opening,
    "Middlegame": king_square_table_middlegame,
    "Endgame": king_square_table_endgame
}

piece_values = {
        chess.PAWN: 10, 
        chess.KNIGHT: 30, 
        chess.BISHOP: 33, 
        chess.ROOK: 50, 
        chess.QUEEN: 90, 
        chess.KING: 0
    }

def calculate_mobility(board):
    mobility_score = 0
    mobility_score += len(list(board.legal_moves)) * 5

    for move in board.legal_moves:
        captured_piece_type = None
        # moving_piece = board.piece_at(move.from_square)
        
        # if moving_piece.piece_type == chess.PAWN:
        #     mobility_score += 1
        # elif moving_piece.piece_type == chess.KNIGHT:
        #     mobility_score += 3
        # elif moving_piece.piece_type == chess.BISHOP:
        #     mobility_score += 3
        # elif moving_piece.piece_type == chess.ROOK:
        #     mobility_score += 3.5
        # elif moving_piece.piece_type == chess.QUEEN:
        #     mobility_score += 5
        # elif moving_piece.piece_type == chess.KING:
        #     mobility_score += 3
        
        # if board.is_capture(move):
        #     mobility_score += 3
        # if move.promotion is not None:
        #     if move.promotion == chess.QUEEN:
        #         mobility_score += 10
        #     elif move.promotion in [chess.ROOK, chess.BISHOP, chess.KNIGHT]:
        #         mobility_score += 5

        # board.push(move)
        # if board.is_check():
        #     mobility_score += 15
        # if board.is_checkmate():
        #     mobility_score += 5000
        # board.pop()
        if board.is_capture(move):
            board.push(move)
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                captured_piece_type = captured_piece.piece_type
                if captured_piece_type == chess.PAWN:
                    mobility_score += 10
                elif captured_piece_type == chess.KNIGHT or captured_piece_type == chess.BISHOP:
                    mobility_score += 30
                elif captured_piece_type == chess.ROOK:
                    mobility_score += 50
                elif captured_piece_type == chess.QUEEN:
                    mobility_score += 90
            board.pop()
        else:
            board.push(move)
            if board.is_check():
                mobility_score += 150
            if board.is_checkmate():
                mobility_score += 5000
            board.pop()

        if move.promotion is not None:
            # Adjust score based on the promotion type
            if move.promotion == chess.QUEEN:
                mobility_score += 80
            else:
                mobility_score += 30
        
    return mobility_score

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

def evaluate_board(board, minimax_color, opponent_color):
    if board.is_checkmate():
        if board.turn == minimax_color:
            return -9999
        else:
            return 9999

    game_phase = determine_game_phase(board)
    current_king_square_table = king_square_tables[game_phase]

    piece_values = {
        chess.PAWN: 10, 
        chess.KNIGHT: 30, 
        chess.BISHOP: 33, 
        chess.ROOK: 50, 
        chess.QUEEN: 90, 
        chess.KING: 0
    }

    piece_square_tables = {
        chess.PAWN: pawn_square_table,
        chess.KNIGHT: knight_square_table,
        chess.BISHOP: bishop_square_table,
        chess.ROOK: rook_square_table,
        chess.QUEEN: queen_square_table,
        chess.KING: current_king_square_table
    }

    minimax_material_value = 0
    opponent_material_value = 0

    minimax_piece_square_table_value = 0
    opponent_piece_square_table_value = 0

    for piece_type, piece_value in piece_values.items():
        minimax_pieces = board.pieces(piece_type, minimax_color)
        opponent_pieces = board.pieces(piece_type, opponent_color)

        minimax_material_value += piece_value * len(minimax_pieces)
        opponent_material_value += piece_value * len(opponent_pieces)

        for square in minimax_pieces:
            # since minimax is alwasy the maximising player, therefore the square table needs to be mirror when minimax plays black
            if minimax_color == chess.BLACK:
                # print(square, "1")
                square = chess.square_mirror(square)
                # print(square, "2")
            minimax_piece_square_table_value += piece_square_tables[piece_type][square]

        for square in opponent_pieces:
            if minimax_color == chess.WHITE:
                # print(square, "3")
                square = chess.square_mirror(square)
                # print(square, "4")
            opponent_piece_square_table_value += piece_square_tables[piece_type][square]

    material_score = minimax_material_value - opponent_material_value
    piece_square_score = minimax_piece_square_table_value - opponent_piece_square_table_value
    
    # this mobility depends on the depth of the search can be either the mobility of stockfish or the mobility of minimaxalgo
    # if it belongs to sotckfish then should be negative, vice versa
    stockfish_mobility = calculate_mobility(board)

    return (material_score + piece_square_score - stockfish_mobility)

# def evaluate_board(board, minimax_color, opponent_color):
#     # board = chess.Board()

#     if board.is_checkmate():
#         if board.turn:
#             return -9999
#         else:
#             return 9999
    
#     # Calculate estimate utitliy for each type of pieces
#     minimax_pawn = len(board.pieces(chess.PAWN, minimax_color))
#     minimax_knight = len(board.pieces(chess.KNIGHT, minimax_color))
#     minimax_bishop = len(board.pieces(chess.BISHOP, minimax_color))
#     minimax_rook = len(board.pieces(chess.ROOK, minimax_color))
#     minimax_queen = len(board.pieces(chess.QUEEN, minimax_color))

#     opponent_pawn = len(board.pieces(chess.PAWN, opponent_color))
#     opponent_knight = len(board.pieces(chess.KNIGHT, opponent_color))
#     opponent_bishop = len(board.pieces(chess.BISHOP, opponent_color))
#     opponent_rook = len(board.pieces(chess.ROOK, opponent_color))
#     opponent_queen = len(board.pieces(chess.QUEEN, opponent_color))

#     pawn_value = 10 * (minimax_pawn - opponent_pawn)
#     knight_value = 30 * (minimax_knight - opponent_knight)
#     bishop_value = 30 * (minimax_bishop - opponent_bishop)
#     rook_value = 50 * (minimax_rook - opponent_rook)
#     queen_value = 90 * (minimax_queen - opponent_queen)

#     minimax_pawn_score = sum(pawn_square_table[i] for i in board.pieces(chess.PAWN, minimax_color))
#     opponent_pawn_score = sum(-(pawn_square_table[chess.square_mirror(i)]) for i in board.pieces(chess.PAWN, opponent_color))

#     minimax_knight_score = sum(knight_square_table[i] for i in board.pieces(chess.KNIGHT, minimax_color))
#     opponent_knight_score = sum(-(knight_square_table[chess.square_mirror(i)]) for i in board.pieces(chess.KNIGHT, opponent_color))

#     minimax_bishop_score = sum(bishop_square_table[i] for i in board.pieces(chess.BISHOP, minimax_color))
#     opponent_bishop_score = sum(-(bishop_square_table[chess.square_mirror(i)]) for i in board.pieces(chess.BISHOP, opponent_color))

#     minimax_rook_score = sum(rook_square_table[i] for i in board.pieces(chess.ROOK, minimax_color))
#     opponent_rook_score = sum(-(rook_square_table[chess.square_mirror(i)]) for i in board.pieces(chess.ROOK, opponent_color))

#     minimax_queen_score = sum(queen_square_table[i] for i in board.pieces(chess.QUEEN, minimax_color))
#     opponent_queen_score = sum(-(queen_square_table[chess.square_mirror(i)]) for i in board.pieces(chess.QUEEN, opponent_color))

#     # this mobility depends on the depth of the search can be either the mobility of stockfish or the mobility of minimaxalgo
#     # if it belongs to sotckfish then should be negative, vice versa
#     stockfish_mobility = calculate_mobility(board)

#     pieces_value = pawn_value + knight_value + bishop_value + rook_value + queen_value
    
#     white_pieces_square_table_score =  minimax_pawn_score + minimax_knight_score + minimax_bishop_score + minimax_rook_score + minimax_queen_score
#     black_pieces_square_table_score = opponent_pawn_score + opponent_knight_score + opponent_bishop_score + opponent_rook_score + opponent_queen_score

#     # return the estimate value
#     return pieces_value + white_pieces_square_table_score + black_pieces_square_table_score - stockfish_mobility


def moves_order(board, move):
    move_score = 0
    if board.is_capture(move):
        move_score += 10  

    # board.push(move)
    # if board.is_check():
    #     move_score += 10
    # if board.is_checkmate():
    #     move_score += 5000
    # board.pop() 
    return move_score

def minimax(board, minimax_color, opponent_color, depth, is_maximising_player, alpha, beta):
    # board = chess.Board()
    if depth == 0:
        return evaluate_board(board, minimax_color, opponent_color)
    
    
    if is_maximising_player:

        max_value = -9999999
        # moves = [(moves_order(board, move), move) for move in board.legal_moves]
        # moves.sort(key=lambda x: x[0])
        # for _, move in moves:
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
        # moves = [(moves_order(board, move), move) for move in board.legal_moves]
        # moves.sort(key=lambda x: x[0])
        # for _, move in moves:
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, minimax_color, opponent_color, depth-1, True, alpha, beta)
            board.pop()
            min_value = min(min_value, eval)
            beta = min(beta, min_value)
            if alpha >= beta:
                break
        return min_value

def minimax_algorithm_move(board, minimax_color, max_depth):
    # board = chess.Board()

    best_move = None
    best_value = -9999999
    if minimax_color == chess.WHITE:
        opponent_color = chess.BLACK
    else:
        opponent_color = chess.WHITE

    for move in board.legal_moves:
        board.push(move)
        move_value = minimax(board, minimax_color, opponent_color, max_depth, True, -9999999, 9999999)
        board.pop()

        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move



    

def stock_fish_move(board, engine):
    result = engine.play(board, chess.engine.Limit(time=0.1))
    return result.move

def play_game(minimax_color, chess_logger):
    board = chess.Board()

    path_to_stockfish = "D:\stockfish\stockfish\stockfish-windows-x86-64-avx2.exe"
    engine = chess.engine.SimpleEngine.popen_uci(path_to_stockfish)
    engine.configure({"Skill Level": 0})
    while not board.is_game_over():
        # chess board down white, up black
        if board.turn == minimax_color:
            print(board.legal_moves)
            move = minimax_algorithm_move(board, minimax_color, 2)
        else:
            move = stock_fish_move(board, engine)
            # move = minimax_algorithm_move(board, not minimax_color, 2)
        
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
    return {"result": result, "captured": chess_logger.captured_pieces_sum, "chess_logger": chess_logger}


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

def print_stats(total_games, wins, captured_pieces_counter, color, average_time, average_moves):
    print(f"\n\nStatistics when minimax algo plays {color}: ")
    print("Total games:", total_games)
    print("Wins for WHITE:", wins["WHITE"])
    print("Winning rate for WHITE:", wins["WHITE"] / total_games)
    print("Wins for BLACK:", wins["BLACK"])
    print("Winning rate for BLACK:", wins["BLACK"] / total_games)
    print("Draws:", wins["DRAW"])
    for color, counts in captured_pieces_counter.items():
        print(f"{color}'s captured pieces:")
        for piece, count in counts.items():
            print(f"{piece}: {count}")
    
    print(f"Average game duration: {average_time:.2f} seconds\n")
    print(f"Average moves per game: {average_moves:.2f}\n")

def play_and_collect_stats(total_games, player_color):
    wins = {"WHITE": 0, "BLACK": 0, "DRAW": 0}
    captured_pieces_counter = {"WHITE":{"P": 0, "N": 0, "B": 0, "R": 0, "Q": 0},
                               "BLACK":{"p": 0, "n": 0, "b": 0, "r": 0, "q": 0}}
    
    total_moves = 0
    total_time = 0

    for _ in range(total_games):

        start_time = time.time()

        game_result = play_game(player_color)

        end_time = time.time()
        game_time = end_time - start_time
        total_time += game_time

        total_moves += len(game_result["chess_logger"].white_moves) + len(game_result["chess_logger"].black_moves)

        update_stats(game_result, wins, captured_pieces_counter)
    
    average_time = total_time / total_games
    average_moves = total_moves / total_games

    return wins, captured_pieces_counter, average_time, average_moves


# def main():
    
#     total_games = 1

#     wins_white, captured_pieces_counter_white, average_time_white, average_moves_white = play_and_collect_stats(total_games, chess.WHITE)
#     wins_black, captured_pieces_counter_black, average_time_black, average_moves_black = play_and_collect_stats(total_games, chess.BLACK)

#     print_stats(total_games, wins_white, captured_pieces_counter_white, "white", average_time_white, average_moves_white)
#     print_stats(total_games, wins_black, captured_pieces_counter_black, "black", average_time_black, average_moves_black)

#     # show_stats(total_games, wins_white, captured_pieces_counter_white, average_time_white, average_moves_white)

def main():
    total_games = 3  # 示范用，实际游戏次数可根据需要调整

    # 分别为白方和黑方创建logger实例
    logger_white = ChessAlgoLogger()
    logger_black = ChessAlgoLogger()

    for _ in range(total_games):
        # 白方作为minimax玩家
        start_time = time.time()
        game_result_white = play_game(chess.WHITE, logger_white)
        end_time = time.time()
        game_time_white = end_time - start_time
        logger_white.log_game_result(game_result_white["result"], game_time_white)

    # for _ in range(total_games):
    #     start_time = time.time()
    #     game_result_black = play_game(chess.BLACK, logger_black)
    #     end_time = time.time()
    #     game_time_black = end_time - start_time
    #     logger_black.log_game_result(game_result_black["result"], game_time_black)

    # 分别打印作为白方和黑方时的统计信息
    print("Statistics when playing as WHITE:")
    logger_white.print_stats()
    print("\nStatistics when playing as BLACK:")
    logger_black.print_stats()
if __name__ == "__main__":
    main()

    
