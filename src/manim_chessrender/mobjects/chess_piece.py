from manim import Mobject, ManimColor, ImageMobject
import os

module_dir = os.path.dirname(__file__)
parent_module_dir = os.path.dirname(module_dir)
data_dir = os.path.join(parent_module_dir, 'images')

class ChessPiece(Mobject):    
    def __init__(self, color: ManimColor, piece_name: str, path="", **kwargs):
        """
        Initializes a ChessPiece object with the specified color and piece name.

        Args:
            color (ManimColor): The color of the chess piece (WHITE or BLACK).
            piece_name (str): The name of the chess piece (e.g., "pawn", "king").
            path (str, optional): The file path to the piece image. Defaults to an empty string.
            **kwargs: Additional keyword arguments for the Mobject superclass.
        """
        super().__init__(**kwargs)
        self.color = color
        if str(color)=="#FFFFFF":
            color_str = "white"
        else:
            color_str = "black"

        default_path = os.path.join(data_dir, f"{color_str}-{piece_name}")
        self.add(ImageMobject(path or default_path).scale(0.5))


class Pawn(ChessPiece):
    def __init__(self, color: ManimColor, path="", **kwargs):
        """
        Initializes a Pawn object with the specified color and image path.
        Args:
            color (ManimColor): The color of the pawn (WHITE or BLACK).
            path (str, optional): The file path to the pawn image. Defaults to an empty string.
            **kwargs: Additional keyword arguments for the ChessPiece superclass.
        """
        super().__init__(color, "pawn", path, **kwargs)

class King(ChessPiece):
    def __init__(self, color, path="", **kwargs):
        """
        Initializes a King object with the specified color and image path.

        Args:
            color (str): The color of the king (WHITE or BLACK).
            path (str, optional): The file path to the king image. Defaults to an empty string.
            **kwargs: Additional keyword arguments for the ChessPiece superclass.
        """
        super().__init__(color, "king", path, **kwargs)

class Queen(ChessPiece):
    def __init__(self, color, path="", **kwargs):
        """
        Initializes a Queen object with the specified color and image path.

        Args:
            color (str): The color of the queen (WHITE or BLACK).
            path (str, optional): The file path to the queen image. Defaults to an empty string.
            **kwargs: Additional keyword arguments for the ChessPiece superclass.
        """
        super().__init__(color, "queen", path, **kwargs)

class Knight(ChessPiece):
    def __init__(self, color, path="", **kwargs):
        """
        Initializes a Knight object with the specified color and image path.

        Args:
            color (str): The color of the knight (WHITE or BLACK).
            path (str, optional): The file path to the knight image. Defaults to an empty string.
            **kwargs: Additional keyword arguments for the ChessPiece superclass.
        """
        super().__init__(color, "knight", path, **kwargs)

class Bishop(ChessPiece):
    def __init__(self, color, path="", **kwargs):
        """
        Initializes a Bishop object with the specified color and image path.

        Args:
            color (str): The color of the bishop (WHITE or BLACK).
            path (str, optional): The file path to the bishop image. Defaults to an empty string.
            **kwargs: Additional keyword arguments for the ChessPiece superclass.
        """
        super().__init__(color, "bishop", path, **kwargs)

class Rook(ChessPiece):
    def __init__(self, color, path="", **kwargs):
        """
        Initializes a Rook object with the specified color and image path.

        Args:
            color (str): The color of the rook (WHITE or BLACK).
            path (str, optional): The file path to the rook image. Defaults to an empty string.
            **kwargs: Additional keyword arguments for the ChessPiece superclass.
        """
        super().__init__(color, "rook", path, **kwargs)
