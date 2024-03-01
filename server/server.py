"""Socketio server module"""

import socketio

from asgi.main import app

sio = socketio.AsyncServer(async_mode="asgi")

app = socketio.ASGIApp(sio, app)


@sio.event
async def connect(sid, environ, auth):
    print("connected", sid)


@sio.event
def disconnect(sid):
    print(sid, "has disconnected")

@sio.event
def fname(arg):
    pass
