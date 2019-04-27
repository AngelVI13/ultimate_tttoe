import pygame
from gui.constants import *
from board.ultimate_board import *


class GuiBoard:
    colors = {
        PLAYER_X: RED,
        PLAYER_O: BLUE,
    }

    clicked_cells = []

    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('Ultimate Tic Tac Toe')
        self.clock = pygame.time.Clock()

        self.player = PLAYER_X  # todo this should be replaced with value from ultimate board

    @staticmethod
    def get_text_objects(text, font):
        text_surface = font.render(text, True, BLACK)
        return text_surface, text_surface.get_rect()

    def message_display(self, text):
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        text_surf, text_rect = self.get_text_objects(text, large_text)
        text_rect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))
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

    def draw_subcell(self, border, border_colour, box_colour, highlight_colour, x, y, w, h, action=None):
        # Draw bounding box of cell
        mod_x, mod_y, mod_w, mod_h = BORDERS[border]
        pygame.draw.rect(self.gameDisplay, border_colour, (x, y, w, h))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        inner_x, inner_y, inner_w, inner_h = x + mod_x, y + mod_y, w + mod_w, h + mod_h

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.gameDisplay, highlight_colour, (inner_x, inner_y, inner_w, inner_h))

            if click[0] == 1 and action is not None:
                action(inner_x, inner_y, inner_w, inner_h)
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
            {'border': 'bottom_right', 'x': x,               'y': y},
            {'border': 'u_shape',      'x': x + w * (1 / 3), 'y': y},
            {'border': 'bottom_left',  'x': x + w * (2 / 3), 'y': y},

            # middle row
            {'border': ']_shape',      'x': x,               'y': y + (h / 3)},
            {'border': 'o_shape',      'x': x + w * (1 / 3), 'y': y + (h / 3)},
            {'border': '[_shape',      'x': x + w * (2 / 3), 'y': y + (h / 3)},

            # bottom row
            {'border': 'top_right',    'x': x,               'y': y + h * (2 / 3)},
            {'border': 'n_shape',      'x': x + w * (1 / 3), 'y': y + h * (2 / 3)},
            {'border': 'top_left',     'x': x + w * (2 / 3), 'y': y + h * (2 / 3)},
        ]

        for position in positions:
            self.draw_subcell(**position, border_colour=border_colour, box_colour=box_colour, w=cell_width_,
                              h=cell_height_, highlight_colour=highlight_colour, action=self.subcell_clicked)

    def draw_main_grid(self):
        for parameters in MAIN_GRID_DRAW_PARAMETERS:
            self.draw_sub_grid(**parameters)

    def subcell_clicked(self, x, y, w, h):  # todo this should taken value from ultimate board
        self.clicked_cells.append((x, y, w, h, self.player))
        self.player *= -1

    def draw_clicked_cells(self):
        for x, y, w, h, player_ in self.clicked_cells:
            pygame.draw.rect(self.gameDisplay, self.colors[player_], (x, y, w, h))

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    self.quit_game()

            self.gameDisplay.fill(WHITE)
            self.draw_main_grid()
            self.draw_clicked_cells()
            pygame.display.update()
            self.clock.tick(60)


# TODO replace 3 with board size
if __name__ == '__main__':
    gui_ = GuiBoard()
    gui_.game_loop()
