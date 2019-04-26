# tutorial from https://pythonprogramming.net/drawing-objects-pygame-tutorial/?completed=/displaying-text-pygame-screen/
from functools import partial

import pygame
import time
import random


# RED_RECT = 'ff5e58'
# RED_RECT_HIGHLIGHT = 'ffdbd4'
# BLUE_RECT = '3bd6ff'
# FORCED_BOARD = 'ffffcb'

pygame.init()

display_width = 600
display_height = 600
board_width = 480
board_height = 480

black = (0, 0, 0)
white = (255, 255, 255)
red = (250, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 250)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

block_color = (53, 115, 255)

PLAYER_X = 0
PLAYER_O = 1
colors = {
    PLAYER_X: red,
    PLAYER_O: blue,
}
player = PLAYER_X


# car_width = 73

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

# carImg = pygame.image.load('racecar.png')


# def things_dodged(count):
#     font = pygame.font.SysFont(None, 25)
#     text = font.render("Dodged: " + str(count), True, black)
#     gameDisplay.blit(text, (0, 0))
#
#
# def things(thingx, thingy, thingw, thingh, color):
#     pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
#
#
# def car(x, y):
#     gameDisplay.blit(carImg, (x, y))
#
#
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
#
#
# def message_display(text):
#     largeText = pygame.font.Font('freesansbold.ttf', 115)
#     TextSurf, TextRect = text_objects(text, largeText)
#     TextRect.center = ((display_width / 2), (display_height / 2))
#     gameDisplay.blit(TextSurf, TextRect)
#
#     pygame.display.update()
#
#
# def crash():
#     message_display('You Crashed')
#
#
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)

def quitgame():
    pygame.quit()
    quit()

border_thickness = 2
borders = {
    'top_left': (border_thickness, border_thickness, -border_thickness, -border_thickness),
    'top_right': (0, border_thickness, -border_thickness, -border_thickness),
    'bottom_left': (border_thickness, 0, -border_thickness, -border_thickness),
    'bottom_right': (0, 0, -border_thickness, -border_thickness),
    'u_shape': (border_thickness, 0, -2*border_thickness, -border_thickness),
    'n_shape': (border_thickness, border_thickness, -2*border_thickness, -border_thickness),
    'o_shape': (border_thickness, border_thickness, -2*border_thickness, -2*border_thickness),
    ']_shape': (0, border_thickness, -border_thickness, -2*border_thickness),
    '[_shape': (border_thickness, border_thickness, -border_thickness, -2*border_thickness),
}


def draw_subcell(border, border_colour, box_colour, highlight_colour, x, y, w, h, action=None):
    try:
        mod_x, mod_y, mod_w, mod_h = borders[border]
    except KeyError:
        raise
    else:
        pygame.draw.rect(gameDisplay, border_colour, (x, y, w, h))
        # pygame.draw.rect(gameDisplay, box_colour, (x+mod_x, y+mod_y, w+mod_w, h+mod_h))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(click)
        # print(mouse, x, y, w, h)
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(gameDisplay, highlight_colour, (x+mod_x, y+mod_y, w+mod_w, h+mod_h))

            if click[0] == 1 and action is not None:
                action(x+mod_x, y+mod_y, w+mod_w, h+mod_h)
        else:
            pygame.draw.rect(gameDisplay, box_colour, (x+mod_x, y+mod_y, w+mod_w, h+mod_h))


