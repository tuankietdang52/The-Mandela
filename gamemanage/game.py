import sys
import os

import pygame

from view import PlayerView
from mapcontainer import HouseNormal


class Game:
    FPS = 120
    WIDTH = 700
    HEIGHT = 700

    clock = pygame.time.Clock()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    tilegroup = pygame.sprite.Group()

    gamemap = HouseNormal(screen, tilegroup)
    player = PlayerView.init(screen, 1000, gamemap)

    def __init__(self):
        pass

    def change_map(self, gamemap):
        """:param Map gamemap: """
        self.gamemap = gamemap

    def setup(self):
        gamemap = self.gamemap
        player = self.player

        gamemap.create_map()
        player.update_player()

    def running_game(self):
        gameover = False
        clock = self.clock

        self.setup()

        while not gameover:
            self.__event_action()
            self.__pressing_key()

            pygame.display.flip()

            clock.tick(self.FPS)

    def __event_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def __pressing_key(self):
        keys = pygame.key.get_pressed()

        self.player.moving(keys)
