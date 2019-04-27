"""Defines various constants used in the base and ultimate board implementations such as values for each player,
their string representation for outputting to console and the value of a win/loss/draw for the MCTS engine.
"""

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
