import pygame
import random
from gui.constants import *


class Animation:
    __slots__ = ['img', 'x', 'y', 'x_increment', 'y_increment']

    def __init__(self, img, x, y, x_increment, y_increment):
        self.img = img
        self.x = x
        self.y = y
        self.x_increment = x_increment
        self.y_increment = y_increment


class Background:
    num_animations = 10

    def __init__(self, game_display):
        self.game_display = game_display
        x_coords = (random.randrange(0, DISPLAY_WIDTH) for _ in range(self.num_animations))
        y_coords = (random.randrange(0, DISPLAY_HEIGHT) for _ in range(self.num_animations))
        increment_padding = [0] * (self.num_animations//2)
        x_increment = [random.randrange(2, 5) for _ in range(self.num_animations // 2)]
        x_increment.extend(increment_padding)
        y_increment = increment_padding[:]
        y_increment.extend([random.randrange(2, 5) for _ in range(self.num_animations // 2)])
        self.animations = []
        for x, y, increment_x, increment_y in zip(x_coords, y_coords, x_increment, y_increment):
            hashtag_img = pygame.image.load('../media/hashtag_1.png')
            self.animations.append(Animation(img=hashtag_img, x=x, y=y,
                                             x_increment=increment_x, y_increment=increment_y))

    def update(self):
        for idx in range(len(self.animations)):
            animation = self.animations[idx]
            self.game_display.blit(animation.img, (animation.x, animation.y))

            self.animations[idx].x += self.animations[idx].x_increment
            if self.animations[idx].x > DISPLAY_WIDTH:
                self.animations[idx].x = 0

            self.animations[idx].y += self.animations[idx].y_increment
            if self.animations[idx].y > DISPLAY_HEIGHT:
                self.animations[idx].y = 0
