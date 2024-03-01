"""Implements the Player class"""

class Player:
    def __init__(
        self,
        sid: str,
        username: str,
        symbol: str = '',
        winning_combinations: set[tuple[int, ...]] = set(),
    ) -> None:
        """Initialize a new player.

        Args:
            sid (str): socketio session id of the player
            username (str): player's username
            symbol (str): Symbol to represent the player. Defaults to empty
                string.
            winning_combinations (set[tuple[int]], optional): Set of all the
                combinations the player can win by. Defaults to empty set.
        """

        self.sid = sid
        self.username = username
        self.symbol = symbol
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

    def is_winner(self) -> bool:
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

    def reset(self) -> None:
        """Resets a player's positions and winning_combinations"""
        self.positions = set()
        self.winning_combinations = set()
