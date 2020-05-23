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

    Your GessGame class must include the following:
    An init method that initializes any data members.
    A method called get_game_state that takes no parameters and returns 'UNFINISHED', 'BLACK_WON' or 'WHITE_WON'.
    A method called resign_game that lets the current player concede the game, giving the other player the win.
    A method called make_move that takes two parameters - strings that represent the center square of the piece being moved and the desired new location of the center square. For example, make_move('b6', 'e9'). If the indicated move is not legal for the current player, or if the game has already been won, then it should just return False. Otherwise it should make the indicated move, remove any captured stones, update the game state if necessary, update whose turn it is, and return True.

    Feel free to add whatever other classes, methods, or data members you want. All data members must be private.
    """

    def __init__(self):
        """Initializes GessGame object"""
        self._game_state = "UNFINISHED"  # 'UNFINISHED', 'BLACK_WON' or 'WHITE_WON'
        self._turn_state = "BLACKS_TURN"  # 'BLACKS_TURN' OR 'WHITES_TURN'
        self._bound_rows = self._bound_cols = 20  # board boundary is 20x20 from rows 2-19 and columns b-s
        self._rows = self._cols = 22
        # self._board_dims = (self._bound_rows, self._bound_cols)
        # self._dims = (self._rows, self._cols)
        self._blk_start_pos = (("2", "c"), ("2", "e"), ("2", "g"), ("2", "h"), ("2", "i"), ("2", "j"),
                               ("2", "k"), ("2", "l"), ("2", "m"), ("2", "n"), ("2", "p"), ("2", "r"),
                               ("3", "b"), ("3", "c"), ("3", "d"), ("3", "f"), ("3", "h"), ("3", "i"), ("3", "j"),
                               ("3", "k"), ("3", "m"), ("3", "o"), ("3", "q"), ("2", "r"), ("3", "s"),
                               ("4", "c"), ("4", "e"), ("4", "g"), ("4", "h"), ("4", "i"), ("2", "j"),
                               ("4", "k"), ("4", "l"), ("4", "m"), ("4", "n"), ("4", "p"), ("4", "r"),
                               ("7", "c"), ("7", "f"), ("7", "i"), ("7", "l"), ("7", "o"), ("7", "r"))

        self._wht_start_pos = (("19", "c"), ("19", "e"), ("19", "g"), ("19", "h"), ("19", "i"), ("19", "j"),
                               ("19", "k"), ("19", "l"), ("19", "m"), ("19", "n"), ("19", "p"), ("19", "r"),
                               ("18", "b"), ("18", "c"), ("18", "d"), ("18", "f"), ("18", "h"), ("18", "i"), ("18", "j"),
                               ("18", "k"), ("18", "m"), ("18", "o"), ("18", "q"), ("18", "r"), ("18", "s"),
                               ("17", "c"), ("17", "e"), ("17", "g"), ("17", "h"), ("17", "i"), ("17", "j"),
                               ("17", "k"), ("17", "l"), ("17", "m"), ("17", "n"), ("17", "p"), ("17", "r"),
                               ("14", "c"), ("14", "f"), ("14", "i"), ("14", "l"), ("14", "o"), ("14", "r"))
        self._num_blk_pcs = self._num_wht_pcs = 43  # each player starts with 43 pieces

        self._board = self.create_board()
        self._move_count = 0
        self._move_hist = {}  # a dictionary containing the history of moves
        # key is the move number (1, 2, 3, ..., n-2, n-1, n) and value is the move object

    ####################################################################################################
    # Queries

    def get_game_state(self):
        """
        A method called get_game_state that takes no parameters and returns 'UNFINISHED', 'BLACK_WON' or 'WHITE_WON'.
        :return: self._game_state
        """
        return self._game_state

    def get_num_blk_pcs(self):
        """"""
        return self._num_blk_pcs

    def get_num_wht_pcs(self):
        """"""
        return self._num_wht_pcs

    def get_board(self):
        """"""
        return self._board

    def get_move_count(self):
        return self._move_count

    def get_move_hist(self):
        return self._move_hist

    def get_turn_state(self):
        return self._turn_state

    def display_game(self):
        """
        Displays game info in the following order:
            game state
            number of black and white pieces
            board and current positions of players' pieces
        """
        print('{:*^94}'.format("   Game state = " + self.get_game_state() + "   "))
        print("WHITE " + str(self.get_num_wht_pcs()), end='{:^78}'.format(' '))
        print(str(self.get_num_blk_pcs()) + " BLACK")
        print('{:-^94}'.format(''))
        for rows in range(self._rows):
            print("| ", end="")
            for cols in range(self._cols):
                if cols == 0:
                    print(self._board[rows][cols].rjust(2) + " | ", end="")
                else:
                    print(self._board[rows][cols] + "   ", end="")
            print(self._board[self._rows - 1][self._cols - 1] + " |")
        print()

    ####################################################################################################
    # Commands

    def resign_game(self):
        """
        A method called resign_game that lets the current player concede the game, giving the other player the win.
        :return:
        """
        if self._game_state is "BLACK_WON" or self._game_state is "WHITE_WON":
            return

        if self._game_state is "UNFINISHED" and self._turn_state is "BLACKS_TURN":
            self._game_state = "WHITE_WON"
        else:
            self._game_state = "BLACK_WON"

    def make_move(self, from_square, to_square):
        """
        A method called make_move that takes two parameters - strings that represent the center square of the piece
        being moved and the desired new location of the center square. For example, make_move('b6', 'e9').
        If the indicated move is not legal for the current player, or if the game has already been won, then it should
        just return False. Otherwise it should make the indicated move, remove any captured stones, update the game state
        if necessary, update whose turn it is, and return True.
        :param from_square:
        :param to_square:
        :return: True/False
        """
        # check if game has already been won
        if self._game_state is "BLACK_WON" or self._game_state is "WHITE_WON":
            return False

        # from_coord = (from_square[1], from_square[0])
        # to_coord = (to_square[1], to_square[0])
        move = Move(from_square, to_square, self.get_board(), self.get_turn_state())
        # check if move is valid
        if not move.is_valid():
            del move
            return False

        # game hasn't been won and move is legal
        self._move_count += 1
        self._move_hist[self.get_move_count()] = move
        self._board = move.complete_move()

        # update turn_state to next player
        if self._turn_state is "BLACKS_TURN":
            # update game state if necessary
            if move.check_game_won() is "True":
                self._game_state = "BLACK_WON"
            self._turn_state = "WHITES_TURN"
        else:  # self._turn_state is "WHITES_TURN":
            # update game state if necessary
            if move.check_game_won() is "True":
                self._game_state = "WHITE_WON"
            self._turn_state = "BLACKS_TURN"

        return True

    def create_board(self):
        """Creates Gess board and places each players' pieces in their start position."""
        board = [[' ' for i in range(self._rows)] for j in range(self._cols)]

        # labels playable positions
        for i in range(3, self._bound_rows + 1):
            for j in range(3, self._bound_cols + 1):
                board[i][j] = "-"

        # create row labels
        num = 1
        for i in range(2, self._rows):
            board[i][0] = str(num)
            num += 1

        # create column labels
        char = "a"
        for i in range(2, self._cols):
            board[0][i] = char
            char = chr(ord(char) + 1)

        # create black player's pieces
        for tuples in self._blk_start_pos:
            board[int(tuples[0]) + 1][ord(tuples[1]) - 95] = "B"

        # create white player's pieces
        for tuples in self._wht_start_pos:
            board[int(tuples[0]) + 1][ord(tuples[1]) - 95] = "W"

        return board


