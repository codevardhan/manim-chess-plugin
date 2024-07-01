from manim import *
import chess
import os

# Define paths relative to the current file
module_dir = os.path.dirname(__file__)
parent_module_dir = os.path.dirname(module_dir)

data_dir = os.path.join(parent_module_dir, 'images')


class ChessBoard(Group):
    def __init__(self, square_colors=(WHITE, GREEN), line_color=BLACK, strict_mode=True):
        super().__init__()

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

    def position_squares(self):
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
        color1, color2 = self.square_colors
        for row in 'abcdefgh':
            for col in range(1, 9):
                color = color2 if col % 2 == 1 else color1
                self.squares[f'{row}{col}'].set_fill(color, opacity=0.7)
            color1, color2 = color2, color1

    def add_labels(self):
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
        self.board = Group(*self.squares.values(), *
                           self.labels, *self.elements)
        self.add(self.board)

    def add_element(self, position: str, piece_mobject: Mobject):
        index = self.position_to_index(position)
        square_position = self.squares[position].get_center()
        piece = piece_mobject.move_to(square_position)
        self.elements[index] = piece
        self.group_elements()

    def initialize_board(self, invert=False):
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

    def handle_castling(self, move: chess.Move):
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

    def move_piece(self, move: chess.Move):
        start_pos = move[0:2]
        end_pos = move[2:]

        start_index = self.position_to_index(start_pos)
        end_index = self.position_to_index(end_pos)
        end_square = self.squares[end_pos].get_center()

        # Move using python-chess
        move = chess.Move.from_uci(move)

        if move in self.chessboard.legal_moves or self.strict_mode:
            # Handle en passant
            if move in self.chessboard.pseudo_legal_moves and self.chessboard.is_en_passant(move):
                return self.handle_en_passant(move)
            # Handle castling
            elif move.uci() in ['e1g1', 'e1c1', 'e8g8', 'e8c8']:
                return self.handle_castling(move)
            else:
                self.chessboard.push(move)

                piece = self.elements[start_index]
                target_piece = self.elements[end_index]

                animations = []

                # Check if there's a piece at the end position
                if target_piece != Mobject():
                    # Add special capture animation
                    capture_animation = FadeOut(target_piece)
                    animations.append(capture_animation)

                self.elements[end_index] = piece
                self.elements[start_index] = Mobject()

                move_animation = piece.animate.move_to(end_square)
                animations.append(move_animation)

                return AnimationGroup(*animations)
        else:
            raise ValueError(f"Invalid move: {move}")


class Pawn(Mobject):
    def __init__(self, color, path="", **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.createpiece(path)

    def createpiece(self, path):
        if self.color == WHITE:
            path = path if path != "" else os.path.join(data_dir, "white-pawn")
            self.add(ImageMobject(path).scale(0.5))
        else:
            path = path if path != "" else os.path.join(data_dir, "black-pawn")
            self.add(ImageMobject(path).scale(0.5))


class King(Mobject):
    def __init__(self, color, path="", **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.createpiece(path)

    def createpiece(self, path):
        if self.color == WHITE:
            path = path if path != "" else os.path.join(data_dir, "white-king")
            self.add(ImageMobject(path).scale(0.5))
        else:
            path = path if path != "" else os.path.join(data_dir, "black-king")
            self.add(ImageMobject(path).scale(0.5))


class Queen(Mobject):
    def __init__(self, color, path="", **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.createpiece(path)

    def createpiece(self, path):
        if self.color == WHITE:
            path = path if path != "" else os.path.join(
                data_dir, "white-queen")
            self.add(ImageMobject(path).scale(0.5))
        else:
            path = path if path != "" else os.path.join(
                data_dir, "black-queen")
            self.add(ImageMobject(path).scale(0.5))


class Knight(Mobject):
    def __init__(self, color, path="", **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.createpiece(path)

    def createpiece(self, path):
        if self.color == WHITE:
            path = path if path != "" else os.path.join(
                data_dir, "white-knight")
            self.add(ImageMobject(path).scale(0.5))
        else:
            path = path if path != "" else os.path.join(
                data_dir, "black-knight")
            self.add(ImageMobject(path).scale(0.5))


class Bishop(Mobject):
    def __init__(self, color, path="", **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.createpiece(path)

    def createpiece(self, path):
        if self.color == WHITE:
            path = path if path != "" else os.path.join(
                data_dir, "white-bishop")
            self.add(ImageMobject(path).scale(0.5))
        else:
            path = path if path != "" else os.path.join(
                data_dir, "black-bishop")
            self.add(ImageMobject(path).scale(0.5))


class Rook(Mobject):
    def __init__(self, color, path="", **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.createpiece(path)

    def createpiece(self, path):
        if self.color == WHITE:
            path = path if path != "" else os.path.join(data_dir, "white-rook")
            self.add(ImageMobject(path).scale(0.5))
        else:
            path = path if path != "" else os.path.join(data_dir, "black-rook")
            self.add(ImageMobject(path).scale(0.5))


# class ChessScene(Scene):
#     def construct(self):
#         chessboard = ChessBoard()
#         chessboard.initialize_board()
#         self.add(chessboard.board)
#         self.wait(2)


# if __name__ == "__main__":
#     scene = ChessScene()
#     scene.render()
