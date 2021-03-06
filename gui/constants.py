from enum import IntEnum, Enum, auto
from itertools import count

from gui.colors import *
from board.constants import PLAYER_X, PLAYER_O, DRAW

DISPLAY_SCALING = 3
DISPLAY_WIDTH = 600 * DISPLAY_SCALING
DISPLAY_HEIGHT = 600 * DISPLAY_SCALING
BOARD_WIDTH = 480 * DISPLAY_SCALING
BOARD_HEIGHT = 480 * DISPLAY_SCALING

# noinspection PyTypeChecker
# Create an enum of values starting from 0
Grid = IntEnum('Grid', zip([
    'TOP_LEFT', 'TOP_MIDDLE', 'TOP_RIGHT',
    'MIDDLE_LEFT', 'MIDDLE_MIDDLE', 'MIDDLE_RIGHT',
    'BOTTOM_LEFT', 'BOTTOM_MIDDLE', 'BOTTOM_RIGHT'], count()))


class GameType(Enum):
    SINGLE_PLAYER = auto()
    MULTI_PLAYER = auto()
    DEMO_MODE = auto()


BORDER_THICKNESS = 2
BORDERS = {
    Grid.TOP_LEFT:      (0, 0, -BORDER_THICKNESS, -BORDER_THICKNESS),
    Grid.TOP_MIDDLE:    (BORDER_THICKNESS, 0, -2 * BORDER_THICKNESS, -BORDER_THICKNESS),
    Grid.TOP_RIGHT:     (BORDER_THICKNESS, 0, -BORDER_THICKNESS, -BORDER_THICKNESS),

    Grid.MIDDLE_LEFT:   (0, BORDER_THICKNESS, -BORDER_THICKNESS, -2 * BORDER_THICKNESS),
    Grid.MIDDLE_MIDDLE: (BORDER_THICKNESS, BORDER_THICKNESS, -2 * BORDER_THICKNESS, -2 * BORDER_THICKNESS),
    Grid.MIDDLE_RIGHT:  (BORDER_THICKNESS, BORDER_THICKNESS, -BORDER_THICKNESS, -2 * BORDER_THICKNESS),

    Grid.BOTTOM_LEFT:   (0, BORDER_THICKNESS, -BORDER_THICKNESS, -BORDER_THICKNESS),
    Grid.BOTTOM_MIDDLE: (BORDER_THICKNESS, BORDER_THICKNESS, -2 * BORDER_THICKNESS, -BORDER_THICKNESS),
    Grid.BOTTOM_RIGHT:  (BORDER_THICKNESS, BORDER_THICKNESS, -BORDER_THICKNESS, -BORDER_THICKNESS),
}

SUB_GRID_PADDING = 11
MAIN_BOX_WIDTH = BOARD_WIDTH / 3
MAIN_BOX_HEIGHT = BOARD_HEIGHT / 3
CELL_WIDTH = MAIN_BOX_WIDTH / 3
CELL_HEIGHT = MAIN_BOX_HEIGHT / 3
# offset for main grid from main window
OFFSET_X, OFFSET_Y = (DISPLAY_WIDTH - BOARD_WIDTH) / 2, (DISPLAY_HEIGHT - BOARD_HEIGHT) / 2

# Menu buttons
BUTTON_WIDTH, BUTTON_HEIGHT = 300 * DISPLAY_SCALING, 50 * DISPLAY_SCALING
BUTTON_Y_SPACING = 1.5
BUTTON_X_SPACING = 0.5

