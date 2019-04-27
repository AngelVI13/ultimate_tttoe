# tutorial from https://pythonprogramming.net/drawing-objects-pygame-tutorial/?completed=/displaying-text-pygame-screen/
import pygame
from gui.colors import *
from board.ultimate_board import *


class GuiBoard:
    display_width = 600
    display_height = 600
    board_width = 480
    board_height = 480
    colors = {
        PLAYER_X: RED,
        PLAYER_O: BLUE,
    }

    border_thickness = 2
    borders = {
        'top_left': (border_thickness, border_thickness, -border_thickness, -border_thickness),
        'top_right': (0, border_thickness, -border_thickness, -border_thickness),
        'bottom_left': (border_thickness, 0, -border_thickness, -border_thickness),
        'bottom_right': (0, 0, -border_thickness, -border_thickness),
        'u_shape': (border_thickness, 0, -2 * border_thickness, -border_thickness),
        'n_shape': (border_thickness, border_thickness, -2 * border_thickness, -border_thickness),
        'o_shape': (border_thickness, border_thickness, -2 * border_thickness, -2 * border_thickness),
        ']_shape': (0, border_thickness, -border_thickness, -2 * border_thickness),
        '[_shape': (border_thickness, border_thickness, -border_thickness, -2 * border_thickness),
    }

    clicked_cells = []
    sub_grid_padding = 11
    main_box_width = board_width / 3
    main_box_height = board_height / 3
    cell_width = main_box_width / 3
    cell_height = main_box_height / 3
    # offset for main grid from main window
    offset_x, offset_y = (display_width - board_width) / 2, (display_height - board_height) / 2

    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
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
        text_rect.center = ((self.display_width / 2), (self.display_height / 2))
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
        try:
            mod_x, mod_y, mod_w, mod_h = self.borders[border]
        except KeyError:
            raise
        else:
            pygame.draw.rect(self.gameDisplay, border_colour, (x, y, w, h))
            # pygame.draw.rect(self.gameDisplay, box_colour, (x+mod_x, y+mod_y, w+mod_w, h+mod_h))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            # print(click)
            # print(mouse, x, y, w, h)
            if x + w > mouse[0] > x and y + h > mouse[1] > y:
                pygame.draw.rect(self.gameDisplay, highlight_colour, (x + mod_x, y + mod_y, w + mod_w, h + mod_h))

                if click[0] == 1 and action is not None:
                    action(x + mod_x, y + mod_y, w + mod_w, h + mod_h)
            else:
                pygame.draw.rect(self.gameDisplay, box_colour, (x + mod_x, y + mod_y, w + mod_w, h + mod_h))

    def draw_sub_grid(self, border, border_colour, box_colour, highlight_colour, x, y, w, h):
        try:
            mod_x, mod_y, mod_w, mod_h = self.borders[border]
        except KeyError:
            raise
        else:
            pygame.draw.rect(self.gameDisplay, border_colour, (x, y, w, h))
            # update position and size values for inner rectangle
            x, y = x + mod_x, y + mod_y
            w, h = w + mod_w, h + mod_h
            pygame.draw.rect(self.gameDisplay, box_colour, (x, y, w, h))

        cell_size = min(w, h)
        x, y = x + 2 * self.sub_grid_padding, y + 2 * self.sub_grid_padding
        w = h = cell_size - 4 * self.sub_grid_padding
        cell_width_ = w / 3
        cell_height_ = h / 3

        self.draw_subcell('bottom_right', border_colour, box_colour, highlight_colour, x, y, cell_width_, cell_height_,
                          self.subcell_clicked)
        self.draw_subcell('u_shape', border_colour, box_colour, highlight_colour, x + (w / 3), y, cell_width_,
                          cell_height_,
                          self.subcell_clicked)
        self.draw_subcell('bottom_left', border_colour, box_colour, highlight_colour, x + w * (2 / 3), y, cell_width_,
                          cell_height_,
                          self.subcell_clicked)
        # middle row
        self.draw_subcell(']_shape', border_colour, box_colour, highlight_colour, x, y + (h / 3), cell_width_,
                          cell_height_,
                          self.subcell_clicked)
        self.draw_subcell('o_shape', border_colour, box_colour, highlight_colour, x + w / 3, y + h / 3, cell_width_,
                          cell_height_,
                          self.subcell_clicked)
        self.draw_subcell('[_shape', border_colour, box_colour, highlight_colour, x + w * (2 / 3), y + h / 3,
                          cell_width_,
                          cell_height_, self.subcell_clicked)
        # bottom row
        self.draw_subcell('top_right', border_colour, box_colour, highlight_colour, x, y + h * (2 / 3), cell_width_,
                          cell_height_,
                          self.subcell_clicked)
        self.draw_subcell('n_shape', border_colour, box_colour, highlight_colour, x + w / 3, y + h * (2 / 3),
                          cell_width_,
                          cell_height_, self.subcell_clicked)
        self.draw_subcell('top_left', border_colour, box_colour, highlight_colour, x + w * (2 / 3), y + h * (2 / 3),
                          cell_width_,
                          cell_height_, self.subcell_clicked)

    def draw_main_grid(self, pos_x, pos_y):
        # top row
        self.draw_sub_grid(border='bottom_right', border_colour=BLACK, box_colour=WHITE, highlight_colour=GREEN,
                           x=pos_x, y=pos_y, w=self.main_box_width, h=self.main_box_height)
        self.draw_sub_grid(border='u_shape', border_colour=BLACK, box_colour=WHITE, highlight_colour=GREEN,
                           x=pos_x + self.board_width / 3, y=pos_y, w=self.main_box_width, h=self.main_box_height)
        self.draw_sub_grid(border='bottom_left', border_colour=BLACK, box_colour=WHITE, highlight_colour=GREEN,
                           x=pos_x + self.board_width * (2 / 3), y=pos_y, w=self.main_box_width, h=self.main_box_height)
        # middle row
        self.draw_sub_grid(border=']_shape', border_colour=BLACK, box_colour=WHITE, highlight_colour=GREEN,
                           x=pos_x, y=pos_y + self.board_height / 3, w=self.main_box_width, h=self.main_box_height)
        self.draw_sub_grid(border='o_shape', border_colour=BLACK, box_colour=WHITE, highlight_colour=GREEN,
                           x=pos_x + self.board_width / 3, y=pos_y + self.board_height / 3, w=self.main_box_width,
                           h=self.main_box_height)
        self.draw_sub_grid(border='[_shape', border_colour=BLACK, box_colour=WHITE, highlight_colour=GREEN,
                           x=pos_x + self.board_width * (2 / 3), y=pos_y + self.board_height / 3, w=self.main_box_width,
                           h=self.main_box_height)
        # bottom row
        self.draw_sub_grid(border='top_right', border_colour=BLACK, box_colour=WHITE, highlight_colour=GREEN,
                           x=pos_x, y=pos_y + self.board_height * (2 / 3), w=self.main_box_width,
                           h=self.main_box_height)
        self.draw_sub_grid(border='n_shape', border_colour=BLACK, box_colour=WHITE, highlight_colour=GREEN,
                           x=pos_x + self.board_width / 3, y=pos_y + self.board_height * (2 / 3), w=self.main_box_width,
                           h=self.main_box_height)
        self.draw_sub_grid(border='top_left', border_colour=BLACK, box_colour=WHITE, highlight_colour=GREEN,
                           x=pos_x + self.board_width * (2 / 3), y=pos_y + self.board_height * (2 / 3),
                           w=self.main_box_width,
                           h=self.main_box_height)

    def subcell_clicked(self, x, y, w, h):  # todo this should take value from ultimate board
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
            self.draw_main_grid(self.offset_x, self.offset_y)
            self.draw_clicked_cells()
            pygame.display.update()
            self.clock.tick(60)


# TODO replace 3 with board size
if __name__ == '__main__':
    gui_ = GuiBoard()
    gui_.game_loop()
