from functools import total_ordering

import pygame
from gui.constants import *
from board.ultimate_board import *


@total_ordering
class Cell:
    """Defines a hashable cell container. Used to store info for all cells in all subgrids."""

    __slots__ = ['pos_x', 'pos_y', 'width', 'height', 'player', 'board_idx', 'cell_idx']

    def __init__(self, pos_x, pos_y, width, height, player, board_idx=None, cell_idx=None):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.player = player
        self.board_idx = board_idx
        self.cell_idx = cell_idx

    def __repr__(self):
        return '{name}(pos_x={x}, pos_y={y}, width={w}, height={h}, player={p})'.format(
            name=self.__class__.__name__, x=self.pos_x, y=self.pos_y, w=self.width, h=self.height, p=self.player)

    def __hash__(self):
        return hash((self.pos_x, self.pos_y))

    def __eq__(self, other):
        return self.pos_x == other.pos_x and self.pos_y == other.pos_y

    def __lt__(self, other):
        return self.pos_x < other.pos_x and self.pos_y < other.pos_y


class GuiBoard:
    colors = {
        PLAYER_X: RED,
        PLAYER_O: BLUE,
    }

    clicked_cells = set()  # a set of all clicked cells
    all_cells = set()  # a set of all created cells
    on_cell_clicked = None  # callback method for action on cell clicked

    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('Ultimate Tic Tac Toe')
        self.clock = pygame.time.Clock()

    @staticmethod
    def get_text_objects(text, font):
        text_surface = font.render(text, True, BLACK)
        return text_surface, text_surface.get_rect()

    def message_display(self, text, pos=None, size=60):
        if pos is None:
            pos_x, pos_y = DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2
        else:
            pos_x, pos_y = pos

        large_text = pygame.font.Font('freesansbold.ttf', size)
        text_surf, text_rect = self.get_text_objects(text, large_text)
        text_rect.center = (pos_x, pos_y)
        self.gameDisplay.blit(text_surf, text_rect)
        pygame.display.update()

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        print(click)
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.gameDisplay, ac, (x, y, w, h))

            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(self.gameDisplay, ic, (x, y, w, h))

        small_text = pygame.font.SysFont("comicsansms", 20)
        text_surf, text_rect = self.get_text_objects(msg, small_text)
        text_rect.center = ((x + (w / 2)), (y + (h / 2)))
        self.gameDisplay.blit(text_surf, text_rect)

    @staticmethod
    def quit_game():
        pygame.quit()
        quit()

    def draw_subcell(self, border, border_colour, box_colour, highlight_colour, x, y, w, h, grid_idx, action=None):
        # Draw bounding box of cell
        mod_x, mod_y, mod_w, mod_h = BORDERS[border]
        pygame.draw.rect(self.gameDisplay, border_colour, (x, y, w, h))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        inner_x, inner_y, inner_w, inner_h = x + mod_x, y + mod_y, w + mod_w, h + mod_h

        # keep track of all cells on the board
        cell = Cell(pos_x=inner_x, pos_y=inner_y, width=inner_w, height=inner_h,
                    player=None, board_idx=grid_idx, cell_idx=border)
        if cell not in self.all_cells:
            self.all_cells.add(cell)

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.gameDisplay, highlight_colour, (inner_x, inner_y, inner_w, inner_h))

            if click[0] == 1 and action is not None:
                action(inner_x, inner_y, inner_w, inner_h, grid_idx, border)
        else:
            pygame.draw.rect(self.gameDisplay, box_colour, (inner_x, inner_y, inner_w, inner_h))

    def draw_sub_grid(self, border, border_colour, box_colour, highlight_colour, x, y, w, h):
        # draw bounding box of subgrid
        mod_x, mod_y, mod_w, mod_h = BORDERS[border]
        pygame.draw.rect(self.gameDisplay, border_colour, (x, y, w, h))
        # update position and size values for inner rectangle
        x, y = x + mod_x, y + mod_y
        w, h = w + mod_w, h + mod_h
        pygame.draw.rect(self.gameDisplay, box_colour, (x, y, w, h))

        # calculate inner box for subgrid
        cell_size = min(w, h)
        x, y = x + 2 * SUB_GRID_PADDING, y + 2 * SUB_GRID_PADDING
        w = h = cell_size - 4 * SUB_GRID_PADDING
        cell_width_ = w / 3
        cell_height_ = h / 3

        positions = [
            # top row
            {'border': Grid.TOP_LEFT,      'x': x, 'y': y},
            {'border': Grid.TOP_MIDDLE,    'x': x + w * (1 / 3), 'y': y},
            {'border': Grid.TOP_RIGHT,     'x': x + w * (2 / 3), 'y': y},

            # middle row
            {'border': Grid.MIDDLE_LEFT,   'x': x, 'y': y + (h / 3)},
            {'border': Grid.MIDDLE_MIDDLE, 'x': x + w * (1 / 3), 'y': y + (h / 3)},
            {'border': Grid.MIDDLE_RIGHT,  'x': x + w * (2 / 3), 'y': y + (h / 3)},

            # bottom row
            {'border': Grid.BOTTOM_LEFT,   'x': x, 'y': y + h * (2 / 3)},
            {'border': Grid.BOTTOM_MIDDLE, 'x': x + w * (1 / 3), 'y': y + h * (2 / 3)},
            {'border': Grid.BOTTOM_RIGHT,  'x': x + w * (2 / 3), 'y': y + h * (2 / 3)},
        ]

        for position in positions:
            # here border is the index of which grid all of the cells are part of
            self.draw_subcell(**position, border_colour=border_colour, box_colour=box_colour, w=cell_width_,
                              h=cell_height_, highlight_colour=highlight_colour, grid_idx=border,
                              action=self.on_cell_clicked)

    def draw_main_grid(self):
        for parameters in MAIN_GRID_DRAW_PARAMETERS:
            self.draw_sub_grid(**parameters)

    def draw_clicked_cells(self):
        for cell in self.clicked_cells:
            pygame.draw.rect(self.gameDisplay, self.colors[cell.player],
                             (cell.pos_x, cell.pos_y, cell.width, cell.height))