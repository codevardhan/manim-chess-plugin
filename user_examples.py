from manim import *
from src.manim_chessrender import *


class ChessExample(MovingCameraScene):
    def construct(self):
        chessboard = ChessBoard()

        # Adjust camera frame to fit ChessBoard in scene
        self.camera.frame_width = chessboard.width + 10
        self.camera.frame_height = chessboard.height + 10
        self.camera.frame.move_to(chessboard)

        chessboard.initialize_board()
        self.add(chessboard.board)
        self.wait(2)

if __name__ == "__main__":
    scene = ChessExample()
    scene.render()