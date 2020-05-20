# Author: Arvin Shen
# Date: 05/16/2020
# Description:


class GessGame:
    """
    Remember that this project cannot be submitted late.

    Write a class named GessGame for playing an abstract board game called Gess.
    Note that when a piece's move causes it to overlap stones, any stones covered by the footprint get removed,
    not just those covered by one of the piece's stones. It is not legal to make a move that leaves you without a ring.
    It's possible for a player to have more than one ring. A player doesn't lose until they have no remaining rings.

    Locations on the board will be specified using columns labeled a-t and rows labeled 1-20,
    with row 1 being the Black side and row 20 the White side. The actual board is only columns b-s and rows 2-19.
    The center of the piece being moved must stay within those boundaries. An edge of the piece may go
    into columns a or t, or rows 1 or 20, but any pieces there are removed at the end of the move. Black goes first.

    There's an online implementation here you can try, but it's not 100% consistent with the rules.
    In the case of any discrepancy between the online game and the rules, you should comply with the rules
    (you can also ask us for clarification of course).
    One example is that the online game lets you make moves that leave you without a ring,
    which isn't allowed (if a player wants to end the game, they can just resign).
    Another example is that the online game lets you choose a piece whose center is off the board
    (in columns a or t, or in rows 1 or 20), which isn't allowed.

    You're not required to print the board, but you will probably find it very useful for testing purposes.

    Your GessGame class must include the following:

    An init method that initializes any data members.
    A method called get_game_state that takes no parameters and returns 'UNFINISHED', 'BLACK_WON' or 'WHITE_WON'.
    A method called resign_game that lets the current player concede the game, giving the other player the win.
    A method called make_move that takes two parameters - strings that represent the center square of the piece
    being moved and the desired new location of the center square. For example, make_move('b6', 'e9').
    If the indicated move is not legal for the current player, or if the game has already been won, then it should
    just return False. Otherwise it should make the indicated move, remove any captured stones, update the game state
    if necessary, update whose turn it is, and return True.
    Feel free to add whatever other classes, methods, or data members you want. All data members must be private.
    """
    def __init__(self):
        """Initializes GessGame object"""
        self._game_state = "UNFINISHED"
        self._bound_rows = 20
        self._bound_cols = 20
        self._rows = 22
        self._cols = 22
        self._board_dims = (self._bound_rows, self._bound_cols)
        self._dims = (self._rows, self._cols)
        self._board = self.create_board()

    def get_game_state(self):
        """"""
        return self._game_state

    def resign_game(self):
        """"""
        return

    def make_move(self, curr_pos, move_pos):
        """"""
        return False

    def display_game(self):
        """"""
        for rows in range(self._rows):
            print("| ", end="")
            for cols in range(self._cols):
                if cols == 0:
                    print(self._board[rows][cols].rjust(2) + " | ", end="")
                else:
                    print(self._board[rows][cols] + " | ", end="")
            print(self._board[self._rows-1][self._cols-1] + " |")

    def create_board(self):
        """"""
        board = [[' ' for i in range(self._cols)] for j in range(self._rows)]

        num = 1
        for i in range(21, 1, -1):
            board[i][0] = str(num)
            num += 1

        char = "a"
        for i in range(2, 22):
            board[0][i] = char
            char = chr(ord(char) + 1)
        return board
