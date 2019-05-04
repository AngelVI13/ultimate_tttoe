from board.constants import *


class BaseBoard:
    """Defines the general structure which a board implementation
    must implement in order to be compatible with the MCTS game engine
    """

    def __str__(self):
        raise NotImplementedError

    def __copy__(self):
        raise NotImplementedError

    def make_move(self, *args, **kwargs):
        raise NotImplementedError

    def take_move(self):
        raise NotImplementedError

    def get_moves(self):
        raise NotImplementedError

    def get_result(self, player_jm):
        raise NotImplementedError


class Board:
    """Board implementation for a single NxN board"""

    def __init__(self):
        self.pos = [0] * BOARD_SIZE

    def get_row_strings(self):
        lines = []
        for combo in zip(*[self.pos[i::ROWS] for i in range(ROWS)]):
            lines.append(''.join(['{:<5}'.format(STR_MATRIX[elem]) for elem in combo]))
        return lines

    def __copy__(self):
        _b = Board()
        _b.pos = self.pos[:]  # copy list
        return _b

    def make_move(self, move, side):
        assert move in self.get_moves(), 'Position is already occupied'

        self.pos[move] = side

    def take_move(self, move):
        self.pos[move] = NO_PLAYER

    def get_moves(self):
        return [idx for idx, value in enumerate(self.pos) if value == NO_PLAYER]

    def get_result(self, board=None):
        if board is None:
            board = self.pos

        cols_combo = [board[i::ROWS] for i in range(ROWS)]
        rows_combo = list(zip(*cols_combo))

        for i in range(ROWS):
            # Sum a row and a column
            row_result, col_result = sum(rows_combo[i]), sum(cols_combo[i])

            # Check if sum of values of a row is not equal to number of rows
            # i.e. all 1s or all -1s
            if abs(row_result) == ROWS:
                return int(row_result / ROWS)

            if abs(col_result) == ROWS:
                return int(col_result / ROWS)

        # Sum values on Right diagonal
        # Look at right Diagonal
        # exclude last element since it is not part of the diagonal
        # i.e. if you have [1, 2, 3,
        #                   4, 5, 6,
        #                   7 ,8 ,9] then right diagonal is [3, 5, 7]
        # i.e. starting from the right corner the diagonal is formed by
        # every second number (3, 5, 7), however this will also result
        # in 9 being included which it should not be therefore we remove it
        result = sum(board[ROWS - 1::ROWS - 1][:-1])
        if abs(result) == ROWS:
            return int(result / ROWS)

        # Left diagonal
        result = sum(board[::ROWS + 1])
        if abs(result) == ROWS:
            return int(result / ROWS)

        # Lastly check if no available squares are on the board => TIE
        if sum([abs(elem) for elem in board]) == BOARD_SIZE:
            # here 0.5 indicates a DRAW and for ultimate tttoe
            # this means that a drawn board is not taken into account for
            # any player
            return DRAW