def draw_sub_grid(border, border_colour, box_colour, highlight_colour, x, y, w, h, action=None):
    try:
        mod_x, mod_y, mod_w, mod_h = borders[border]
    except KeyError:
        raise
    else:
        pygame.draw.rect(gameDisplay, border_colour, (x, y, w, h))
        # update position and size values for inner rectangle
        x, y = x+mod_x, y+mod_y
        w, h = w+mod_w, h+mod_h
        pygame.draw.rect(gameDisplay, box_colour, (x, y, w, h))

    cell_size = min(w, h)
    x, y = x + 2*sub_grid_padding, y + 2*sub_grid_padding
    w = h = cell_size - 4*sub_grid_padding
    cell_width = w / 3
    cell_height = h / 3

    draw_subcell('bottom_right', black, white, green, x, y, cell_width, cell_height, subcell_clicked)
    draw_subcell('u_shape', black, white, green, x + (w / 3), y, cell_width, cell_height,
                 subcell_clicked)
    draw_subcell('bottom_left', black, white, green, x + w * (2 / 3), y, cell_width, cell_height,
                 subcell_clicked)
    # middle row
    draw_subcell(']_shape', black, white, green, x, y + (h / 3), cell_width, cell_height,
                 subcell_clicked)
    draw_subcell('o_shape', black, white, green, x + w / 3, y + h / 3, cell_width, cell_height,
                 subcell_clicked)
    draw_subcell('[_shape', black, white, green, x + w * (2 / 3), y + h / 3, cell_width,
                 cell_height, subcell_clicked)
    # bottom row
    draw_subcell('top_right', black, white, green, x, y + h * (2 / 3), cell_width, cell_height,
                 subcell_clicked)
    draw_subcell('n_shape', black, white, green, x + w / 3, y + h * (2 / 3), cell_width,
                 cell_height, subcell_clicked)
    draw_subcell('top_left', black, white, green, x + w * (2 / 3), y + h * (2 / 3), cell_width,
                 cell_height, subcell_clicked)


def draw_main_grid(pos_x, pos_y):
    # top row
    draw_sub_grid('bottom_right', black, white, green, pos_x, pos_y, main_box_width, main_box_height, partial(print, ('hello',)))
    draw_sub_grid('u_shape', black, white, green, pos_x + board_width / 3, pos_y, main_box_width, main_box_height,
                  partial(print, ('hello',)))
    draw_sub_grid('bottom_left', black, white, green, pos_x + board_width * (2 / 3), pos_y, main_box_width, main_box_height,
                  partial(print, ('hello',)))
    # middle row
    draw_sub_grid(']_shape', black, white, green, pos_x, pos_y + board_height / 3, main_box_width, main_box_height,
                  partial(print, ('hello',)))
    draw_sub_grid('o_shape', black, white, green, pos_x + board_width / 3, pos_y + board_height / 3, main_box_width, main_box_height,
                  partial(print, ('hello',)))
    draw_sub_grid('[_shape', black, white, green, pos_x + board_width * (2 / 3), pos_y + board_height / 3, main_box_width,
                  main_box_height, partial(print, ('hello',)))
    # bottom row
    draw_sub_grid('top_right', black, white, green, pos_x, pos_y + board_height * (2 / 3), main_box_width, main_box_height,
                  partial(print, ('hello',)))
    draw_sub_grid('n_shape', black, white, green, pos_x + board_width / 3, pos_y + board_height * (2 / 3), main_box_width,
                  main_box_height, partial(print, ('hello',)))
    draw_sub_grid('top_left', black, white, green, pos_x + board_width * (2 / 3), pos_y + board_height * (2 / 3), main_box_width,
                  main_box_height, partial(print, ('hello',)))


def subcell_clicked(x, y, w, h):
    global player
    clicked_cells.append((x, y, w, h, player))
    player ^= 1


def draw_clicked_cells():
    for x, y, w, h, pl in clicked_cells:
        pygame.draw.rect(gameDisplay, colors[pl], (x, y, w, h))


clicked_cells = []
sub_grid_padding = 11
main_box_width = board_width / 3
main_box_height = board_height / 3
cell_width = main_box_width / 3
cell_height = main_box_height / 3
offset_x, offset_y = (display_width - board_width)/2, (display_height - board_height)/2

while True:
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            quitgame()

    gameDisplay.fill(white)
    draw_main_grid(offset_x, offset_y)
    draw_clicked_cells()
    pygame.display.update()
    clock.tick(60)

