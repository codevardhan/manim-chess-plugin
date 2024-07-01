# Manim Chessboard

A Manim plugin that allows you to generate scenes with chessboards with minimal setup.


## Installation

```bash
pip install manim-chessrender
```

## Features

- **Initialize Chessboard**: Easily create and display a fully initialized chessboard.
- **Move Pieces**: Animate standard piece movements using UCI notation.
- **Special Moves**: Handle special chess moves like castling and en passant.
- **Load FEN Strings**: Load and display a board configuration from a FEN string.
- **Play PGN Files**: Load and animate moves from PGN files.
- **Customization**: Customize the appearance of the chessboard and pieces with different colors and image paths.


## Usage

To render the examples, you need to run the script using Manim. Below are the examples included in this project.


### MovePieceExample
This example initializes the chessboard and demonstrates moving a piece.

```python

class MovePieceExample(MovingCameraScene):
    """
    Scene to demonstrate moving a piece on the chessboard.
    """
    def construct(self):
        """
        Constructs the scene by initializing the chessboard and moving a piece.
        """
        chessboard = ChessBoard()
        chessboard.initialize_board()
        self.add(chessboard.board)
        self.wait(1)
        self.play(chessboard.execute_move('e2e4'))
        self.wait(2)
```

### PlayPGNExample
This example demonstrates playing moves from a PGN file on the chessboard.

```python

class PlayPGNExample(MovingCameraScene):
    """
    Scene to demonstrate playing moves from a PGN file on the chessboard.
    """
    def construct(self):
        """
        Constructs the scene by loading a PGN file and animating the moves on the chessboard.
        """
        chessboard = ChessBoard()
        chessboard.initialize_board()
        self.add(chessboard.board)
        self.wait(1)
        
        games = chessboard.load_pgn("./example/example.pgn")
        game = games[0]
        for move in game:
            self.play(chessboard.execute_move(move.uci()))
            self.wait(0.5)
```

### Running the Examples
To run any of the examples, execute the script using Manim. For instance, to run the `InitializeChessBoard` example:

```sh
manim -pql examples.py InitializeChessBoard
```

Replace `InitializeChessBoard` with the class name of the example you want to run.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.
