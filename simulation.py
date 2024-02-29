"""Simulate two computer players"""

from sys import argv

from gameboard import GameBoard
from computer import Computer


def play(
    game_board: GameBoard,
    current_player: Computer,
    other_player: Computer,
    check: bool,
) -> bool:
    """Make a single play move.

    Args:
        game_board (GameBoard): Board for the game
        current_player (Computer): Player that is currently making move
        other_player (Computer): Player being played against
        check (bool): Whether to check for win

    Returns:
        bool: `True` if current_player has won, else `false`
    """
    number_picked = current_player.next_move(other_player, game_board.choices)

    print(f"\n{current_player.symbol}: {number_picked}")

    game_board.modify_board(number_picked, current_player.symbol)
    current_player.update_positions(number_picked)

    other_player.filter_winning_combinations(number_picked)

    if check and current_player.check_win():
        game_board.print_board()
        print(f"\n{current_player.symbol} Won")
        return True

    return False


def game_loop(game_board: GameBoard, player_X: Computer, player_O: Computer):
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
            leave_loop = play(game_board, player_X, player_O, check)

            turn_count += 1

        # player_O's turn - Computer
        else:
            leave_loop = play(game_board, player_O, player_X, check)
            turn_count += 1

        if turn_count % game_board.rows:
            check = True

        if (len(game_board.choices) == 0 and leave_loop is False) or (
            len(player_X.winning_combinations) == 0
            and len(player_O.winning_combinations) == 0
        ):
            print("\nDraw")
            game_board.print_board()
            leave_loop = True


def main():
    """Entry point"""
    try:
        size = int(argv[1])
    except IndexError:
        print("Size 3 used.")
        size = 3

    game_board = GameBoard(size, size)
    player_X = Computer("X", game_board.combinations)
    player_O = Computer("O", game_board.combinations)

    game_loop(game_board, player_X, player_O)


if __name__ == "__main__":
    main()
