from manim import *
from src.manim_chessrender import *

class InitializeChessBoard(MovingCameraScene):
    """
    Scene to demonstrate initializing the chessboard.
    """
    def construct(self):
        chessboard = ChessBoard()
        chessboard.initialize_board()
        self.add(chessboard.board)
        self.wait(2)

class MovePieceExample(MovingCameraScene):
    """
    Scene to demonstrate moving a piece on the chessboard.
    """
    def construct(self):
        chessboard = ChessBoard()
        chessboard.initialize_board()
        self.add(chessboard.board)
        self.wait(1)
        self.play(chessboard.move_piece('e2e4'))
        self.wait(2)

class LoadFENExample(MovingCameraScene):
    """
    Scene to demonstrate loading a FEN string into the chessboard.
    """
    def construct(self):
        chessboard = ChessBoard()
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        chessboard.load_fen(fen)
        self.add(chessboard.board)
        self.wait(2)

class CastlingExample(MovingCameraScene):
    """
    Scene to demonstrate castling on the chessboard.
    """
    def construct(self):
        chessboard = ChessBoard()
        chessboard.initialize_board()
        self.add(chessboard.board)
        self.wait(1)
        # Move pieces to prepare for castling
        moves = ['e2e4', 'e7e5', 'g1f3', 'g8f6', 'f1e2', 'f8e7']
        for move in moves:
            self.play(chessboard.move_piece(move))
        self.play(chessboard.move_piece('e1g1'))  # Kingside castling
        self.wait(2)

class EnPassantExample(MovingCameraScene):
    """
    Scene to demonstrate the en passant move on the chessboard.
    """
    def construct(self):
        chessboard = ChessBoard()
        chessboard.initialize_board()
        self.add(chessboard.board)
        self.wait(1)
        # Move pieces to prepare for en passant
        moves = ['e2e4', 'e7e5', 'd2d4', 'e5d4', 'c2c4']
        for move in moves:
            self.play(chessboard.move_piece(move))
        self.play(chessboard.move_piece('d4c3'))  # En passant
        self.wait(2)

class PlayPGNExample(MovingCameraScene):
    """
    Scene to demonstrate playing moves from a PGN file on the chessboard.
    """
    def construct(self):
        chessboard = ChessBoard()
        chessboard.initialize_board()
        self.add(chessboard.board)
        self.wait(1)
        
        games = chessboard.load_pgn(".example/example.pgn")
        game = games[0]
        for move in game:
            self.play(chessboard.move_piece(move.uci()))
            self.wait(0.5)
            
            
if __name__ == "__main__":
    scenes = [InitializeChessBoard, MovePieceExample, LoadFENExample, CastlingExample, EnPassantExample, PlayPGNExample]
    # render an entire game from pgn
    scene_instance = scenes[-1]()
    scene_instance.render()

