import os

def clear_terminal():
    """Clears the terminal"""

    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')