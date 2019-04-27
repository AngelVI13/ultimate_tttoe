from gui.colors import *


DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 600
BOARD_WIDTH = 480
BOARD_HEIGHT = 480

BORDER_THICKNESS = 2
BORDERS = {
    'top_left':     (BORDER_THICKNESS, BORDER_THICKNESS, -BORDER_THICKNESS,     -BORDER_THICKNESS),
    'top_right':    (0,                BORDER_THICKNESS, -BORDER_THICKNESS,     -BORDER_THICKNESS),
    'bottom_left':  (BORDER_THICKNESS, 0,                -BORDER_THICKNESS,     -BORDER_THICKNESS),
    'bottom_right': (0,                0,                -BORDER_THICKNESS,     -BORDER_THICKNESS),
    'u_shape':      (BORDER_THICKNESS, 0,                -2 * BORDER_THICKNESS, -BORDER_THICKNESS),
    'n_shape':      (BORDER_THICKNESS, BORDER_THICKNESS, -2 * BORDER_THICKNESS, -BORDER_THICKNESS),
    'o_shape':      (BORDER_THICKNESS, BORDER_THICKNESS, -2 * BORDER_THICKNESS, -2 * BORDER_THICKNESS),
    ']_shape':      (0,                BORDER_THICKNESS, -BORDER_THICKNESS,     -2 * BORDER_THICKNESS),
    '[_shape':      (BORDER_THICKNESS, BORDER_THICKNESS, -BORDER_THICKNESS,     -2 * BORDER_THICKNESS),
}

SUB_GRID_PADDING = 11
MAIN_BOX_WIDTH = BOARD_WIDTH / 3
MAIN_BOX_HEIGHT = BOARD_HEIGHT / 3
CELL_WIDTH = MAIN_BOX_WIDTH / 3
CELL_HEIGHT = MAIN_BOX_HEIGHT / 3
# offset for main grid from main window
OFFSET_X, OFFSET_Y = (DISPLAY_WIDTH - BOARD_WIDTH) / 2, (DISPLAY_HEIGHT - BOARD_HEIGHT) / 2

HIGHLIGHT_COLOR = GREEN
BORDER_COLOR = BLACK
BOX_COLOR = WHITE

# In these parameters the values for x & y will the added to the current position computed for each grid cell
MAIN_GRID_DRAW_PARAMETERS = [
    {'border': 'bottom_right', 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'highlight_colour': HIGHLIGHT_COLOR,
     'x': OFFSET_X, 'y': OFFSET_Y,
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    {'border': 'u_shape', 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'highlight_colour': HIGHLIGHT_COLOR,
     'x': OFFSET_X + BOARD_WIDTH / 3, 'y': OFFSET_Y,
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    {'border': 'bottom_left', 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'highlight_colour': HIGHLIGHT_COLOR,
     'x': OFFSET_X + BOARD_WIDTH * (2 / 3), 'y': OFFSET_Y,
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    # middle row
    {'border': ']_shape', 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'highlight_colour': HIGHLIGHT_COLOR,
     'x': OFFSET_X, 'y': OFFSET_Y + BOARD_HEIGHT / 3,
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    {'border': 'o_shape', 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'highlight_colour': HIGHLIGHT_COLOR,
     'x': OFFSET_X + BOARD_WIDTH / 3, 'y': OFFSET_Y + BOARD_HEIGHT / 3,
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    {'border': '[_shape', 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'highlight_colour': HIGHLIGHT_COLOR,
     'x': OFFSET_X + BOARD_WIDTH * (2 / 3), 'y': OFFSET_Y + BOARD_HEIGHT / 3,
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    # bottom row
    {'border': 'top_right', 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'highlight_colour': HIGHLIGHT_COLOR,
     'x': OFFSET_X, 'y': OFFSET_Y + BOARD_HEIGHT * (2 / 3),
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    {'border': 'n_shape', 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'highlight_colour': HIGHLIGHT_COLOR,
     'x': OFFSET_X + BOARD_WIDTH / 3, 'y': OFFSET_Y + BOARD_HEIGHT * (2 / 3),
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
    {'border': 'top_left', 'border_colour': BORDER_COLOR, 'box_colour': BOX_COLOR,
     'highlight_colour': HIGHLIGHT_COLOR,
     'x': OFFSET_X + BOARD_WIDTH * (2 / 3), 'y': OFFSET_Y + BOARD_HEIGHT * (2 / 3),
     'w': MAIN_BOX_WIDTH, 'h': MAIN_BOX_HEIGHT},
]
