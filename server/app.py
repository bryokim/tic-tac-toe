import socketio

from typing import Any

from controllers.user import UserController
from controllers.room import RoomController
from game.player import Player
from utils.constants import Messages


class App:
    """Handles Events sent to the server"""

    def __init__(self, socket_io: socketio.AsyncServer):
        """Initialize a new App instance

        Args:
            socket_io (socketio.AsyncServer): Socketio server.
        """
        self.sio = socket_io
        self.data: dict[Any, Any] = {}
        self.user_controller = UserController()
        self.room_controller = RoomController()

    async def handle_enter(self, sid: str, username: str):
        """Handles the enter event.

        Args:
            sid (str): socketio session id.
            username (str): The player's username.
        """
        if self.user_controller.check_exists(username):
            await self.sio.emit("uname-exists", Messages.uname_exists, to=sid)
        else:
            self.user_controller.add_to_queue(sid, username)

            if self.user_controller.get_queue_size() >= 2:
                players = self.user_controller.add_to_store()
                await self.match(players)
            else:
                await self.sio.emit("info", Messages.waiting, to=sid)

    async def match(self, players: list[Player]) -> None:
        """Matches two players and creates a room for them to play.

        Args:
            players (list[Player, Player]): Two players being matched
        """
        player_X, player_O = players

        new_game = self.room_controller.create([player_X, player_O])

        room_id = new_game.game_id

        # Add the players to a common room
        await self.sio.enter_room(player_X.sid, room_id)
        await self.sio.enter_room(player_O.sid, room_id)

        self.data[room_id] = {player_O, player_X}
        self.data[player_X.sid] = room_id
        self.data[player_O.sid] = room_id

        player_X.symbol = "X"
        player_O.symbol = "O"

        await self.sio.emit("info", Messages.player_x, to=player_X.sid)
        await self.sio.emit("info", Messages.player_o, to=player_O.sid)

        await self.sio.emit("progress", new_game.progress(), room=room_id)
        await self.sio.emit("scoreboard", new_game.scoreboard, room=room_id)

    def handle_play(self, message):
        pass

    def handle_replay(self, confirmed):
        pass

    def handle_disconnect(self, sid):
        pass
