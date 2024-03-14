import sys

import pygame
import pytmx

from Entity.PlayerContainer import Player
from MapContainer import Map
from MapContainer import HouseNormal

# Attribute for game #

FPS = 60
WIDTH = 700
HEIGHT = 700

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

player = Player.init(1000)
gamemap = HouseNormal(screen)


# Running Game #

def running_game():
    gameover = False

    while not gameover:
        gamemap.update_map()

        __event_action()
        __pressing_key()

        pygame.display.update()

        clock.tick(FPS)


def __event_action():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def __pressing_key():
    keys = pygame.key.get_pressed()

    player.moving(keys)


if __name__ == "__main__":
    running_game()
