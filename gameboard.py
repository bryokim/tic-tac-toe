"""Implementation of the GameBoard class"""

class GameBoard:
    """GameBoard for tic tac toe game"""

    def __init__(self, rows: int = 3, cols: int = 3) -> None:
        """Initialize a new GameBoard.

        Args:
            rows (int, optional): Number of rows in the board. Defaults to 3
            cols (int, optional): Number of columns in the board. Defaults to 3
        """
        self.rows = rows
        self.cols = cols

        # Range of numbers that the player can pick to play.
        self.choices: list[int] = list(range(1, (rows * cols) + 1))

        # Board filled with spaces
        self.board: list[list[str]] = [
            [" " for _ in range(cols)] for _ in range(rows)
        ]

        # Combinations along the rows
        self.row_combinations = [
            list(range(cols * row, cols * (row + 1))) for row in range(rows)
        ]

        # Combinations along the columns
        self.col_combinations = [
            list(range(col, cols * rows, cols)) for col in range(cols)
        ]

        # Combinations along the diagonals
        self.cross_combinations = [
            [(cols * row) + row for row in range(rows)],
            [
                (cols * row) + i
                for i, row in enumerate(range(rows - 1, -1, -1))
            ],
        ]

        # All combinations
        self.combinations: set[tuple[int, ...]] = {
            tuple(y)
            for x in [
                self.row_combinations,
                self.col_combinations,
                self.cross_combinations,
            ]
            for y in x
        }

    def print_board(self) -> None:
        """Print the board"""

        for row in range(self.rows):
            print("\n", "+---" * self.cols, "+\n|", end="", sep="")

            for col in range(self.cols):
                print(f" {self.board[row][col]} |", end="")

        print("\n", "+---" * self.cols, "+", sep="")

    def modify_board(self, choice: int, symbol: str) -> None:
        """Label the position picked with the player's symbol.
        The position picked is removed from the available choices.

        Args:
            choice (int): Position picked to be filled.
            symbol (str): Symbol signifying current player.
        """
        index = choice - 1

        x = index // self.rows  # Row to modify
        y = index % self.cols  # Column to modify

        self.board[x][y] = symbol

        # Remove choice that has been made
        self.choices.remove(choice)

    def filled(self) -> bool:
        """Check if there are any more positions not yet played on the board.

        Returns:
            bool: True if the board has no empty positions, False otherwise.
        """
        return len(self.choices) == 0
