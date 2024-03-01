"""Implements UserController class"""

from game.player import Player


class UserController:
    """Manage users/players"""

    def __init__(self):
        """Initialize a new UserController"""

        self.queue: list[Player] = []
        self.players: dict[str, Player] = {}

    def get_queue_size(self):
        """Returns length of the queue"""
        return len(self.queue)

    def add_to_store(self) -> list[Player]:
        """Removes two players from queue

        Returns:
            list[Player]: players from the queue
        """
        two_players = self.queue[:2]
        self.queue = self.queue[2:]

        player_X, player_O = two_players
        self.players[player_X.sid] = player_X
        self.players[player_O.sid] = player_O

        return two_players

    def add_to_queue(self, sid: str, username: str) -> None:
        """Adds a player to the queue

        Args:
            sid (str): socketio session id of the player
            username (str): player's username
        """
        player = Player(sid, username)

        self.queue.append(player)

    def get_player(self, sid: str) -> Player | None:
        """Returns player associated with the given sid

        Args:
            sid (str): socketio session id of the player

        Returns:
            Player | None: A player if sid is valid, else None
        """
        return self.players.get(sid)

    def remove(self, sid: str) -> None:
        """Removes player associated with the given sid from store

        Args:
            sid (str): socketio session id of the player
        """
        try:
            self.players.pop(sid)
        except KeyError:
            pass

    def check_exists(self, username: str) -> bool:
        """Checks whether a username is already taken

        Args:
            username (str): username to check

        Returns:
            bool: `True` if the username exists, else `False`
        """
        usernames = [
            user.username for user in (self.players.values() or self.queue)
        ]

        return username in usernames
