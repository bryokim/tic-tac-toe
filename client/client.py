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


def print_board(board: list[list[int]], size: int) -> None:
    """Prints the board"""

    try:
        for row in range(size):
            print("\n", "+---" * size, "+\n|", end="", sep="")

            for col in range(size):
                print(f" {board[row][col]} |", end="")

        print("\n", "+---" * size, "+", sep="")
    except IndexError:
        pass


@sio.on("progress")
def progress(data: list):
    """State of the board

    Args:
        data (list): List of the current board.
    """
    if len(data) > 0:
        print_board(data, 3)


@sio.on("make move")
def make_move(message: str = ""):
    """Make single move.

    Args:
        message (str, optional): Message to give the player. Defaults to "".
    """
    if message:
        print(message)

    move = input("Enter move: ")

    while move == "" or not move.isdecimal():
        move = input("Wrong input. Please enter a number from 1-9: ")

    sio.emit("move", f"{move}")


@sio.on("scoreboard")
def scoreboard(data: dict[str, int]):
    """Show scoreboard.

    Args:
        data (dict[str, int]): Dictionary containing current scoreboard
    """
    print(data)


@sio.on("over")
def over(data: dict[str, int]):
    """Show scoreboard.

    Args:
        data (dict[str, int]): Dictionary containing current scoreboard
    """
    print(data)


@sio.event
def replay(message: str):
    # print(message)
    confirm = input(f'{message} [y/n]: ')
    sio.emit('replay', confirm)


sio.connect(SERVER_URL)

# Emit the enter event with username given
sio.emit("enter", argv[1])


sio.wait()

# sio.disconnect()
