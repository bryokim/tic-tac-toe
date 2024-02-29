"""Main"""

from tictactoe import TicTacToe


def main():
    """Entry point"""
    try:
        size = int(input("Enter the size of the board (Defaults to 3): "))
    except ValueError:
        print("Invalid value for size. Default used.")
        size = 3
    else:
        if size < 3:
            print("Size cannot be less than 3. Using default")
            size = 3

    game = TicTacToe(size)
    game.game_loop()


if __name__ == "__main__":
    main()
