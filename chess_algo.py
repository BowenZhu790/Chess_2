# import python-chess library
import chess
import chess.engine

path_to_stockfish = "/Applications/Stockfish.app/Contents/MacOS/Stockfish"

engine = chess.engine.SimpleEngine.popen_uci(path_to_stockfish)

board = chess.Board()
def evaluate_board(board):
    board = chess.Board()

    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    
    # Calculate estimate utitliy for each type of piece
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


while not board.is_game_over():
     result = engine.play(board, chess.engine.Limit(time=0.1))
     board.push(result.move)

engine.quit()


    
