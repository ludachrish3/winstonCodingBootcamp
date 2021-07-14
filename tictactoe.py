#!/usr/bin/env python3

# TIP 1
# The comment on the first line make it so that this script can be run as an
# executable without specifying "python3" before the script name. You could
# just do "./tictactoe.py" and the script will run.

# TIP 2
# argparse is an extremely powerful and useful argument parsing library. Use it
# to give command line tools some professional flair.
import argparse

# TIP 3
# Function prologues are expected in professional code. The style can vary from
# company to company and from language to language, but a comment that describes
# what a function does, its inputs, and outputs is the bare minimum.


class Player():
    """
    Description:    Class to represent a Tic-Tac-Toe player. Each Player has a
                    mark and a name.
    """

    def __init__( self, mark, name ):

        self.set_mark(mark)
        self.set_name(name)


    def get_mark( self ):

        return self.mark


    def set_mark( self, mark):

        self.mark = mark.upper()


    def get_name( self ):

        return self.name


    def set_name( self, name ):

        self.name = name


class Board():
    """
    Description:    Class to represent a Tic-Tac-Toe board. It is assumed that
                    the number of rows and columns are the same.
    """

    # TIP 4
    # Use constants for values that are checked or used in multiple places. It
    # reduces the number of changes you'll have to make later if the value ever
    # changes. Also, it's common practice to make them in call caps to make
    # them stand out.
    TIE_STRING = "tie"

    def __init__( self, size=3 ):

        # Create a list of lists that have 'size' elements in each row and
        # 'size' rows
        self.board = [ [" "] * size for row in range(size) ]
        self.size = size
        self.max_position = size ** 2


    def make_move( self, player ):
        """
        Description:    Takes user input to make a move for a given player.

        Arguments:      player - Player object that is currently making a move

        Return:         None
        """

        is_valid_move = False
        row    = 0
        column = 0

        while not is_valid_move:

            index_string = input(f"{player.get_name()}, please enter the position (1-{self.max_position}): ")

            # TIP 5
            # Here's an example of a try-except block. The "Exception as e" part
            # saves the exception object as a variable named e so you can use its
            # data if you need to. You can also have multiple except blocks, each
            # with a unique type of Exception to have different error handling for
            # different errors.

            # Subtract one to index from zero and make the math easier
            try:
                index = int(index_string) - 1

            except Exception as e:
                print(f"'{index_string}' is not a valid position. Please enter a number between 1 and {self.max_position}.")
                continue

            if index < 0 or index > self.max_position:
                print(f"'{index_string}' is not a valid position. Please enter a number between 1 and {self.max_position}.")
                continue

            row    = index // self.size
            column = index % self.size

            if self.board[row][column] != " ":
                print(f"Position {index_string} is already taken by {self.board[row][column]}")
                continue

            is_valid_move = True
            self.board[row][column] = player.get_mark()


    def check_for_winner( self, first_player, second_player ):
        """
        Description:    Checks whether there is a winner based on the current state
                        of the board.

        Arguments:      first_player  - Player object representing the player that
                                        goes first in each round.
                        second_player - Player object representing the player that
                                        goes second in each round.

        Return:         Tuple containing a boolean of whether the game is over and
                        a string with the name of the winner. The name of the
                        winner will be "tie" if no one has won.
        """

        num_open_spots = 0  # Number of spots not containing a player's mark
        diagonal1 = []      # List of diagonal marks from upper left to lower right
        diagonal2 = []      # List of diagonal marks from upper right to lower left
        columns = []        # List of marks in each column

        # Make a dictionary keyed on the mark to make it easier to determine the
        # name of the winner once the winning mark is determined.
        name_dict = {
            first_player.get_mark(): first_player.get_name(),
            second_player.get_mark(): second_player.get_name(),
        }

        # Check each row for a winner, and create lists of column marks while we're
        # at it to make checking columns easier
        for index, row in enumerate(self.board):

            # Check each row for a winner
            if row[0] != " " and len(set(row)) == 1:
                return True, name_dict[row[0]]

            # Keep track of how many open spots there are
            num_open_spots += row.count(" ")

            # Build up the list of diagonal marks in both diagonal directions
            diagonal1.append(row[index])
            diagonal2.append(row[len(row) - index - 1])

            # Build up a list of columns to check later
            columns.append([ board_row[index] for board_row in self.board ])

        # Check each column for a winner
        for col_index, col in enumerate(columns):

            if col[0] != " " and len(set(col)) == 1:
                return True, name_dict[col[0]]

        # Check for a winner on diagonals
        if diagonal1[0] != " " and len(set(diagonal1)) == 1:
            return True, name_dict[diagonal1[0]]

        if diagonal2[0] != " " and len(set(diagonal2)) == 1:
            return True, name_dict[diagonal2[0]]

        # The game is over if all open spots are taken and no winner was found
        if num_open_spots == 0:
            return True, Board.TIE_STRING

        # If no other cases were hit, the game must go on
        return False, Board.TIE_STRING


    # TIP 6
    # Every object has a __str__() function and a __repr__() function. They
    # get called when you try to print the object as a string, like in print()
    # or in str(). __repr__() is more for debugging and seeing a more verbose
    # form of the object. __str__() is meant for displaying the object to a user.
    def __str__( self ):
        """
        Description:    Create a string representation of the Board object.

        Arguments:      None

        Return:         String representing the Board object.
        """

        board_string = "+---" * self.size + "+"

        for row in self.board:

            row_string = " | ".join(row)
            board_string += "\n" + "| " + row_string + " |"
            board_string += "\n" + "+---" * self.size + "+"

        return board_string


