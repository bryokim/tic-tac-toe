from os import getenv
from dataclasses import dataclass

# prefix for socketio rooms
ROOM_PREFIX = getenv("ROOM_PREFIX", "tictactoe_room_")


@dataclass
class Messages:
    tie = "Tied!"
    win = "U Won!"
    lose = "U Lost!"
    resign = "The other player has resigned"
    replay = "Play one more?"
    game_0 = "Game has not started yet!"
    game_1 = "Game started"
    invalid = "Invalid move"
    not_yet = "It's not your move yet."
    waiting = "Waiting for another player"
    player_x = "You are 'Player X.'"
    player_o = "You are 'Player O.'"
    uname_exists = "Username already exists!"
