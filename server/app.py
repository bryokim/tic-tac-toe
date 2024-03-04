import socketio
import re
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

    async def handle_enter(
        self, sid: str, username: str, replay: bool = False
    ):
        """Handles the enter event.

        Args:
            sid (str): socketio session id.
            username (str): The player's username.
            replay (bool): Whether it is a replay of an existing game.
                Usernames are not checked.
        """
        if self.user_controller.check_exists(username) and not replay:
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
        await self.sio.emit("make move", to=player_X.sid)

        new_game.init()

    async def handle_play(self, sid: str, message: str):
        """Handles the move event

        Args:
            sid (str): socketio session id of the current player.
            message (str): position to play to.
        """
        normalized_message = re.sub(r"/s", "", message)

        room_id = self.data[sid]
        game = self.room_controller.get_room(room_id)
        current_player: Player = game.players[sid]

        player_turn = game._turn == current_player.symbol

        if player_turn and game._status == 1:
            try:
                move = int(normalized_message)
            except ValueError:
                move = 0

            accepted = game.make_move(current_player, move)

            if accepted:
                progress = game.progress()

                await self.sio.emit("progress", progress, room=room_id)
                if game._status == 3:
                    await self.sio.emit("over", Messages.win, to=sid)
                    await self.sio.emit(
                        "over", Messages.lose, room=room_id, skip_sid=sid
                    )
                    await self.sio.emit(
                        "replay", Messages.replay, room=room_id
                    )
                    game.update_scoreboard(current_player.symbol)
                    game.reset()
                elif game._status == 2:
                    await self.sio.emit("over", Messages.tie, room=room_id)
                    await self.sio.emit(
                        "replay", Messages.replay, room=room_id
                    )
                    game.update_scoreboard("tie")
                    game.reset()
                else:
                    other_player_sid: str = list(
                        filter(lambda x: x != sid, game.players.keys())
                    )[0]
                    await self.sio.emit("make move", to=other_player_sid)

                    game.toggle_turn()
            else:
                await self.sio.emit(
                    "make move", Messages.invalid, to=current_player.sid
                )
        elif not player_turn:
            await self.sio.emit("info", Messages.not_yet, to=sid)
        else:
            await self.sio.emit("info", Messages.game_0, to=sid)

    async def handle_replay(self, sid: str, confirmed: bool):
        """Handles the replay event

        Args:
            sid (str): socketio session id of the current player.
            confirmed (bool): Whether the player has confirmed replay.
        """
        room_id = self.data[sid]
        game = self.room_controller.get_room(room_id)

        if not confirmed:
            # Player did not confirm replay
            player = self.user_controller.get_player(sid)

            self.room_controller.remove(room_id)

            await self.handle_enter(sid, player.username, True)

            if game and game.replay_confirmed:
                # First player had confirmed replay
                other_player = (
                    game.player_X
                    if game.player_X.sid != sid
                    else game.player_O
                )
                await self.sio.emit(
                    "info",
                    Messages.resign,
                    to=other_player.sid,
                )
                await self.handle_enter(
                    other_player.sid, other_player.username, True
                )

        elif not game:
            # First player did not confirm replay
            await self.sio.emit(
                "info",
                Messages.resign,
                to=sid,
            )
            player = self.user_controller.get_player(sid)
            await self.handle_enter(sid, player.username, True)
        elif game.replay_confirmed == 0:
            # First player to confirm replay
            game.confirm_replay()
            await self.sio.emit("info", Messages.waiting_confirm, to=sid)
        else:
            # Both players have confirmed replay
            game.reset()
            game.init()

            await self.sio.emit("scoreboard", game.scoreboard, room=room_id)
            await self.sio.emit("info", Messages.game_1, room=room_id)
            await self.sio.emit("progress", game.progress(), room=room_id)
            await self.sio.emit("make move", to=game.player_X.sid)

    def handle_disconnect(self, sid):
        pass
