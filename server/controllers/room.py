"""Implements RoomController class"""

from uuid import uuid4

from utils.constants import ROOM_PREFIX
from game.game import Game
from game.player import Player


class RoomController:
    """Manage the player's rooms"""

    def __init__(self):
        """Initialize a new RoomController"""
        self.ongoing = {}

    def create(self, players: list[Player]) -> Game:
        """Creates a new game that is assigned its own room

        Args:
            players (list[Player]): Two players.

        Returns:
            Game: The created Game instance that the players will use
        """
        game = Game(f"{ROOM_PREFIX}{uuid4().hex}", players)

        self.ongoing[game.game_id] = game

        return game

    def get_room(self, game_id: str) -> Game | None:
        """Gets a room assigned to specified game_id

        Args:
            game_id (str): id assigned to a game

        Returns:
            Game | None: A Game instance if one exists with given id.
        """
        return self.ongoing.get(game_id)

    def remove(self, game_id: str) -> None:
        """Removes a game.

        Args:
            game_id (str): id of the game to remove
        """
        try:
            self.ongoing.pop(game_id)
        except KeyError:
            pass
