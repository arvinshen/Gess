# Author: Arvin Shen
# Date: 05/16/2020
# Description: A GessGame simulator

class GessGame:
    """Represents an abstract board game called Gess."""

    def __init__(self):
        """Initializes GessGame object"""
        self._game_state = "UNFINISHED"  # 'UNFINISHED', 'BLACK_WON' or 'WHITE_WON'
        self._turn_state = "BLACKS_TURN"  # 'BLACKS_TURN' OR 'WHITES_TURN'
        self._bound_rows = self._bound_cols = 20  # board boundary is 20x20 from rows 2-19 and columns b-s
        self._num_rows = self._num_cols = 22
        self._blk_start_pos = (("2", "c"), ("2", "e"), ("2", "g"), ("2", "h"), ("2", "i"), ("2", "j"),
                               ("2", "k"), ("2", "l"), ("2", "m"), ("2", "n"), ("2", "p"), ("2", "r"),
                               ("3", "b"), ("3", "c"), ("3", "d"), ("3", "f"), ("3", "h"), ("3", "i"), ("3", "j"),
                               ("3", "k"), ("3", "m"), ("3", "o"), ("3", "q"), ("3", "r"), ("3", "s"),
                               ("4", "c"), ("4", "e"), ("4", "g"), ("4", "h"), ("4", "i"), ("4", "j"),
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
        self._move_hist = {}  # a dictionary containing the history of moves (as a Move object) made in the game
        # key is the move number (1, 2, 3, ..., n-2, n-1, n) and value is the move object

        self._dict_prompt = {
            "menu": ("Gess Main Menu\nChoose from the following options:\n"
                     "1. Display Gess Board\n2. Check Players' Turn\n3. Play Move\n4. Resign\n5. Exit\n", 5),
            "play": ("Choose from the following options:\n"
                     "1. New Game\n2. Exit\n", 2),
            # "row": ("Row to be updated (1-9): ", n),
            # "column": ("Column to be updated (1-9): ", n),
            # "fill": ("Number to fill cell (1-9): ", n)
        }

        self._option = 5

    ####################################################################################################
    # Queries

    def prompt(self, prompt_tuple):
        """Prompts and validates user input"""
        while True:
            try:
                prompt = prompt_tuple[0]
                value = int(input(prompt))
            except ValueError:
                print("ValueError: Response must be a number\n")
                continue

            num_options = prompt_tuple[1]
            if 0 < value <= num_options:
                break
            else:
                print("Invalid: Response must be a valid number\n")
                continue
        return value

    def prompt_move(self):
        """Prompts for player's move"""
        try:
            from_square = input("Enter a square to move from (e.g. b6): ").strip().lower()
            to_square = input("Enter a square to move to (e.g. e9): ").strip().lower()
            # try_move = game.make_move(from_square, to_square)
            while not self.make_move(from_square, to_square):
                self.display_game()
                print(self.get_turn_state().replace("_", " "))
                print("Move not valid. Try again")
                from_square = input("Enter a square to move from (e.g. b6): ").strip().lower()
                to_square = input("Enter a square to move to (e.g. e9): ").strip().lower()
        except ValueError:
            print("Illegal move! Please try again!!")

    def get_dict_prompt(self):
        """Returns the dictionary of prompts"""
        return self._dict_prompt

    def start_gess(self):
        """Starts the game"""
        self.display_game()
        print("BLACK STARTS")
        player_input = self.prompt(self.get_dict_prompt()["menu"])
        while player_input != self.get_option():
            player_input = self.chosen_option(player_input)

    def get_option(self):
        """A method called get_option to get the number of options"""
        return self._option

    def get_game_state(self):
        """
        A method called get_game_state that takes no parameters and returns 'UNFINISHED', 'BLACK_WON' or 'WHITE_WON'.
        :return: self._game_state
        """
        return self._game_state

    def get_num_blk_pcs(self):
        """
        A method called get_num_blk_pcs that takes no parameters and returns the number of black pieces on the board
        :return: self._num_blk_pcs
        """
        return self._num_blk_pcs

    def get_num_wht_pcs(self):
        """
        A method called get_num_wht_pcs that takes no parameters and returns the number of white pieces on the board
        :return: self._num_wht_pcs
        """
        return self._num_wht_pcs

    def get_board(self):
        """A method called get_board that takes no parameters and returns the abstract board"""
        return self._board

    def get_move_hist(self):
        """
        A method called get_move_hist that takes no parameters and returns a dictionary of all the moves made in the game.
        :return: self._move_hist
        """
        return self._move_hist

    def get_turn_state(self):
        """
        A method called get_turn_state that takes no parameters and returns 'BLACKS_TURN' OR 'WHITES_TURN'.
        :return: self._turn_state
        """
        return self._turn_state

    def display_game(self):
        """
        A method called display_game that takes no parameters and prints the game info in the following order:
            game state
            number of black and white pieces
            board and current positions of players' pieces
        """
        print('{:*^94}'.format("   Game state = " + self.get_game_state() + "   "))
        print("WHITE " + str(self.get_num_wht_pcs()), end='{:^78}'.format(' '))
        print(str(self.get_num_blk_pcs()) + " BLACK")
        print('{:-^94}'.format(''))
        for rows in range(self._num_rows + 1):
            print("| ", end="")
            for cols in range(self._num_cols):
                if cols == 0:
                    print(self._board[rows][cols].rjust(2) + " | ", end="")
                else:
                    print(self._board[rows][cols] + "   ", end="")
            print(self._board[self._num_rows - 1][self._num_cols - 1] + " |")
        print()

    ####################################################################################################
    # Commands

    def new_game(self):
        """
        A method called new_game that sets up a new game
        :return:
        """
        self._game_state = "UNFINISHED"
        self._num_blk_pcs = self._num_wht_pcs = 43  # each player starts with 43 pieces
        self._board = self.create_board()
        self._move_count = 0
        self._move_hist = {}
        self.display_game()

    def resign_game(self):
        """
        A method called resign_game that lets the current player concede the game, giving the other player the win.
        :return:
        """
        if self._game_state == "BLACK_WON" or self._game_state == "WHITE_WON":
            return

        if self._game_state == "UNFINISHED" and self._turn_state == "BLACKS_TURN":
            self._game_state = "WHITE_WON"
        else:
            self._game_state = "BLACK_WON"
        print(self.get_game_state().replace("_", " "))

    def chosen_option(self, user_input):
        """Executes chosen option from main menu and play"""
        if self.get_game_state() == "UNFINISHED":
            if user_input == 1:
                self.display_game()
            elif user_input == 2:
                print(self.get_turn_state().replace("_", " "))
            elif user_input == 3:
                self.prompt_move()
                self.display_game()
                if self.get_game_state() != "UNFINISHED":
                    print(self.get_game_state().replace("_", " "))
                    return self.prompt(self.get_dict_prompt()["play"])
                else:
                    print(self.get_turn_state().replace("_", " "))
            elif user_input == 4:
                self.resign_game()
                return self.prompt(self.get_dict_prompt()["play"])
        elif user_input == 1:
            self.new_game()
        elif user_input == 2:
            return self.get_option()
        return self.prompt(self.get_dict_prompt()["menu"])

    def make_move(self, from_square, to_square):
        """
        A method called make_move that takes two parameters - strings that represent the center square of the piece
        being moved and the desired new location of the center square. For example, make_move('b6', 'e9').
        If the indicated move is not legal for the current player, or if the game has already been won, then it should
        just return False. Otherwise it should make the indicated move, remove any captured stones, update the game state
        if necessary, update whose turn it is, and return True.

        In the make_move function, it will create a Move object (a representation of a move) and
        call the is_valid, complete_move, and check_game_won functions.

        :param from_square:
        :param to_square:
        :return: True/False
        """
        # check if game has already been won
        if self._game_state == "BLACK_WON" or self._game_state == "WHITE_WON":
            return False

        move = Move(from_square, to_square, self._board, self._turn_state, self._num_blk_pcs, self._num_wht_pcs)
        # check if move is valid
        if not move.is_valid():
            del move
            return False

        # game hasn't been won and move is legal
        self._move_count += 1
        self._move_hist[self._move_count] = move
        self._board = move.complete_move()

        # update number of pieces for both players
        self._num_blk_pcs = move.get_num_blk_after()
        self._num_wht_pcs = move.get_num_wht_after()

        # update turn_state to next player
        if self._turn_state == "BLACKS_TURN":
            # update game state if necessary
            if move.check_game_won() is True:
                if move.get_player_ring() is False and move.get_opponent_ring() is True:
                    self._game_state = "WHITE_WON"
                elif move.get_player_ring() is True and move.get_opponent_ring() is False:
                    self._game_state = "BLACK_WON"
            self._turn_state = "WHITES_TURN"
        else:  # self._turn_state is "WHITES_TURN":
            # update game state if necessary
            if move.check_game_won() is True:
                if move.get_player_ring() is False and move.get_opponent_ring() is True:
                    self._game_state = "BLACK_WON"
                elif move.get_player_ring() is True and move.get_opponent_ring() is False:
                    self._game_state = "WHITE_WON"
            self._turn_state = "BLACKS_TURN"

        return True

    def create_board(self):
        """
        A method called create_board that takes no parameters; Creates the Gess board and places each players' pieces in their starting
        positions, then returns the board.
        :return: board
        """
        board = [[' ' for i in range(self._num_rows + 2)] for j in range(self._num_cols + 1)]

        # labels playable squares
        for i in range(3, self._bound_rows + 1):
            for j in range(3, self._bound_cols + 1):
                board[i][j] = "-"

        # create row labels
        num = 1
        for i in range(2, self._num_rows):
            board[i][0] = str(num)
            num += 1

        # create column labels
        char = "a"
        for i in range(2, self._num_cols):
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

    def __init__(self, from_square, to_square, board_before, turn_state, num_blk_pcs, num_wht_pcs):
        """
        Initializes Move object
        :param from_square: board coordinates (row, column) as a tuple of the piece to be moved
        :param to_square: board coordinates (row, column) as a tuple where the piece is to be moved
        :param board_before: abstract representation of the board before the move
        :param turn_state: indicates which players' turn it is
        :param num_blk_pcs: number of black pieces on the board
        :param num_wht_pcs: number of white pieces on the board
        """
        # board coordinates (row, column) as a tuple of the piece to be moved
        self._from_square = from_square
        self._to_square = to_square

        # board coordinates adjusted to correct board index
        self._from_board_index = self.square_to_indices(from_square)
        self._to_board_index = self.square_to_indices(to_square)

        # board dimensions
        self._playable_area = (3, 21)  # playable board index area; inclusive [3, 21) non-inclusive
        self._rows = ('2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19')
        self._cols = ('b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's')

        # board
        self._board_before = board_before  # game layout before move
        self._board_after = []  # game layout after move
        for i in self._board_before:
            self._board_after.append(list(i))

        # players
        self._player = "B" if turn_state == "BLACKS_TURN" else "W"
        self._opponent = "W" if turn_state == "BLACKS_TURN" else "B"

        # ring presence
        self._game_won = False
        self._player_ring = False
        self._opponent_ring = False

        # number of pieces
        self._num_blk_before = num_blk_pcs
        self._num_blk_after = num_blk_pcs
        self._num_wht_before = num_wht_pcs
        self._num_wht_after = num_wht_pcs

        # move distance
        self._max_dist_w_center = 17
        self._max_dist_wo_center = 3
        self._dist = 0

    ####################################################################################################
    # Queries

    def is_valid(self):
        """
        A method called is_valid that takes no parameters and checks if the move is valid
        :return: True/False
        """
        # check if starting square is the same as destination square
        if self._from_square is self._to_square:
            return False

        # check if center square to be moved is within rows 2-19 and columns b-s
        if (''.join(col for col in self._from_square if col.isalpha()) or None) not in self._cols \
                or (''.join(row for row in self._from_square if row.isdigit()) or None) not in self._rows:
            return False

        # check if all 9 squares contain only pieces from player by:
        # first checking if there are any of the opponent's pieces
        for row in range(-1, 2):
            for col in range(-1, 2):
                if self._board_before[self._from_board_index[0] + row][self._from_board_index[1] + col] is self._opponent:
                    return False

        # second checking if it's not empty
        contains_player = False
        for row in range(-1, 2):
            for col in range(-1, 2):
                if self._board_before[self._from_board_index[0] + row][self._from_board_index[1] + col] is self._player:
                    contains_player = True
                    break

        if contains_player is False:
            return False

        # check if to_board_index is outside of boundaries (center square can't move outside of board)
        if self._to_board_index[0] < 3 or self._to_board_index[0] > 20 or self._to_board_index[1] < 3 or self._to_board_index[
            1] > 20:
            return False

        # eliminate invalid moves by calculating the distance from one square to another.
        # center square can only move north/up, south/down, east/right, west/left where the distance will be an integer value,
        # and diagonally (NW, NE, SE, SW) which will be an (n * sqrt(2)) where n is an int
        self._dist = self.calc_dist(self._from_board_index, self._to_board_index)

        if self._dist.is_integer():
            self._dist = int(self._dist)
        else:
            self._dist = self._dist / (2 ** (1 / 2.0))
            if self._dist.is_integer() or abs(int(self._dist) - self._dist) < 1 * 10 ** -12:
                self._dist = int(self._dist)
            elif abs(int(self._dist + 1) - self._dist) < 1 * 10 ** -12:
                self._dist = int(self._dist + 1)

        # checks if the distance between two squares is greater than the maximum of 17 on the board.
        if self._dist > self._max_dist_w_center:
            return False

        # checks if center square contains the player's piece and whether the distance is greater than 3
        if self._board_before[self._from_board_index[0]][
            self._from_board_index[1]] == "-" and self._dist > self._max_dist_wo_center:
            return False

        self.remove_3x3()

        return self.check_path()

    def get_board_after(self):
        """
        A method called get_board_after that takes no parameters and returns the updated board after the move
        :return: self._board_after
        """
        return self._board_after

    def get_player_ring(self):
        """
        A method called get_player_ring that takes no parameters and returns True if the player's ring is present, otherwise returns
        False
        :return: self._player_ring
        """
        return self._player_ring

    def get_opponent_ring(self):
        """
        A method called get_opponent_ring that takes no parameters and returns True if the opponent's ring is present, otherwise returns
        False
        :return: self._opponent_ring
        """
        return self._opponent_ring

    def get_num_blk_after(self):
        """
        A method called get_num_blk_after that takes no parameters and returns the number of black pieces after the move
        :return: self._num_blk_after
        """
        return self._num_blk_after

    def get_num_wht_after(self):
        """
        A method called get_num_wht_after that takes no parameters and returns the number of white pieces after the move
        :return: self._num_wht_after
        """
        return self._num_wht_after

    def check_path(self):
        """Checks validity of movement direction, then checks it's path for obstructions"""
        if self._to_board_index[0] < self._from_board_index[0] and self._to_board_index[1] == self._from_board_index[1]:
            # check if N piece present
            if self._board_before[self._from_board_index[0] - 1][self._from_board_index[1]] is not self._player:
                return False
            # check N path
            for index in range(1, self._dist + 1):
                pcs_3x3 = self.check_3x3(self._from_board_index[0] - index, self._from_board_index[1])
                if index == self._dist:
                    return True
                elif self._player in pcs_3x3 or self._opponent in pcs_3x3:
                    return False
        elif self._to_board_index[0] < self._from_board_index[0] and self._to_board_index[1] > self._from_board_index[1]:
            # check if NE piece is present
            if self._board_before[self._from_board_index[0] - 1][self._from_board_index[1] + 1] is not self._player:
                return False
            # check NE path
            for index in range(1, self._dist + 1):
                pcs_3x3 = self.check_3x3(self._from_board_index[0] - index, self._from_board_index[1] + index)
                if index == self._dist:
                    return True
                elif self._player in pcs_3x3 or self._opponent in pcs_3x3:
                    return False
        elif self._to_board_index[0] == self._from_board_index[0] and self._to_board_index[1] > self._from_board_index[1]:
            # check if E piece is present
            if self._board_before[self._from_board_index[0]][self._from_board_index[1] + 1] is not self._player:
                return False
            # check E path
            for index in range(1, self._dist + 1):
                pcs_3x3 = self.check_3x3(self._from_board_index[0], self._from_board_index[1] + index)
                if index == self._dist:
                    return True
                elif self._player in pcs_3x3 or self._opponent in pcs_3x3:
                    return False
        elif self._to_board_index[0] > self._from_board_index[0] and self._to_board_index[1] > self._from_board_index[1]:
            # check if SE piece is present
            if self._board_before[self._from_board_index[0] + 1][self._from_board_index[1] + 1] is not self._player:
                return False
            # check SE path
            for index in range(1, self._dist + 1):
                pcs_3x3 = self.check_3x3(self._from_board_index[0] + index, self._from_board_index[1] + index)
                if index == self._dist:
                    return True
                elif self._player in pcs_3x3 or self._opponent in pcs_3x3:
                    return False
        elif self._to_board_index[0] > self._from_board_index[0] and self._to_board_index[1] == self._from_board_index[1]:
            # check if S piece is present
            if self._board_before[self._from_board_index[0] + 1][self._from_board_index[1]] is not self._player:
                return False
            # check S path
            for index in range(1, self._dist + 1):
                pcs_3x3 = self.check_3x3(self._from_board_index[0] + index, self._from_board_index[1])
                if index == self._dist:
                    return True
                elif self._player in pcs_3x3 or self._opponent in pcs_3x3:
                    return False
        elif self._to_board_index[0] > self._from_board_index[0] and self._to_board_index[1] < self._from_board_index[1]:
            # check if SW piece is present
            if self._board_before[self._from_board_index[0] + 1][self._from_board_index[1] - 1] is not self._player:
                return False
            # check SW path
            for index in range(1, self._dist + 1):
                pcs_3x3 = self.check_3x3(self._from_board_index[0] + index, self._from_board_index[1] - index)
                if index == self._dist:
                    return True
                elif self._player in pcs_3x3 or self._opponent in pcs_3x3:
                    return False
        elif self._to_board_index[0] == self._from_board_index[0] and self._to_board_index[1] < self._from_board_index[1]:
            # check if W piece is present
            if self._board_before[self._from_board_index[0]][self._from_board_index[1] - 1] is not self._player:
                return False
            # check W path
            for index in range(1, self._dist + 1):
                pcs_3x3 = self.check_3x3(self._from_board_index[0], self._from_board_index[1] - index)
                if index == self._dist:
                    return True
                elif self._player in pcs_3x3 or self._opponent in pcs_3x3:
                    return False
        else:
            # check if NW piece is present
            if self._board_before[self._from_board_index[0] - 1][self._from_board_index[1] - 1] is not self._player:
                return False
            # check NW path
            for index in range(0, self._dist + 1):
                pcs_3x3 = self.check_3x3(self._from_board_index[0] - index, self._from_board_index[1] - index)
                if index == self._dist:
                    return True
                elif self._player in pcs_3x3 or self._opponent in pcs_3x3:
                    return False

        return True

    def check_3x3(self, row, col):
        return (self._board_after[row][col],  # C
                self._board_after[row - 1][col],  # N from C
                self._board_after[row - 1][col + 1],  # NE from C
                self._board_after[row][col + 1],  # E from C
                self._board_after[row + 1][col + 1],  # SE from C
                self._board_after[row + 1][col],  # S from C
                self._board_after[row + 1][col - 1],  # SW from C
                self._board_after[row][col - 1],  # W from C
                self._board_after[row - 1][col - 1])  # NW from C

    ####################################################################################################
    # Commands

    def calc_dist(self, point1, point2):
        """
        Calculates distance between two points
        :param point1: starting point of center square
        :param point2: ending point of center square
        :return: distance
        """
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** (1 / 2.0)

    def square_to_indices(self, square):
        """
        A method called square_to_indices that takes no parameters and converts the square coordinates to the equivalent indices on the
        board
        :param square:
        :return: indices on the board equivalent to square
        """
        row_num, col_letter = (''.join(row for row in square if row.isdigit()) or None,
                               ''.join(col for col in square if col.isalpha()) or None)
        return int(row_num) + 1, ord(col_letter) - 95

    def complete_move(self):
        """
        A method called complete_move that takes no parameters and completes the move by updating the board and then returning the board
        after the move
        :return: self._board_after
        """
        # make a copy of all 1-9 pieces to be moved
        pcs_3x3 = []
        for row in range(-1, 2):
            for col in range(-1, 2):
                if self._board_before[self._from_board_index[0] + row][self._from_board_index[1] + col] == " ":
                    pcs_3x3.append('-')
                else:
                    pcs_3x3.append(self._board_before[self._from_board_index[0] + row][self._from_board_index[1] + col])
        pcs_3x3 = tuple(pcs_3x3)

        # replace all pieces surrounding center coordinate where piece is to be moved to
        index = 0
        for row in range(-1, 2):
            for col in range(-1, 2):
                if self._board_after[self._to_board_index[0] + row][self._to_board_index[1] + col] == "B":
                    self._num_blk_after -= 1
                elif self._board_after[self._to_board_index[0] + row][self._to_board_index[1] + col] == "W":
                    self._num_wht_after -= 1
                if self._board_after[self._to_board_index[0] + row][self._to_board_index[1] + col] != " ":
                    self._board_after[self._to_board_index[0] + row][self._to_board_index[1] + col] = pcs_3x3[index]
                    if pcs_3x3[index] == "B":
                        self._num_blk_after += 1
                    elif pcs_3x3[index] == "W":
                        self._num_wht_after += 1
                index += 1

        return self._board_after

    def check_game_won(self):
        """
        A method called check_game_won that takes no parameters and checks if a player has won the game.
        Returns True if a player has won the game, and False otherwise.
        :return: self._game_won
        """
        for i in range(self._playable_area[0] + 1, self._playable_area[1] - 1):
            for j in range(self._playable_area[0] + 1, self._playable_area[1] - 1):
                if self._board_after[i][j] == "-":
                    # check if player's ring is present (clock-wise from Center)
                    if (self._board_after[i - 1][j] == self._player and  # check N from C
                            self._board_after[i - 1][j + 1] == self._player and  # check NE from C
                            self._board_after[i][j + 1] == self._player and  # check E from C
                            self._board_after[i + 1][j + 1] == self._player and  # check SE from C
                            self._board_after[i + 1][j] == self._player and  # check S from C
                            self._board_after[i + 1][j - 1] == self._player and  # check SW from C
                            self._board_after[i][j - 1] == self._player and  # check W from C
                            self._board_after[i - 1][j - 1] == self._player):  # check NW from C
                        self._player_ring = True

                    # check if opponent's ring is present (clock-wise from Center)
                    if (self._board_after[i - 1][j] == self._opponent and  # check N from C
                            self._board_after[i - 1][j + 1] == self._opponent and  # check NE from C
                            self._board_after[i][j + 1] == self._opponent and  # check E from C
                            self._board_after[i + 1][j + 1] == self._opponent and  # check SE from C
                            self._board_after[i + 1][j] == self._opponent and  # check S from C
                            self._board_after[i + 1][j - 1] == self._opponent and  # check SW from C
                            self._board_after[i][j - 1] == self._opponent and  # check W from C
                            self._board_after[i - 1][j - 1] == self._opponent):  # check NW from C
                        self._opponent_ring = True

        if self._player_ring is False or self._opponent_ring is False:
            self._game_won = True

        return self._game_won

    def remove_3x3(self):
        """Removes the 3x3 pieces to be moved; Represents a player "picking up" the pieces"""
        for row in range(-1, 2):
            for col in range(-1, 2):
                if self._board_after[self._from_board_index[0] + row][self._from_board_index[1] + col] == "B":
                    self._num_blk_after -= 1
                elif self._board_after[self._from_board_index[0] + row][self._from_board_index[1] + col] == "W":
                    self._num_wht_after -= 1
                if self._board_after[self._from_board_index[0] + row][self._from_board_index[1] + col] != " ":
                    self._board_after[self._from_board_index[0] + row][self._from_board_index[1] + col] = "-"


if __name__ == "__main__":
    game = GessGame()
    game.start_gess()

