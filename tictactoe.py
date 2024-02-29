"""Implementation of the TicTacToe class"""

from gameboard import GameBoard
from player import Player
from computer import Computer


class TicTacToe:
    def __init__(self, size: int):
        """Initialize a new TicTacToe instance.

        Args:
            size (int): Number of rows on the game board. Equal to columns.
        """
        self.game_board = GameBoard(size, size)
        self.player_X = Player("X", self.game_board.combinations)
        self.player_O = Computer("O", self.game_board.combinations)

        # Check for possible win
        self.check_win = False

    def game_loop(self):
        """Game logic."""
        leave_loop = False
        turn_count = 0

        while leave_loop is False:
            # player_X's turn
            if turn_count % 2 == 0:
                self.game_board.print_board()

                leave_loop = self.user_play(
                    self.player_X,
                    self.player_O,
                )

            # player_O's turn - Computer
            else:
                leave_loop = self.computer_play(
                    self.player_O,
                    self.player_X,
                )

            turn_count += 1

            if turn_count % self.game_board.rows:
                self.check_win = True

            if self.is_draw(leave_loop):
                self.game_board.print_board()
                leave_loop = True

    def user_play(
        self,
        current_player: Player,
        other_player: Player,
    ) -> bool:
        """Logic for a player that is not computer.

        Args:
            current_player (Player): Player making the play
            other_player (Player): Player being played against

        Returns:
            bool: `True` if current player has won, else `False`
        """
        while True:
            try:
                number_picked = int(
                    input(f"\nChoose a number {self.game_board.choices}: ")
                )
            except ValueError:
                print("You must pick a number. Please try again")
            else:
                if number_picked in self.game_board.choices:
                    return self.play(
                        current_player,
                        other_player,
                        number_picked,
                    )
                else:
                    print("Invalid choice. Please try again")

    def computer_play(
        self,
        current_player: Computer,
        other_player: Player,
    ) -> bool:
        """Logic for the computer player.

        Args:
            current_player (Player): Player making the play
            other_player (Player): Player being played against

        Returns:
            bool: `True` if computer has won, else `False`
        """
        # number_picked = random.choice(self.game_board.choices)
        number_picked = current_player.next_move(
            other_player, self.game_board.choices
        )
        print(f"\nComputer choice: {number_picked}")

        return self.play(current_player, other_player, number_picked)

    def play(
        self,
        current_player: Player,
        other_player: Player,
        number_picked: int,
    ) -> bool:
        """Play with the number picked.

        Args:
            current_player (Player): Current player making play
            other_player (Player): Player being played against
            number_picked (int): Number of the box the current_player has picked.
                Indexed from 1.

        Returns:
            bool: `True` if the current_player has won, else `False`.
        """
        self.game_board.modify_board(number_picked, current_player.symbol)
        current_player.update_positions(number_picked)

        # Remove combination with number picked from other player's possible
        # winning combinations
        other_player.filter_winning_combinations(number_picked)

        if self.check_win and current_player.is_winner():
            self.game_board.print_board()
            print(f"\n{current_player.symbol} Won")
            return True

        return False

    def is_draw(self, leave_loop: bool) -> bool:
        if (len(self.game_board.choices) == 0 and leave_loop is False) or (
            len(self.player_X.winning_combinations) == 0
            and len(self.player_O.winning_combinations) == 0
        ):
            print("\nDraw")
            return True

        return False
