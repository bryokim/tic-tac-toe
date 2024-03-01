"""FastAPI app"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    """Home page"""
    return 'Welcome to TIC-tac-TOE'

