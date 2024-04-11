from unittest import TestCase
import unittest
import chess
import time

from chess_algo import calculate_mobility, evaluate_board, determine_game_phase, calculate_piece_material_score, piece_material_scores, calculate_piece_square_table_score, knight_square_table, pawn_square_table, play_game, stock_fish_move, path_to_stockfish
from chess_algo_logger import ChessAlgoLogger 

class TestChessAlgo(TestCase):
    def setUp(self):
        self.board = chess.Board()
        self.custom_board = chess.Board(fen=None)
        for square in chess.SQUARES:
            self.custom_board.remove_piece_at(square)

    def test_initial_board(self):
        self.assertEqual(str(self.board.fen()), chess.STARTING_FEN)
        self.assertEqual(len(self.board.piece_map()), 32)
        self.assertTrue(self.board.turn == chess.WHITE)

    def test_pawn_advance(self):
        move = chess.Move.from_uci('e2e4')
        self.board.push(move)
        self.assertTrue(self.board.piece_at(chess.E4).piece_type == chess.PAWN) 
        self.assertTrue(self.board.color_at(chess.E4) == chess.WHITE)

    def test_calculate_mobility_initial_position(self):
        board = chess.Board()
        minimax_colour = chess.WHITE
        self.assertEqual(calculate_mobility(board, minimax_colour), 80, "Initial mobility score should be 8, 64 from pawns, 16 from knights.")

    def test_evaluate_board_initial_position(self):
        board = chess.Board()
        minimax_color = chess.WHITE
        opponent_color = chess.BLACK
        self.assertEqual(evaluate_board(board, minimax_color, opponent_color), 80, "Initial board score should be 80, because material score and PST score cancel each others out, but still needs to add mobility score which is initially 80")

    def test_calculate_piece_material_score_custom(self):
        self.custom_board.set_piece_at(chess.D4, chess.Piece(chess.PAWN, chess.WHITE))
        self.custom_board.set_piece_at(chess.D5, chess.Piece(chess.ROOK, chess.BLACK))
        expected_score = piece_material_scores[chess.PAWN] - piece_material_scores[chess.ROOK]
        self.assertEqual(calculate_piece_material_score(self.custom_board, chess.WHITE, chess.BLACK), expected_score, "Custom material score calculation error.")

    def test_calculate_piece_square_table_score_custom(self):
        self.custom_board.set_piece_at(chess.D4, chess.Piece(chess.PAWN, chess.WHITE))
        self.custom_board.set_piece_at(chess.D5, chess.Piece(chess.PAWN, chess.BLACK))
        self.custom_board.set_piece_at(chess.E4, chess.Piece(chess.KNIGHT, chess.WHITE))
        game_phase = determine_game_phase(self.custom_board)
        self.assertEqual(game_phase, "Endgame", "Game phase should be Endgame.")
        score = calculate_piece_square_table_score(self.custom_board, chess.WHITE, chess.BLACK)
        expected_score = knight_square_table[chess.E4] + pawn_square_table[chess.D4] - pawn_square_table[chess.square_mirror(chess.D5)]
        self.assertEqual(score, expected_score, "Custom PST score calculation error.")




    def test_opening_phase(self):
        board = chess.Board()
        self.assertEqual(determine_game_phase(board), "Opening")

    def test_middlegame_phase(self):
        board = chess.Board()
        board.remove_piece_at(chess.parse_square("e2"))
        board.remove_piece_at(chess.parse_square("e7"))
        board.remove_piece_at(chess.parse_square("d2"))
        board.remove_piece_at(chess.parse_square("d7"))
        self.assertEqual(determine_game_phase(board), "Middlegame")

    def test_endgame_phase(self):
        board = chess.Board()
        for square in ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
                       "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
                       "a1", "h1", "a8", "h8"]:
            board.remove_piece_at(chess.parse_square(square))
        self.assertEqual(determine_game_phase(board), "Endgame")



