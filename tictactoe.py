#!/usr/bin/env python3

# TIP 1
# The comment on the first line make it so that this script can be run as an
# executable without specifying "python3" before the script name. You could
# just do "./tictactoe.py" and the script will run.

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

    def __init__( self, size ):

        # Create a list of lists that have 'size' elements in each row and
        # 'size' rows
        self.board = [ [" "] * size for row in range(size) ]





# TIP 2
# Function prologues are expected in professional code. The style can vary from
# company to company and from language to language, but a comment that describes
# what a function does, its inputs, and outputs is the bare minimum.

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


def player_move( board, player ):
    """
    Description:    Takes user input to make a move for a given player.

    Arguments:      board  - 2D array representing the board
                    player - Player object that is currently making a move

    Return:         None
    """

    is_valid_move = False
    row    = 0
    column = 0

    while not is_valid_move:

        index_string = input(f"{player.get_name()}, please enter the position (0-8): ")

        # TIP 3
        # Here's an example of a try-except block. The "Exception as e" part
        # saves the exception object as a variable named e so you can use its
        # data if you need to. You can also have multiple except blocks, each
        # with a unique type of Exception to have different error handling for
        # different errors.
        try:
            index = int(index_string)

        except Exception as e:
            print(f"'{index_string}' is not a valid position. Please enter a number between 0 and 8.")
            continue

        if index < 0 or index > 8:
            print(f"'{index_string}' is not a valid position. Please enter a number between 0 and 8.")
            continue

        row    = index // 3
        column = index % 3

        if board[row][column] != " ":
            print(f"Position {index} is already taken by {board[row][column]}")
            continue

        is_valid_move = True
        board[row][column] = player.get_mark()


def display_board( board ):
    """
    Description:    Prints out the current state of the board.

    Arguments:      board - 2D array representing the board

    Return:         None
    """

    # Assume the number of rows and columns are the same
    board_size = len(board)

    print("+---" * board_size + "+")

    for row in board:

        row_string = " | ".join(row)
        print("| " + row_string + " |")
        print("+---" * board_size + "+")


def check_for_winner( board, first_player, second_player ):
    """
    Description:    Checks whether there is a winner based on the current state
                    of the board.

    Arguments:      board         - 2D array representing the board
                    first_player  - Player object representing the player that
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
    for index, row in enumerate(board):

        # Check each row for a winner
        if row[0] != " " and len(set(row)) == 1:
            return True, name_dict[row[0]]

        # Keep track of how many open spots there are
        num_open_spots += row.count(" ")

        # Build up the list of diagonal marks in both diagonal directions
        diagonal1.append(row[index])
        diagonal2.append(row[len(row) - index - 1])

        # Build up a list of columns to check later
        columns.append([ board_row[index] for board_row in board ])

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
        return True, "tie"

    # If no other cases were hit, the game must go on
    return False, "tie"


if __name__ == "__main__":

    board = [
                [" ", " ", " "],
                [" ", " ", " "],
                [" ", " ", " "],
            ]

    game_over = False

    first_player, second_player = create_players()

    while not game_over:

        player_move(board, first_player)
        display_board(board)
        game_over, winner = check_for_winner(board, first_player, second_player)

        if game_over:
            break

        player_move(board, second_player)
        display_board(board)
        game_over, winner = check_for_winner(board, first_player, second_player)

    if winner == "tie":
        print("Good news: no one lost! Bad news: no one won :(")

    else:
        print(f"The winner is: {winner}")
