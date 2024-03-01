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
def disconnect(sid):
    print(sid, "has disconnected")

@sio.event
async def enter(sid: str, username: str):
    """Event for when a player enters the game

    Args:
        sid (str): socketio session id
        username (str): Player's username
    """
    await event_handler.handle_enter(sid, username)