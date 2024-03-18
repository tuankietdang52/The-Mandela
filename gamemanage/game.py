import sys
import os

import pygame

from view import PlayerView
from mapcontainer import HouseNormal


class Game:
    FPS = 120
    WIDTH = 700
    HEIGHT = 700

    centerx = WIDTH / 2
    centery = HEIGHT / 2 + 10

    clock = pygame.time.Clock()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    player = PlayerView.init(screen, 1000, centerx, centery)
    gamemap = HouseNormal(screen)

    def __init__(self):
        pass

    def change_map(self, gamemap):
        """:param Map gamemap: """
        self.gamemap = gamemap

    def setup(self):
        gamemap = self.gamemap
        player = self.player

        startpoint = gamemap.get_start_point()

        player.presenter.set_position(startpoint[0], startpoint[1])

        gamemap.update_map()
        player.update_player()

    def running_game(self):
        gameover = False

        gamemap = self.gamemap
        player = self.player
        clock = self.clock

        count = 0

        self.setup()

        while not gameover:
            gamemap.update_map()
            player.update_player()

            self.__event_action()
            self.__pressing_key()

            pygame.display.update()

            clock.tick(self.FPS)

    def __event_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def __pressing_key(self):
        keys = pygame.key.get_pressed()

        self.player.moving(keys)
