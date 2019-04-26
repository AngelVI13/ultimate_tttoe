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

display_width = 480
display_height = 480

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

block_color = (53, 115, 255)

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


def make_cell(border, border_colour, box_colour, highlight_colour, x, y, w, h, action=None):
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
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(gameDisplay, highlight_colour, (x+mod_x, y+mod_y, w+mod_w, h+mod_h))

            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(gameDisplay, box_colour, (x+mod_x, y+mod_y, w+mod_w, h+mod_h))


while True:
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            quitgame()

    main_box_width = display_width / 3
    main_box_height = display_height / 3
    gameDisplay.fill(white)
    # top row
    make_cell('bottom_right', black, white, green, 0, 0, main_box_width, main_box_height, partial(print, ('hello',)))
    make_cell('u_shape', black, white, green, display_width/3, 0, main_box_width, main_box_height, partial(print, ('hello',)))
    make_cell('bottom_left', black, white, green, display_width*(2/3), 0, main_box_width, main_box_height, partial(print, ('hello',)))
    # middle row
    make_cell(']_shape', black, white, green, 0, display_height/3, main_box_width, main_box_height, partial(print, ('hello',)))
    make_cell('o_shape', black, white, green, display_width/3, display_height/3, main_box_width, main_box_height, partial(print, ('hello',)))
    make_cell('[_shape', black, white, green, display_width*(2/3), display_height/3, main_box_width, main_box_height, partial(print, ('hello',)))
    # bottom row
    make_cell('top_right', black, white, green, 0, display_height * (2/3), main_box_width, main_box_height, partial(print, ('hello',)))
    make_cell('n_shape', black, white, green, display_width/3, display_height * (2/3), main_box_width, main_box_height, partial(print, ('hello',)))
    make_cell('top_left', black, white, green, display_width*(2/3), display_height * (2/3), main_box_width, main_box_height, partial(print, ('hello',)))

    pygame.display.update()
    clock.tick(15)

