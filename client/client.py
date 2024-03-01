"""Socketio client module"""

import socketio
import os

from utils.clear import clear_terminal

PORT = os.getenv('SERVER_PORT', 8000)
SERVER_URL = os.getenv('SERVER_URL', f'http://localhost:{PORT}')

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
    
    
sio.connect(SERVER_URL)

sio.disconnect()
