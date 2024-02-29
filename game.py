"""Game entry point."""

from gameboard import GameBoard
from player import Player
from computer import Computer


def play(
    game_board: GameBoard,
    current_player: Player,
    other_player: Player,
    number_picked: int,
    check_win: bool,
) -> bool:
    game_board.modify_board(number_picked, current_player.symbol)
    current_player.update_positions(number_picked)

    # Remove combination with number picked from other player's possible
    # winning combinations
    other_player.filter_winning_combinations(number_picked)

    if check_win and current_player.is_winner():
        game_board.print_board()
        print(f"\n{current_player.symbol} Won")
        return True

    return False


def game_loop(game_board: GameBoard, player_X: Player, player_O: Computer):
    """Game logic.

    Args:
        game_board (GameBoard): Board for the game.
        player_X (Player): First player.
        player_O (Player): Second Player.
    """
    leave_loop = False
    check_win = False
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
                        leave_loop = play(
                            game_board,
                            player_X,
                            player_O,
                            number_picked,
                            check_win,
                        )
                        turn_count += 1

                        break
                    else:
                        print("Invalid choice. Please try again")

        # player_O's turn - Computer
        else:
            # number_picked = random.choice(game_board.choices)
            number_picked = player_O.next_move(player_X, game_board.choices)
            print(f"\nComputer choice: {number_picked}")

            leave_loop = play(
                game_board, player_O, player_X, number_picked, check_win
            )
            turn_count += 1

        if turn_count % game_board.rows:
            check_win = True

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
