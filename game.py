"""Game entry point."""

from gameboard import GameBoard
from player import Player
from computer import Computer


def game_loop(game_board: GameBoard, player_X: Player, player_O: Computer):
    """Game logic.

    Args:
        game_board (GameBoard): Board for the game.
        player_X (Player): First player.
        player_O (Player): Second Player.
    """
    leave_loop = False
    check = False
    turn_count = 0

    while leave_loop is False:
        # player_X's turn
        if turn_count % 2 == 0:
            game_board.print_board()

            while True:
                try:
                    number_picked = int(
                        input(f"\nChoose a number {game_board.choices}: ")
                    )
                except ValueError:
                    print("You must pick a number. Please try again")
                else:
                    if number_picked in game_board.choices:
                        game_board.modify_board(number_picked, player_X.symbol)
                        player_X.update_positions(number_picked)

                        # Remove any combination with number picked from other player's
                        # possible winning combinations
                        player_O.filter_winning_combinations(number_picked)

                        turn_count += 1

                        if check and player_X.check_win():
                            game_board.print_board()
                            print(f"\n{player_X.symbol} Won")
                            leave_loop = True

                        break
                    else:
                        print("Invalid choice. Please try again")

        # player_O's turn - Computer
        else:
            # number_picked = random.choice(game_board.choices)
            number_picked = player_O.next_move(player_X, game_board.choices)
            print(f"\nComputer choice: {number_picked}")

            if number_picked in game_board.choices:
                game_board.modify_board(number_picked, player_O.symbol)
                player_O.update_positions(number_picked)

                player_X.filter_winning_combinations(number_picked)

                turn_count += 1

                if check and player_O.check_win():
                    game_board.print_board()
                    print(f"\n{player_O.symbol} Won")
                    leave_loop = True

        if turn_count % game_board.rows:
            check = True

        if (len(game_board.choices) == 0 and leave_loop is False) or (
            len(player_X.winning_combinations) == 0
            and len(player_O.winning_combinations) == 0
        ):
            print("\nDraw")
            leave_loop = True


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

    game_board = GameBoard(size, size)
    player_X = Player("X", game_board.combinations)
    player_O = Computer("O", game_board.combinations)

    game_loop(game_board, player_X, player_O)


if __name__ == "__main__":
    main()
