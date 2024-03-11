import sys

import pygame
from pygame.locals import *

FPS = 60
Width = 700
Height = 700
clock = pygame.time.Clock()


def running_game():
    pygame.init()

    gameover = False
    pygame.display.set_mode((Width, Height))

    while not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True

        clock.tick(FPS)


if __name__ == "__main__":
    running_game()
