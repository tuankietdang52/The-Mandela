import pygame as pg

import gamepart.housemap.beginning as bg
import gamepart.housemap.startmenu as sm

from view.player.playerview import PlayerView
from mapcontainer import *


class Game:
    music_path = "Assets/Music/"

    FPS = 120
    WIDTH = 800
    HEIGHT = 800

    game_part_index = 0
    clock = pg.time.Clock()
    dt = 0

    pg.init()

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)

    screen.fill((0, 0, 0))

    # Music Background init #
    pg.mixer.init()

    def __init__(self):
        self.gamemap = HouseNormal(self.screen)
        self.player = PlayerView.init(self.screen, self.gamemap, 1000)
        self.gamepart = sm.StartMenu(self.screen, self.gamemap)

        self.setup_manager()

    def setup_manager(self):
        Manager.player = self.player
        Manager.gamemap = self.gamemap
        Manager.screen = self.screen

    # def __init__(self):
    #     self.gamemap = HouseNormal(self.screen)
    #
    #     self.player = PlayerView.init(self.screen, self.gamemap, 1000)
    #
    #     self.gamepart = bg.BeginStory(self.screen, self.gamemap)
    #
    #     self.test()
    #
    # def test(self):
    #     """test element"""
    #     self.gamemap.change_sect("OutDoor")
    #     self.gamepart.set_progess_index(3)
    #
    #     self.setup_manager()
    #     self.setup()
    #
    # def setup(self):
    #     """For test"""
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

    def change_map(self, gamemap: mp.Map):
        self.gamemap = gamemap

    def running_game(self):
        pg.time.wait(1000)

        gameover = False
        clock = self.clock

        while not gameover:
            if self.gamepart.is_changing_part:
                self.changing_part(self.gamepart.nextpart)
                self.gamepart.is_changing_part = False

            self.gamepart.event_action()
            self.gamepart.pressing_key()

            self.gamepart.update()

            Manager.update_enemy()

            pg.display.flip()

            dt = clock.tick(self.FPS)

    def changing_part(self, gamePart):
        self.gamepart = gamePart


class Manager:
    gamemap = None
    player = None
    appear_entities = pg.sprite.Group()
    screen = None

    @classmethod
    def unload_map(cls):
        cls.gamemap = None
        cls.screen.fill((0, 0, 0))
        pg.display.update()

    @classmethod
    def update_UI(cls):
        if cls.gamemap is None:
            return

        cls.gamemap.sect.redraw()
        cls.appear_entities.draw(cls.screen)
        cls.player.update()

    @classmethod
    def update_UI_ip(cls):
        if cls.gamemap is None:
            return

        cls.gamemap.sect.redraw()
        cls.appear_entities.draw(cls.screen)
        cls.player.update()

        pg.display.update()

    @classmethod
    def update_enemy(cls):
        if len(Manager.appear_entities) == 0:
            return

        cls.appear_entities.update()
        cls.update_UI_ip()

    @staticmethod
    def play_theme(path: str):
        pg.mixer.music.unload()
        pg.mixer.music.load(path)

        pg.mixer.music.play(-1)

    @classmethod
    def get_screen(cls) -> pg.surface.Surface:
        return cls.screen
