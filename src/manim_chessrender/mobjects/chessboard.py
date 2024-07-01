from manim import *
import chess, chess.pgn
import os

# Define paths relative to the current file
module_dir = os.path.dirname(__file__)
parent_module_dir = os.path.dirname(module_dir)

data_dir = os.path.join(parent_module_dir, 'images')


class ChessBoard(Group):
    """
    A class representing a chessboard with pieces.

    Attributes:
        elements (list): A list containing the Mobject instances for the 64 squares.
        square_colors (tuple): A tuple containing the colors of the squares.
        line_color (color): The color of the lines.
        strict_mode (bool): A flag for strict mode.
        squares (dict): A dictionary mapping positions to their respective Square objects.
        chessboard (chess.Board): A chess board object from the python-chess library.
    """
    
    def __init__(self, square_colors=(WHITE, GREEN), line_color=BLACK, strict_mode=True, **kwargs):
        """
        Initializes the ChessBoard with the given square colors, line color, and strict mode flag.

        Args:
            square_colors (tuple, optional): Colors of the squares. Defaults to (WHITE, GREEN).
            line_color (color, optional): Color of the lines. Defaults to BLACK.
            strict_mode (bool, optional): Flag for strict mode. Defaults to True.
            **kwargs: Additional keyword arguments passed to the Group superclass.
        """
        super().__init__(**kwargs)

        self.elements = [Mobject() for _ in range(64)]
        self.square_colors = square_colors
        self.line_color = line_color
        self.strict_mode = strict_mode
        self.squares = {f'{row}{col}': Square(stroke_color=line_color).scale(0.5)
                        for row in 'abcdefgh' for col in range(1, 9)}

        self.chessboard = chess.Board()
        self.position_squares()
        self.color_squares()
        self.add_labels()
        self.group_elements()

    def position_squares(self):
        """
        Positions the squares on the board in their correct locations.
        """
        self.squares['e5'].move_to(UP * 0.5 + RIGHT * 0.5)

        for i in range(4, 0, -1):
            self.squares[f'e{i}'].next_to(
                self.squares[f'e{i + 1}'], DOWN, buff=0)
        for i in range(6, 9):
            self.squares[f'e{i}'].next_to(
                self.squares[f'e{i - 1}'], UP, buff=0)

        for row in 'dcba':
            self.squares[f'{row}1'].next_to(
                self.squares[f'{chr(ord(row) + 1)}1'], LEFT, buff=0)
        for row in 'fg':
            self.squares[f'{row}1'].next_to(
                self.squares[f'{chr(ord(row) - 1)}1'], RIGHT, buff=0)
        self.squares['h1'].next_to(self.squares['g1'], RIGHT, buff=0)

        for row in 'abcdefgh':
            for col in range(2, 9):
                self.squares[f'{row}{col}'].next_to(
                    self.squares[f'{row}{col - 1}'], UP, buff=0)

    def color_squares(self):
        """
        Colors the squares on the board in a checkerboard pattern.
        """
        color1, color2 = self.square_colors
        for row in 'abcdefgh':
            for col in range(1, 9):
                color = color2 if col % 2 == 1 else color1
                self.squares[f'{row}{col}'].set_fill(color, opacity=0.7)
            color1, color2 = color2, color1

    def add_labels(self):
        """
        Adds labels to the squares on the board indicating ranks and files.
        """
        self.labels = []
        color1, color2 = self.square_colors
        for idx, letter in enumerate('abcdefgh'):
            color = color2 if idx % 2 == 1 else color1
            self.labels.append(Text(letter, font="Ubuntu Mono", color=color).move_to(
                self.squares[f'{letter}1'].get_center() + DOWN * 0.35 + RIGHT * 0.35).scale(0.3))
        for idx in range(1, 9):
            color = color1 if idx % 2 == 1 else color2
            self.labels.append(Text(str(idx), font="Ubuntu Mono", color=color).move_to(
                self.squares[f'a{idx}'].get_center() + UP * 0.35 + LEFT * 0.35).scale(0.3))

    def group_elements(self):
        """
        Groups all the squares, labels, and elements into a single group and adds it to the board.
        """
        self.board = Group(*self.squares.values(), *
                           self.labels, *self.elements)
        self.add(self.board)

    def index_to_position(self, index: int) -> str:
        """
        Convert an index (0-63) to a chess board position ('a1' to 'h8').

        Args:
        index (int): The index to convert, should be in the range 0-63.

        Returns:
        str: The corresponding chess board position.
        """
        if not 0 <= index < 64:
            raise ValueError("Index must be between 0 and 63")
        row = index // 8
        col = index % 8
        return chr(col + ord('a')) + str(row + 1)

    def position_to_index(self, position: str) -> int:
        """
        Convert a chess board position ('a1' to 'h8') to an index (0-63).

        Args:
        position (str): The position to convert, should be in the format 'a1' to 'h8'.

        Returns:
        int: The corresponding index.
        """
        if len(position) != 2 or position[0] not in 'abcdefgh' or position[1] not in '12345678':
            raise ValueError("Position must be in the format 'a1' to 'h8'")
        col = ord(position[0]) - ord('a')
        row = int(position[1]) - 1
        return row * 8 + col

    def add_element(self, position: str, piece_mobject: Mobject):
        """
        Adds a chess piece to the board at the specified position.

        Args:
            position (str): The board position (e.g., 'e4').
            piece_mobject (Mobject): The graphical object representing the chess piece.
        """
        index = self.position_to_index(position)
        square_position = self.squares[position].get_center()
        piece = piece_mobject.move_to(square_position)
        self.elements[index] = piece
        self.group_elements()
  
    def handle_castling(self, move: chess.Move):
        """
        Handles castling moves on the board.

        Args:
            move (chess.Move): A move object representing the castling move.

        Returns:
            AnimationGroup: An animation group showing the castling move.
        """
        # Execute castling move
        self.chessboard.push(move)
        animations = []

        # Update positions of rook and king on the board
        if move.to_square == chess.G1:  # Kingside castling
            rook_start = chess.H1
            rook_end = chess.F1
            king_start = chess.E1
            king_end = chess.G1
        elif move.to_square == chess.C1:  # Queenside castling
            rook_start = chess.A1
            rook_end = chess.D1
            king_start = chess.E1
            king_end = chess.C1
        elif move.to_square == chess.G8:  # Kingside castling for Black
            rook_start = chess.H8
            rook_end = chess.F8
            king_start = chess.E8
            king_end = chess.G8
        elif move.to_square == chess.C8:  # Queenside castling for Black
            rook_start = chess.A8
            rook_end = chess.D8
            king_start = chess.E8
            king_end = chess.C8
        else:
            return   # Invalid castling move

        # Move the rook on the board
        rook_start_index = self.position_to_index(
            chess.square_name(rook_start))
        rook_end_index = self.position_to_index(chess.square_name(rook_end))
        rook = self.elements[rook_start_index]
        rook_end_square = self.squares[chess.square_name(
            rook_end)].get_center()
        rook_move_animation = rook.animate.move_to(rook_end_square)
        animations.append(rook_move_animation)
        self.elements[rook_end_index] = rook
        self.elements[rook_start_index] = Mobject()

        # Move the king on the board
        king_start_index = self.position_to_index(
            chess.square_name(king_start))
        king_end_index = self.position_to_index(chess.square_name(king_end))
        king = self.elements[king_start_index]
        king_end_square = self.squares[chess.square_name(
            king_end)].get_center()
        king_move_animation = king.animate.move_to(king_end_square)
        animations.append(king_move_animation)
        self.elements[king_end_index] = king
        self.elements[king_start_index] = Mobject()

        return AnimationGroup(*animations)

    def handle_en_passant(self, move: chess.Move):
        """
        Handles en passant captures on the board.

        Args:
            move (chess.Move): A move object representing the en passant capture.

        Returns:
            AnimationGroup: An animation group showing the en passant capture.

        Raises:
            ValueError: If the move is not a valid en passant capture.
        """
        animations = []

        # Remove the captured pawn from the board
        if move.to_square == self.chessboard.ep_square:
            # Execute en passant move
            self.chessboard.push(move)

            if self.chessboard.turn == chess.WHITE:
                captured_square = chess.square(
                    chess.square_file(move.to_square), 3)
            else:
                captured_square = chess.square(
                    chess.square_file(move.to_square), 4)

            captured_square_index = self.position_to_index(
                chess.square_name(captured_square))
            captured_piece = self.elements[captured_square_index]

            capture_animation = FadeOut(captured_piece)
            animations.append(capture_animation)

            # Animating the capturing pawn move
            start_square = chess.square_name(move.from_square)
            end_square = chess.square_name(move.to_square)
            start_index = self.position_to_index(start_square)
            end_index = self.position_to_index(end_square)

            capturing_piece = self.elements[start_index]
            end_square_center = self.squares[end_square].get_center()
            move_animation = capturing_piece.animate.move_to(end_square_center)
            animations.append(move_animation)

            # Remove captured piece from elements list and board
            self.elements[captured_square_index] = Mobject()
            self.chessboard.remove_piece_at(captured_square)

            return AnimationGroup(*animations)
        else:
            raise ValueError(f"Invalid move: {move}")

    def handle_promotion(self, move: chess.Move):
        """
        Handles pawn promotion moves on the board.

        Args:
            move (chess.Move): A move object representing the pawn promotion move.

        Returns:
            AnimationGroup: An animation group showing the pawn promotion.

        Raises:
            ValueError: If the move is not a valid promotion move.
        """
        animations = []

        # Execute promotion move
        self.chessboard.push(move)

        # Get end position of the promotion
        start_pos = chess.square_name(move.from_square)
        start_index = self.position_to_index(start_pos)
        pawn_piece = self.elements[start_index]
        
        end_pos = chess.square_name(move.to_square)
        end_index = self.position_to_index(end_pos)
        end_square = self.squares[end_pos].get_center()
        
        # Replace the pawn with the promoted piece
        # TODO: make promotion animation smoother
         
        promotion_piece = {
            '5': Queen, '4': Rook, '3': Bishop, '2': Knight
        }.get(str(move.promotion), Queen)(pawn_piece.color)
        
        promotion_animation = pawn_piece.animate.move_to(end_square)
        animations.append(promotion_animation)

        capture_animation = FadeOut(pawn_piece)
        animations.append(capture_animation)
        
        promotion_piece.move_to(end_square)
        final_animation = FadeIn(promotion_piece)
        animations.append(final_animation)
        
        self.elements[end_index] = promotion_piece
        return AnimationGroup(*animations)
    
    def execute_move(self, move: str):
        """
        Moves a piece on the board according to the given UCI move string.

        Args:
            move (str): The UCI string representing the move (e.g., 'e2e4').

        Returns:
            AnimationGroup: An animation group showing the move.

        Raises:
            ValueError: If the move is invalid.
        """
        
        # Move using python-chess
        move = chess.Move.from_uci(move)
        if not (move in self.chessboard.legal_moves or self.strict_mode):
            raise ValueError(f"Invalid move: {move}")
        
        start_pos = chess.square_name(move.from_square)
        end_pos = chess.square_name(move.to_square)
        
        start_index = self.position_to_index(start_pos)
        end_index = self.position_to_index(end_pos)
        end_square = self.squares[end_pos].get_center()
            
        # Handle pawn promotion
        if move.promotion:
            return self.handle_promotion(move)
    
        # Handle special moves (en passant or castling)
        if move in self.chessboard.pseudo_legal_moves:
            if self.chessboard.is_en_passant(move):
                return self.handle_en_passant(move)
            elif move.uci() in ['e1g1', 'e1c1', 'e8g8', 'e8c8']:
                return self.handle_castling(move)

    
        self.chessboard.push(move)

        piece = self.elements[start_index]
        target_piece = self.elements[end_index]

        animations = []

        # Check if there's a piece at the end position
        if target_piece != Mobject():
            animations.append(FadeOut(target_piece))

        self.elements[end_index] = piece
        self.elements[start_index] = Mobject()

        move_animation = piece.animate.move_to(end_square)
        animations.append(move_animation)
        
        if self.chessboard.is_checkmate():
            # Perform checkmate animation
            checkmate_text = Text("Checkmate!", font="Ubuntu Mono").scale(1.5)
            checkmate_text.move_to(self.board.get_center())
            animations.append(FadeIn(checkmate_text))
        elif self.chessboard.is_stalemate():
            # Perform stalemate animation
            stalemate_text = Text("Stalemate!", font="Ubuntu Mono").scale(1.5)
            stalemate_text.move_to(self.board.get_center())
            animations.append(FadeIn(stalemate_text))

        return AnimationGroup(*animations)

    def initialize_board(self, invert=False):
        """
        Initializes the chessboard with the standard piece positions.

        Args:
            invert (bool, optional): If True, inverts the board by switching the colors of the pieces.
                                    Defaults to False.

        This method sets up the chessboard by placing pawns, rooks, knights, bishops, the queen, and the king
        in their standard starting positions. The color of the pieces can be inverted by setting the `invert`
        parameter to True.
        """
        pieces = [
            (Rook, 'a1'), (Knight, 'b1'), (Bishop, 'c1'),
            (Queen, 'd1'), (King, 'e1'), (Bishop, 'f1'),
            (Knight, 'g1'), (Rook, 'h1')
        ]
        clr1, clr2 = (WHITE, BLACK) if not invert else (BLACK, WHITE)

        for letter in 'abcdefgh':
            position = f"{letter}2"
            index = self.position_to_index(position)
            pawn = Pawn(clr1).move_to(self.squares[position].get_center())
            self.elements[index] = pawn

        for piece, position in pieces:
            chess_piece = piece(clr1).move_to(
                self.squares[position].get_center())
            index = self.position_to_index(position)
            self.elements[index] = chess_piece

        for letter in 'abcdefgh':
            position = f"{letter}7"
            index = self.position_to_index(position)
            pawn = Pawn(clr2).move_to(self.squares[position].get_center())
            self.elements[index] = pawn

        for piece, position in pieces:
            new_position = position.replace('1', '8')
            chess_piece = piece(clr2).move_to(
                self.squares[new_position].get_center())
            index = self.position_to_index(new_position)
            self.elements[index] = chess_piece
        self.group_elements()

    def load_fen(self, fen):
        """
        Load a board position from a FEN string.
        """
        self.elements = [Mobject() for _ in range(64)]
        
        rows = fen.split()[0].split('/')
        piece_map = {
            'r': Rook, 'n': Knight, 'b': Bishop, 'q': Queen, 'k': King, 'p': Pawn,
            'R': Rook, 'N': Knight, 'B': Bishop, 'Q': Queen, 'K': King, 'P': Pawn
        }
        colors = {
            'r': BLACK, 'n': BLACK, 'b': BLACK, 'q': BLACK, 'k': BLACK, 'p': BLACK,
            'R': WHITE, 'N': WHITE, 'B': WHITE, 'Q': WHITE, 'K': WHITE, 'P': WHITE
        }

        for rank_index, row in enumerate(rows):
            file_index = 0
            for char in row:
                if char.isdigit():
                    file_index += int(char)
                else:
                    position = f"{chr(ord('a') + file_index)}{8 - rank_index}"
                    piece_class = piece_map[char]
                    color = colors[char]
                    chess_piece = piece_class(color).move_to(self.squares[position].get_center())
                    index = self.position_to_index(position)
                    self.elements[index] = chess_piece
                    file_index += 1
        
        self.group_elements()
      
    def load_pgn(self, pgn_path):
        """
        Load all games from a PGN file and return a list of move arrays for each game.

        Args:
            pgn_path (str): The path to the PGN file.

        Returns:
            list: A list of move arrays, each representing the moves of a single game.
        """
        games = []
        with open(pgn_path) as pgn_file:
            while True:
                game = chess.pgn.read_game(pgn_file)
                if game is None:
                    break
                games.append(list(game.mainline_moves()))
        return games

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
