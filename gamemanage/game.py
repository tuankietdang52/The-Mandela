import sys
import pygame

import mapcontainer.map
from pjenum import EState
from view.playerview import PlayerView
from mapcontainer import *
from gamepart import *


class Game:
    music_path = "Assets/Music/"

    game_part_index = 0

    FPS = 120
    WIDTH = 800
    HEIGHT = 800

    clock = pygame.time.Clock()
    dt = 0

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    screen.fill((0, 0, 0))

    # Music Background init #
    pygame.mixer.init()

    def __init__(self):
        self.gamemap = HouseNormal(self.screen)
        self.player = PlayerView.init(self.screen, self.gamemap, 1000)
        self.gamepart = Start(self.screen, self.gamemap)

        Manager.entities.add(self.player)
        Manager.gamemap = self.gamemap

    # def setup(self):
    #     gamemap = self.gamemap
    #     player = self.player
    #
    #     gamemap.sect.create()
    #
    #     try:
    #         start_point = gamemap.sect.get_spawn_point()
    #     except AttributeError:
    #         start_point = gamemap.sect.get_start_point()
    #
    #     start_point = start_point[0] - 100, start_point[1]
    #
    #     player.set_position(start_point)
    #
    #     Manager.update_UI()

    @staticmethod
    def get_time() -> int:
        return Game.dt

    def change_map(self, gamemap: mapcontainer.map.Map):
        self.gamemap = gamemap

    def running_game(self):
        pygame.time.wait(1000)

        gameover = False
        clock = self.clock

        while not gameover:
            if self.gamepart.is_changing_part:
                self.changing_part(FirstPart(self.screen, self.gamemap))
                self.gamepart.is_changing_part = False

            self.gamepart.event_action()
            self.gamepart.pressing_key()

            self.gamepart.update()

            pygame.display.update()

            dt = clock.tick(self.FPS)

    def changing_part(self, gamepart):
        self.gamepart = gamepart


class Manager:
    entities = pygame.sprite.Group()
    gamemap = None

    @classmethod
    def update_UI(cls):
        cls.gamemap.sect.redraw()
        cls.entities.update()

    @classmethod
    def update_UI_ip(cls):
        cls.gamemap.sect.redraw()
        cls.entities.update()

        pygame.display.update()
