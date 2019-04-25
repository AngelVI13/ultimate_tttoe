from collections import deque


PLAYER_X = 1
PLAYER_O = -1
NO_PLAYER = 0

STR_MATRIX = {
    PLAYER_X: 'X',
    PLAYER_O: 'O',
    NO_PLAYER: '-'
}

ROWS = 3
BOARD_SIZE = ROWS*ROWS

LOSS = 0.0
DRAW = 0.5
WIN = 1.0


class BaseBoard:
    """Defines the general structure which a board implementation must implement"""
    def __init__(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def __copy__(self):
        raise NotImplementedError

    def make_move(self, move):
        raise NotImplementedError

    def take_move(self):
        raise NotImplementedError

    def get_moves(self):
        raise NotImplementedError

    def get_result(self, player_jm):
        raise NotImplementedError


class Board:
    def __init__(self):
        self.pos = [0] * BOARD_SIZE
        self.side = PLAYER_X
        self.playerJustMoved = PLAYER_O
        self.history = deque()

    def __str__(self):
        lines = []
        for combo in zip(*[self.pos[i::ROWS] for i in range(ROWS)]):
            lines.extend(['{:<5}'.format(STR_MATRIX[elem]) for elem in combo])
            lines.append('\n')
        return ''.join(lines)

    def __copy__(self):
        _b = Board()
        _b.pos = self.pos[:]  # copy list
        _b.side = self.side  # todo remove this, not needed since player just moved
        _b.playerJustMoved = self.playerJustMoved
        _b.history = self.history.copy()  # todo copying deque is too slow
        return _b

    def make_move(self, move):
        assert move in self.get_moves(), 'Position is already occupied'

        self.pos[move] = self.side
        self.side = -self.side  # change side to move
        self.playerJustMoved = -self.playerJustMoved
        self.history.append(move)

    def take_move(self):
        move = self.history.pop()
        self.pos[move] = NO_PLAYER
        self.side = -self.side  # change side to move
        self.playerJustMoved = -self.playerJustMoved

    def get_moves(self):
        return [idx for idx, value in enumerate(self.pos) if value == NO_PLAYER]

    def get_result(self, player_jm):
        cols_combo = [self.pos[i::ROWS] for i in range(ROWS)]
        rows_combo = list(zip(*cols_combo))
        # print(cols_combo)
        # print(row s_combo)

        for i in range(ROWS):
            # Sum a row and a column
            row_result, col_result = sum(rows_combo[i]), sum(cols_combo[i])

            # Check if sum of values of a row is not equal to number of rows i.e. all 1s or all -1s
            if abs(row_result) == ROWS:
                return WIN if int(row_result / ROWS) == player_jm else LOSS

            if abs(col_result) == ROWS:
                return WIN if int(col_result / ROWS) == player_jm else LOSS

        # Sum values on Right diagonal
        # Look at right Diagonal
        # exclude last element since it is not part of the diagonal
        # i.e. if you have [1, 2, 3,
        #                   4, 5, 6,
        #                   7 ,8 ,9] then right diagonal is [3, 5, 7]
        # i.e. starting from the right corner the diagonal is formed by every second number
        # (3, 5, 7), however this will also result in 9 being included which it should not be
        # therefore we remove it
        result = sum(self.pos[ROWS - 1::ROWS - 1][:-1])
        if abs(result) == ROWS:
            return WIN if int(result / ROWS) == player_jm else LOSS

        # Left diagonal
        result = sum(self.pos[::ROWS + 1])
        if abs(result) == ROWS:
            return WIN if int(result / ROWS) == player_jm else LOSS

        # Lastly check if no available squares are on the board => TIE
        if sum([abs(elem) for elem in self.pos]) == BOARD_SIZE:
            return DRAW
