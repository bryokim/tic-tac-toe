"""Socketio server module"""

import socketio

from app import App
from asgi.main import app

sio = socketio.AsyncServer(async_mode="asgi")

app = socketio.ASGIApp(sio, app)

event_handler = App(sio)


@sio.event
async def connect(sid, environ, auth):
    print("connected", sid)


@sio.event
async def disconnect(sid):
    print(sid, "has disconnected")
    await event_handler.handle_disconnect(sid)


@sio.event
async def enter(sid: str, username: str):
    """Event for when a player enters the game

    Args:
        sid (str): socketio session id
        username (str): Player's username
    """
    await event_handler.handle_enter(sid, username)


@sio.event
async def move(sid: str, move: str):
    await event_handler.handle_play(sid, move)


@sio.event
async def replay(sid: str, confirm: str):
    confirmed = True if confirm.lower() == "y" else False

    await event_handler.handle_replay(sid, confirmed)
