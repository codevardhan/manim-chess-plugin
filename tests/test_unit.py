import pytest
from manim import Mobject, WHITE, GREEN, BLACK
from manim_chessrender.mobjects.chessboard import ChessBoard
from manim_chessrender.mobjects.chess_piece import Queen, King, Pawn, Rook, Bishop, Knight
import chess


@pytest.fixture
def chess_board():
    return ChessBoard()


def test_initialize_board(chess_board):
    chess_board.initialize_board()
    assert isinstance(
        chess_board.elements[0], Rook), "Rook not placed correctly on a1."
    assert isinstance(
        chess_board.elements[7], Rook), "Rook not placed correctly on h1."
    assert isinstance(
        chess_board.elements[8], Pawn), "Pawn not placed correctly on a2."
    assert isinstance(
        chess_board.elements[63], Rook), "Rook not placed correctly on h8."


def test_position_to_index(chess_board):
    assert chess_board.position_to_index(
        'a1') == 0, "Incorrect index for position a1."
    assert chess_board.position_to_index(
        'h8') == 63, "Incorrect index for position h8."
    with pytest.raises(ValueError):
        chess_board.position_to_index('z9')


def test_index_to_position(chess_board):
    assert chess_board.index_to_position(
        0) == 'a1', "Incorrect position for index 0."
    assert chess_board.index_to_position(
        63) == 'h8', "Incorrect position for index 63."
    with pytest.raises(ValueError):
        chess_board.index_to_position(64)


def test_color_squares(chess_board):
    chess_board.color_squares()
    assert chess_board.squares['a1'].get_fill_opacity(
    ) == 0.7, "Incorrect square color fill opacity."
    assert chess_board.squares['h8'].get_fill_opacity(
    ) == 0.7, "Incorrect square color fill opacity."


def test_add_element(chess_board):
    piece = King(WHITE)
    chess_board.add_element('e4', piece)
    index = chess_board.position_to_index('e4')
    assert chess_board.elements[index] == piece, "Piece not added correctly to the board."


def test_handle_castling(chess_board):
    chess_board.initialize_board()
    move = chess.Move.from_uci('e1g1')  # White kingside castling
    animations = chess_board.handle_castling(move)
    assert animations is not None, "Castling animation group should not be None."
    rook_index = chess_board.position_to_index('f1')
    king_index = chess_board.position_to_index('g1')
    assert isinstance(
        chess_board.elements[rook_index], Rook), "Rook not moved correctly during castling."
    assert isinstance(
        chess_board.elements[king_index], King), "King not moved correctly during castling."


def test_handle_promotion(chess_board):
    chess_board.load_fen("8/4P3/8/8/8/8/8/8 w - - 0 1")
    move = chess.Move.from_uci('e7e8q')  # Promotion to Queen
    animations = chess_board.handle_promotion(move)
    assert animations is not None, "Promotion animation group should not be None."
    promoted_index = chess_board.position_to_index('e8')
    assert isinstance(
        chess_board.elements[promoted_index], Queen), "Pawn not promoted to Queen correctly."


def test_load_fen(chess_board):
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    chess_board.load_fen(fen)
    assert isinstance(
        chess_board.elements[0], Rook), "FEN loading failed for a1."
    assert isinstance(
        chess_board.elements[63], Rook), "FEN loading failed for h8."
    assert isinstance(
        chess_board.elements[8], Pawn), "FEN loading failed for a2."
