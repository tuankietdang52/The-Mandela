import sys

import pygame

import Enum.EState
from Entity.PlayerContainer.Player import Player


FPS = 60
Width = 700
Height = 700
clock = pygame.time.Clock()

player = Player.init(1000)
player.set_state(Enum.EState.EState.DEAD)


def running_game():
    pygame.init()

    gameover = False
    pygame.display.set_mode((Width, Height))

    while not gameover:
        __event_action()
        __pressing_key()

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
