"""Implements the Computer class"""

from collections import defaultdict
from typing import Literal
import random

from player import Player


class Computer(Player):
    """Computer player."""

    def __init__(
        self, symbol: str, winning_combinations: set[tuple[int, ...]] = set()
    ) -> None:
        super().__init__(symbol, winning_combinations)

    def next_move(self, other_player: Player, choices: list[int]) -> int:
        """Determine the next position that the computer will play.

        Args:
            other_player (Player): Player the computer is playing against.
            choices (list[int]): List of available choices the computer can make.

        Returns:
            int: Computer's next position.
        """

        computer_moves = self._computer_next_positions([i - 1 for i in choices])
        other_player_moves = self._other_player_next_positions(other_player)

        # Take highest weight for each possible move
        best_moves = self.combine_dicts(computer_moves, other_player_moves)
        max_weight = max(list(best_moves.values()))

        next_moves = []
        for pos, weight in best_moves.items():
            if weight == max_weight:
                next_moves.append(pos)

        return random.choice(next_moves) + 1

    def _computer_next_positions(
        self, available_positions: list[int]
    ) -> dict[int, float]:
        """Calculate the weights of the computer's possible next moves.
        These moves are based on the available positions and how close
        the position is to making a win.

        Args:
            `available_positions (list[int])`: List of available positions that
                the computer can play into.

        Returns:
            `dict[int, float]`: A dictionary of each possible move and its weight.
        """

        possible_next_positions: dict[int, float] = defaultdict(
            self.default_int
        )

        for comb in self.winning_combinations:
            # Positions that have not been played by either player or computer
            # in the current winning combination
            not_played = set(comb).intersection(available_positions)
            not_played_size = len(not_played)

            # Positions that have been played by the computer in the current
            # winning combination
            comp_played = set(comb).intersection(self.positions)
            comp_played_size = len(comp_played)

            while len(not_played) > 0:
                # weight = (size of board / not_played_size) * comp_played_size
                possible_next_positions[not_played.pop()] += (
                    len(comb) / not_played_size
                ) * comp_played_size

        return possible_next_positions

    def _other_player_next_positions(
        self, other_player: Player
    ) -> dict[int, float]:
        """Compute the weights of the other player's most likely next positions.
        These positions help stop player from making a winning move or a move
        that allows them to gain an advantage over the computer.

        ```Text
        For example:
            +---+---+---+
            | X |   |   |
            +---+---+---+
            |   | O |   |
            +---+---+---+
            |   | X |   |
            +---+---+---+

            In the case above, the computer will play box 7 (indexed from 1)
            preventing the player from creating a double pivot scenario that
            would see the player win in the next move.

        ```
        Args:
            `other_player (Player)`: Player that the computer is playing against.

        Returns:
            `dict[int, float]`: A dictionary of the other player's next moves and
                their weights.
        """

        # Differences between other player's winning combination and the positions
        # that they have already played.
        # Key: Length of the difference
        # Value: List of all positions that were in a difference of same length
        diffs: dict[int, list[int]] = defaultdict(self.default_list)

        max_len = 0  # Max length of the differences
        board_size = 0  # Size of the board

        for comb in other_player.winning_combinations:
            diff = set(comb).difference(other_player.positions)
            if max_len < len(diff):
                max_len = len(diff)

            diffs[len(diff)].extend(diff)

            if board_size == 0:
                board_size = len(comb)

        other_player_next_positions: dict[int, float] = defaultdict(
            self.default_int
        )
        for key, value in diffs.items():
            for pos in value:
                # weight = max length of the differences / key
                other_player_next_positions[pos] += max_len / key

                # If the position is a winning position
                if key == 1:
                    other_player_next_positions[pos] *= board_size

        return other_player_next_positions

    @staticmethod
    def combine_dicts(a: dict, b: dict) -> dict:
        """Combine two dictionaries. If a key is found in both dictionaries
        the larger value is used.

        Args:
            a (dict): First dictionary
            b (dict): Second dictionary

        Returns:
            dict: A dictionary containing keys from both a and b with the
                largest value for each key.
        """
        return {
            **a,
            **b,
            **{k: a[k] if a[k] > b[k] else b[k] for k in a.keys() & b},
        }

    @staticmethod
    def default_int() -> Literal[0]:
        """Factory for default value of a defaultdict whose values are ints.
        Default value is `0`.
        """
        return 0

    @staticmethod
    def default_list() -> list:
        """Factory for default value of a defaultdict whose values are lists.
        Default value is `[]`.
        """
        return []