class TestChessAlgoLogger(TestCase):
    def setUp(self):
        self.logger = ChessAlgoLogger()
        self.board = chess.Board()

    def test_log_move(self):
        move = chess.Move.from_uci("e2e4")
        self.logger.log_move(move, chess.WHITE)
        self.assertIn("e2e4", self.logger.white_moves)

    def test_log_capture(self):
        self.board.set_piece_at(chess.parse_square("e4"), chess.Piece(chess.PAWN, chess.BLACK))
        move = chess.Move.from_uci("e2e4")
        self.logger.log_capture(self.board, move)
        self.board.push(move)
        self.assertIn('p', self.logger.captured_pieces_per_game["BLACK"])

    def test_log_game_result(self):
        self.logger.log_game_result("white win", 100)
        self.assertEqual(self.logger.results["WHITE"], 1)

    def test_summarise_game(self):
        self.logger.log_move(chess.Move.from_uci("e2e4"), chess.WHITE)
        self.logger.summarise_game()
        self.assertEqual(len(self.logger.white_moves), 0) 

    def test_print_stats(self):
        self.logger.log_game_result("white win", 100)
        self.logger.print_stats() 


class TestFunctional(TestCase):
    def setUp(self):
        self.logger = ChessAlgoLogger()
        self.board = chess.Board()

    def test_full_game_process(self):
        logger = ChessAlgoLogger()
        start_time = time.time()
        game_result = play_game(chess.WHITE, logger)
        end_time = time.time()
        game_time = end_time - start_time
        logger.log_game_result(game_result, game_time)
        self.assertIn(game_result, ["white win", "black win", "stale mate", "insufficient material", "fivefold_repetition", "seventyfive_moves"], "Game did not end with a recognized condition.")
        self.assertGreaterEqual(logger.total_moves, 1, "Game should have at least one move.")

    def test_stockfish_move_generation(self):
        board = chess.Board()
        engine = chess.engine.SimpleEngine.popen_uci(path_to_stockfish)
        move = stock_fish_move(board, engine)
        self.assertTrue(move in board.legal_moves, "The move generated by Stockfish should be legal.")
        engine.quit()

    def test_material_score(self):
        board = chess.Board()
        score = calculate_piece_material_score(board, chess.WHITE, chess.BLACK)
        self.assertEqual(score, 0, "Initial material score should be equal for both sides.")

    def test_mobility_score_initial_position(self):
        board = chess.Board()
        score = calculate_mobility(board, chess.WHITE)
        self.assertTrue(score > 0, "Mobility score in the initial position should be greater than 0.")
    

    def test_capture_logging(self):
        logger = ChessAlgoLogger()
        board = chess.Board("8/8/8/3q4/3P4/8/8/8 w - - 0 1")
        move = chess.Move.from_uci("d5d4")
        board.push(move)
        logger.log_capture(board, move)
        self.assertIn('Q', logger.captured_pieces_per_game["WHITE"], "Capture should be logged correctly.")

    def test_game_statistics_summary(self):
        logger = ChessAlgoLogger()
        logger.log_game_result("white win", 100)
        logger.summarise_game()
        self.assertEqual(logger.results["WHITE"], 1, "Game results should be summarized correctly.")

    def test_performance_metrics(self):
        logger = ChessAlgoLogger()
        logger.log_game_result("white win", 100)
        logger.print_stats()
        self.assertTrue(logger.total_games > 0, "Total number of games played should be greater than 0.")

    def test_game_evaluation(self):
        board = chess.Board("8/5k2/8/8/8/8/2R5/4K3 w - - 0 1")
        minimax_colour = chess.WHITE
        opponent_colour = chess.BLACK
        score = evaluate_board(board, minimax_colour, opponent_colour)
        self.assertTrue(score > 0, "Endgame evaluation should favor WHITE.")

    def test_pawn_promotion_impact(self):
        board = chess.Board("8/P7/8/8/8/8/8/7k w - - 0 1")
        minimax_colour = chess.WHITE
        opponent_colour = chess.BLACK
        move = chess.Move.from_uci("a7a8q")
        board.push(move)
        score = evaluate_board(board, minimax_colour, opponent_colour)
        self.assertTrue(score > 0, "Pawn promotion should significantly increase WHITE's score.")

    def test_game_logging(self):
        logger = ChessAlgoLogger()
        board = chess.Board()
        move = chess.Move.from_uci("e2e4")
        board.push(move)
        logger.log_move(move, chess.WHITE)
        move = chess.Move.from_uci("e7e5")
        board.push(move)
        logger.log_move(move, chess.BLACK)
        self.assertIn("e2e4", logger.white_moves, "White move not logged correctly.")
        self.assertIn("e7e5", logger.black_moves, "Black move not logged correctly.")

if __name__ == '__main__':
    unittest.main() 