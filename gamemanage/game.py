import sys

import pygame

from view import PlayerView
from mapcontainer import HouseNormal
from mapcontainer import Map


class Game:
    FPS = 60
    WIDTH = 700
    HEIGHT = 700
    OFFSETX = 4.5
    OFFSETY = 4

    clock = pygame.time.Clock()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def __init__(self):
        self.player = PlayerView(self.screen, 1000)
        self.gamemap = HouseNormal(self.screen)

    def change_map(self, gamemap):
        """:param Map gamemap: """
        self.gamemap = gamemap

    def running_game(self):
        gamemap = self.gamemap
        player = self.player
        clock = self.clock

        gameover = False
        player.presenter.set_position(gamemap.startpoint.x * self.OFFSETX,
                                      gamemap.startpoint.y * self.OFFSETY)

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