def create_players( ):
    """
    Description:    Asks Player 1 what kind of mark they want to use, which must
                    be either 'X' or 'O', and determines the player order. The
                    player that uses 'O' always goes first.

    Arguments:      None

    Return:         Tuple containing Player objects for the player that goes
                    first and the player that goes second.
    """

    is_valid_mark = False

    while not is_valid_mark:

        player_one_mark = input("Player 1, choose X or O: ").upper()

        # O goes first, so the first player is whoever uses O as their mark
        if player_one_mark == "O":

            first_player  = Player("O", "Player 1")
            second_player = Player("X", "Player 2")
            is_valid_mark = True

        elif player_one_mark == "X":

            first_player  = Player("O", "Player 2")
            second_player = Player("X", "Player 1")
            is_valid_mark = True

        else:

            print(f"'{player_one_mark}' is not a valid selection. Please try again.")

    return first_player, second_player

# TIP 7
# Checking if __name__ equals __main__ is a way to ensure certain code only
# runs if it is the main script and not imported as a module. If you're
# writing code that can be imported as a module later and can also be run on
# its own, this code is not run when imported. For example, if this script was
# a module and someone was importing it for access to the Board or Player
# objects, they wouldn't necessarily want to be launched into a game of
# tic-tac-toe when they import the file. They just want to get the definitions
# of the object and that's it.

if __name__ == "__main__":

    parser = argparse.ArgumentParser(add_help=False)

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument("-s", "--board-size", default=3, type=int, help="Board size to use for tic-tac-toe. The default is 3 if not specified.")
    optional.add_argument("-h", "--help",       action="help",       help="Show this help message and exit")

    args = parser.parse_args()

    # 3 is the smallest acceptable size becuase a size of 1 or 2 means the
    # first player always wins and anything smaller than that makes no sense.
    if args.board_size < 3:
        print("The board is too small. 3 is the minimum size")
        exit(1)

    board =  Board(size=args.board_size)
    game_over = False

    first_player, second_player = create_players()

    while not game_over:

        board.make_move(first_player)
        print(board)
        game_over, winner = board.check_for_winner(first_player, second_player)

        if game_over:
            break

        board.make_move(second_player)
        print(board)
        game_over, winner = board.check_for_winner(first_player, second_player)

    if winner == Board.TIE_STRING:
        print("Good news: no one lost! Bad news: no one won :(")

    else:
        print(f"The winner is: {winner}")

    # TIP 8
    # It's good practice to always give your scripts an exit code. It makes it
    # easier to check their return code in the shell after they run if you
    # have an automation framework checking if things succeeded. Without it,
    # the return code could be undetermined.
    exit(0)
