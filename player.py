"""Implementation of the Player class"""

class Player:
    """A player in the tic tac toe game."""

    def __init__(
        self, symbol: str, winning_combinations: set[tuple[int, ...]] = set()
    ) -> None:
        """Initialize a new player.

        Args:
            symbol (str): Symbol to represent the player.
            winning_combinations (list[list[int]], optional): List of all the
                combinations the player can win by. Defaults to [].
        """
        # Either 'X' or 'O' or any other symbol a player chooses.
        self.symbol = symbol

        # List of all combinations that the player can win by
        self.winning_combinations = winning_combinations

        # Set of the positions a player has picked.
        self.positions: set[int] = set()

    def update_positions(self, new_position: int) -> None:
        """Update the positions a player has picked.

        Args:
            new_position (int): New position that the player has picked.
        """
        self.positions.add(new_position - 1)

    def filter_winning_combinations(self, choice: int) -> None:
        """Filter winning combinations after the other player has played.
        Removes any combinations that have the choice selected by other player.

        Args:
            choice (int): Position selected by other player.
        """
        choice -= 1

        self.winning_combinations = set(
            filter(lambda x: choice not in x, self.winning_combinations)
        )

    def check_win(self) -> bool:
        """Check if player has won.
        Checks to see if a winning combination is among the player's picked
        positions.

        Returns:
            bool: True if player has won, otherwise False.
        """
        for combination in self.winning_combinations:
            if not set(combination).difference(self.positions):
                return True

        return False