MENU_BUTTON_PROPERTIES = {  # todo add names instead of integers as keys
    0: {'x': (DISPLAY_WIDTH-BUTTON_WIDTH) / 2, 'y': (DISPLAY_HEIGHT / 3) + 1*BUTTON_HEIGHT*BUTTON_Y_SPACING,
        'w': BUTTON_WIDTH, 'h': BUTTON_HEIGHT, 'ic': PURPLE, 'ac': PURPLE_HIGHLIGHT},
    1: {'x': (DISPLAY_WIDTH-BUTTON_WIDTH) / 2, 'y': (DISPLAY_HEIGHT / 3) + 2*BUTTON_HEIGHT*BUTTON_Y_SPACING,
        'w': BUTTON_WIDTH, 'h': BUTTON_HEIGHT, 'ic': PURPLE, 'ac': PURPLE_HIGHLIGHT},
    2: {'x': (DISPLAY_WIDTH-BUTTON_WIDTH) / 2, 'y': (DISPLAY_HEIGHT / 3) + 3*BUTTON_HEIGHT*BUTTON_Y_SPACING,
        'w': BUTTON_WIDTH, 'h': BUTTON_HEIGHT, 'ic': PURPLE, 'ac': PURPLE_HIGHLIGHT},
    3: {'x': (DISPLAY_WIDTH-BUTTON_WIDTH) / 2, 'y': (DISPLAY_HEIGHT / 3) + 4*BUTTON_HEIGHT*BUTTON_Y_SPACING,
        'w': BUTTON_WIDTH, 'h': BUTTON_HEIGHT, 'ic': RED,   'ac': RED_HIGHLIGHT},
}

GRID_RESULT_COLORS = {
    PLAYER_X: RED_HIGHLIGHT,
    PLAYER_O: BLUE_HIGHLIGHT,
    DRAW: GREY
}

BORDER_COLOR = BLACK
BOX_COLOR = WHITE

# In these parameters the values for x & y will the added to the current position computed for each grid cell
MAIN_GRID_DRAW_PARAMETERS = [
    {'border': Grid.TOP_LEFT, 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'x': OFFSET_X, 'y': OFFSET_Y,
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    {'border': Grid.TOP_MIDDLE, 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'x': OFFSET_X + BOARD_WIDTH / 3, 'y': OFFSET_Y,
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    {'border': Grid.TOP_RIGHT, 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'x': OFFSET_X + BOARD_WIDTH * (2 / 3), 'y': OFFSET_Y,
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    # middle row
    {'border': Grid.MIDDLE_LEFT, 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'x': OFFSET_X, 'y': OFFSET_Y + BOARD_HEIGHT / 3,
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    {'border': Grid.MIDDLE_MIDDLE, 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'x': OFFSET_X + BOARD_WIDTH / 3, 'y': OFFSET_Y + BOARD_HEIGHT / 3,
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    {'border': Grid.MIDDLE_RIGHT, 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'x': OFFSET_X + BOARD_WIDTH * (2 / 3), 'y': OFFSET_Y + BOARD_HEIGHT / 3,
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    # bottom row
    {'border': Grid.BOTTOM_LEFT, 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'x': OFFSET_X, 'y': OFFSET_Y + BOARD_HEIGHT * (2 / 3),
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    {'border': Grid.BOTTOM_MIDDLE, 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'x': OFFSET_X + BOARD_WIDTH / 3, 'y': OFFSET_Y + BOARD_HEIGHT * (2 / 3),
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    {'border': Grid.BOTTOM_RIGHT, 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'x': OFFSET_X + BOARD_WIDTH * (2 / 3), 'y': OFFSET_Y + BOARD_HEIGHT * (2 / 3),
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
]

GAME_FRAMES_PER_SECOND = 30
MENU_FRAMES_PER_SECOND = 30
# after entering game loop pause for some time before allowing the user to click
# fixes issues with accidental clicks
PAUSE_BEFORE_USER_INPUT = 1

COLOR_BOX_SIZE = 20 * DISPLAY_SCALING
COLOR_BOX_BORDER_THICKNESS = 2 * DISPLAY_SCALING

OVERLAY_W, OVERLAY_H = 140 * DISPLAY_SCALING, 80 * DISPLAY_SCALING
RESULT_OVERLAY = {
    'x': DISPLAY_WIDTH / 2 - OVERLAY_W / 2,
    'y': DISPLAY_HEIGHT / 2 - OVERLAY_H / 2,
    'w': OVERLAY_W,
    'h': OVERLAY_H
}