class Move:
    """Represents a Move in the game"""

    def __init__(self, from_square, to_square, board_before, turn_state):
        """Initializes Move object"""
        self._from_square = from_square  # board coordinates (row, column) as a tuple of the piece to be moved
        self._to_square = to_square  # board coordinates (row, column) as a tuple where the piece is to be moved
        self._from_board_index = self.square_to_indices(from_square)  # from_square adjusted to correct board index
        self._to_board_index = self.square_to_indices(to_square)  # to_square adjusted to correct board index
        self._playable_area = (3, 21)  # playable board index area; inclusive [3, 21) non-inclusive
        self._board_before = board_before
        self._board_after = board_before
        self._player = "B" if turn_state is "BLACKS_TURN" else "W"
        self._opponent = "W" if turn_state is "BLACKS_TURN" else "B"
        self._game_won = False

    ####################################################################################################
    # Queries

    def is_valid(self):
        """"""
        # check if all 9 squares contain only pieces from player
        for row in range(-1, 2):
            for col in range(-1, 2):
                if self._board_before[self._to_board_index[0] + row][self._to_board_index[1] + col] is self._opponent:
                    return False

        contains_player = False
        for row in range(-1, 2):
            for col in range(-1, 2):
                if self._board_before[self._to_board_index[0] + row][self._to_board_index[1] + col] is self._player:
                    contains_player = True
                    break

        if contains_player is False:
            return False

        # if center piece is present --> able to move any amount of squares in possible directions


        # else only able to move up to 3 squares in possible directions

        return True

    def get_board_after(self):
        """"""
        return self._board_after

    def get_game_won(self):
        """"""
        return self._game_won

    ####################################################################################################
    # Commands

    @staticmethod
    def square_to_indices(square):
        """"""
        row_num, col_letter = (''.join(row for row in square if row.isdigit()) or None,
                               ''.join(col for col in square if col.isalpha()) or None)
        return int(row_num) + 1, ord(col_letter) - 95

    def complete_move(self):
        """"""
        # make a copy of all 1-9 pieces to be moved
        pcs_3x3 = (self._board_after[self._from_board_index[0]][self._from_board_index[1]],          # C
                   self._board_after[self._from_board_index[0] - 1][self._from_board_index[1]],      # N from C
                   self._board_after[self._from_board_index[0] - 1][self._from_board_index[1] + 1],  # NE from C
                   self._board_after[self._from_board_index[0]][self._from_board_index[1] + 1],      # E from C
                   self._board_after[self._from_board_index[0] + 1][self._from_board_index[1] + 1],  # SE from C
                   self._board_after[self._from_board_index[0] + 1][self._from_board_index[1]],      # S from C
                   self._board_after[self._from_board_index[0] + 1][self._from_board_index[1] - 1],  # SW from C
                   self._board_after[self._from_board_index[0]][self._from_board_index[1] - 1],      # W from C
                   self._board_after[self._from_board_index[0] - 1][self._from_board_index[1] - 1])  # NW from C

        # # delete current position of all pieces to be moved
        # self._board_after[self._from_board_index[0]][self._from_board_index[1]] = "-"          # C
        # self._board_after[self._from_board_index[0] - 1][self._from_board_index[1]] = "-"      # N from C
        # self._board_after[self._from_board_index[0] - 1][self._from_board_index[1] + 1] = "-"  # NE from C
        # self._board_after[self._from_board_index[0]][self._from_board_index[1] + 1] = "-"      # E from C
        # self._board_after[self._from_board_index[0] + 1][self._from_board_index[1] + 1] = "-"  # SE from C
        # self._board_after[self._from_board_index[0] + 1][self._from_board_index[1]] = "-"      # S from C
        # self._board_after[self._from_board_index[0] + 1][self._from_board_index[1] - 1] = "-"  # SW from C
        # self._board_after[self._from_board_index[0]][self._from_board_index[1] - 1] = "-"      # W from C
        # self._board_after[self._from_board_index[0] - 1][self._from_board_index[1] - 1] = "-"  # NW from C

        for row in range(-1, 2):
            for col in range(-1, 2):
                self._board_after[self._from_board_index[0] + row][self._from_board_index[1] + col] = "-"  # C

        # replace all pieces surrounding center coordinate where piece is to be moved to
        self._board_after[self._to_board_index[0]][self._to_board_index[1]] = pcs_3x3[0]          # C
        self._board_after[self._to_board_index[0] - 1][self._to_board_index[1]] = pcs_3x3[1]      # N from C
        self._board_after[self._to_board_index[0] - 1][self._to_board_index[1] + 1] = pcs_3x3[2]  # NE from C
        self._board_after[self._to_board_index[0]][self._to_board_index[1] + 1] = pcs_3x3[3]      # E from C
        self._board_after[self._to_board_index[0] + 1][self._to_board_index[1] + 1] = pcs_3x3[4]  # SE from C
        self._board_after[self._to_board_index[0] + 1][self._to_board_index[1]] = pcs_3x3[5]      # S from C
        self._board_after[self._to_board_index[0] + 1][self._to_board_index[1] - 1] = pcs_3x3[6]  # SW from C
        self._board_after[self._to_board_index[0]][self._to_board_index[1] - 1] = pcs_3x3[7]      # W from C
        self._board_after[self._to_board_index[0] - 1][self._to_board_index[1] - 1] = pcs_3x3[8]  # NW from C

        # index = 0
        # for row in range(-1, 2):
        #     for col in range(-1, 2):
        #         self._board_after[self._to_board_index[0] + row][self._to_board_index[1] + col] = pcs_3x3[index]
        #         index += 1

        return self._board_after

    def check_game_won(self):
        """"""
        # check if opponent's ring is present (clock-wise from Center)
        for i in range(self._playable_area[0] + 1, self._playable_area[1] - 1):
            for j in range(self._playable_area[0] + 1, self._playable_area[1] - 1):
                if self._board_after[i][j] == "-":
                    # check N from C
                    if (self._board_after[i - 1][j] == self._opponent and
                            # check NE from C
                            self._board_after[i - 1][j + 1] == self._opponent and
                            # check E from C
                            self._board_after[i][j + 1] == self._opponent and
                            # check SE from C
                            self._board_after[i + 1][j + 1] == self._opponent and
                            # check S from C
                            self._board_after[i + 1][j] == self._opponent and
                            # check SW from C
                            self._board_after[i + 1][j - 1] == self._opponent and
                            # check W from C
                            self._board_after[i][j - 1] == self._opponent and
                            # check NW from C
                            self._board_after[i - 1][j - 1] == self._opponent):
                        self._game_won = True
                        return self._game_won

        return self._game_won
