"""Socketio client module"""

from sys import argv
import socketio
import os

from utils.clear import clear_terminal

PORT = os.getenv("SERVER_PORT", 8000)
SERVER_URL = os.getenv("SERVER_URL", f"http://localhost:{PORT}")

sio = socketio.Client()


@sio.event
def connect():
    clear_terminal()
    print("Connected!")


@sio.event
def connect_error(data):
    print("The connection failed!\n", data)


@sio.event
def disconnect():
    print("Disconnected!")


@sio.event
def info(message: str):
    """Event with informational message

    Args:
        message (str): message to display to player
    """
    print(message)


@sio.on("uname-exists")
def username_exists(message: str):
    """Emitted if entered username exists

    Args:
        message (str): message to display to player
    """
    print(message)


@sio.on("progress")
def progress(data: list):
    """State of the board

    Args:
        data (list): List of the current board.
    """
    print(data)


@sio.on("scoreboard")
def scoreboard(data: dict[str, int]):
    """Show scoreboard.

    Args:
        data (dict[str, int]): Dictionary containing current scoreboard
    """
    print(data)


sio.connect(SERVER_URL)

# Emit the enter event with username given
sio.emit("enter", argv[1])


sio.wait()

# sio.disconnect()
