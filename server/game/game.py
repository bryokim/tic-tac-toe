"""Implements the Game class"""

from .gameboard import GameBoard
from .player import Player


class Game:
    def __init__(self, game_id: str, players: list[Player]) -> None:
        """Initialize a new game

        Args:
            game_id (str): id of the game. Used as room in socketio
            players (list[Player]): Players in the game
        """
        self.game_id = game_id
        self.board: GameBoard | None = None

        self.scoreboard = {"total": 0, "X": 0, "O": 0, "tie": 0}

        self._status: int = 0
        self._turn: str = "X"

        self.player_X, self.player_O = players
        self.players = {
            self.player_X.sid: self.player_X,
            self.player_O.sid: self.player_O,
        }

        self.replay_confirmed = 0

    def init(self, size: int = 3):
        """Start a new game

        Args:
            size (int, optional): Size of the board. Defaults to 3.
        """
        self._status = 1
        self._turn = "X"
        self.replay_confirmed = 0

        self.board = GameBoard(size, size)
        self.player_O.winning_combinations = self.board.combinations
        self.player_X.winning_combinations = self.board.combinations

    def toggle_turn(self):
        """Change turn"""
        self._turn = "X" if self._turn == "O" else "O"

    def confirm_replay(self):
        """Confirm game replay"""
        self.replay_confirmed = 1

    def make_move(
        self,
        current_player: Player,
        number_picked: int,
    ) -> bool:
        """Play with the number picked.

        Args:
            current_player (Player): Current player making play
            number_picked (int): Number of the box the current_player has picked.
                Indexed from 1.

        Returns:
            bool: `True` if the current_player has won, else `False`.
        """

        other_player = (
            self.player_O if current_player.symbol == "X" else self.player_X
        )

        if self.board and number_picked in self.board.choices:
            self.board.modify_board(number_picked, current_player.symbol)
            current_player.update_positions(number_picked)

            # Remove combination with number picked from other player's possible
            # winning combinations
            other_player.filter_winning_combinations(number_picked)

            if current_player.is_winner():
                self._status = 3

            if self.is_draw():
                self._status = 2

            return True

        return False

    def is_draw(self) -> bool:
        """Check whether the game is  draw.

        Returns:
            bool: `True` if the game is draw, else `False`.
        """
        return (len(self.board.choices) == 0 and self._status == 1) or (
            len(self.player_X.winning_combinations) == 0
            and len(self.player_O.winning_combinations) == 0
        )

    def update_scoreboard(self, winner: str):
        """Updates scoreboard after game ends.

        Args:
            winner (str): Either `X`, `O` or `tie`
        """
        self.scoreboard["total"] += 1
        self.scoreboard[winner] += 1

    def progress(self):
        """Returns the board"""
        return self.board.board if isinstance(self.board, GameBoard) else []

    def reset(self):
        """Resets a game"""
        self.board.clear()
        self._status = 0
        self.player_O.reset()
        self.player_X.reset()
