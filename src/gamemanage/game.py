import pygame as pg

import src.gamepart.housemap.beginning as bg
import src.gamepart.part as pt

import src.view.player.playerview as pv
import src.mapcontainer.map as mp
import src.mapcontainer.housenormal as hsmp


class Game:
    music_path = "../Assets/Music/"

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
        self.setup_manager()

    def setup_manager(self):
        Manager.screen = self.screen
        Manager.gamemap = hsmp.HouseNormal(self.screen)
        Manager.player = pv.PlayerView.init(self.screen, Manager.gamemap, 1000)
        Manager.gamepart = bg.BeginStory(self.screen)

        self.test()

    def test(self):
        """test element"""
        Manager.gamemap.change_sect("OutDoor")
        Manager.gamepart.set_progess_index(3)

        self.setup()

    def setup(self):
        """For test"""
        gamemap = Manager.gamemap
        player = Manager.player

        gamemap.sect.create()

        try:
            start_point = gamemap.sect.get_spawn_point()
        except AttributeError:
            start_point = gamemap.sect.get_start_point()

        start_point = start_point[0] - 100, start_point[1]

        player.set_position(start_point)

        Manager.update_UI()

    @staticmethod
    def ticking_time():
        Game.dt = Game.clock.tick(Game.FPS) / 1000

    @staticmethod
    def get_time() -> int:
        return Game.dt

    def running_game(self):
        pg.time.wait(1000)

        gameover = False

        while not gameover:
            # if self.gamepart.is_changing_part:
            #     self.changing_part(self.gamepart.nextpart)

            Manager.gamepart.event_action()
            Manager.gamepart.pressing_key()

            Manager.gamepart.update()

            Manager.update_enemy()

            pg.display.flip()

            Game.ticking_time()


class Manager:
    gamepart = None
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
    def clear_entities(cls):
        cls.appear_entities.empty()

    @classmethod
    def update_UI(cls):
        if cls.gamemap is None:
            cls.screen.fill((0, 0, 0))
            return

        cls.gamemap.sect.redraw()
        cls.appear_entities.draw(cls.screen)
        cls.player.update()

    @classmethod
    def update_UI_ip(cls):
        if cls.gamemap is None:
            cls.screen.fill((0, 0, 0))
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

    @staticmethod
    def play_theme(path: str):
        pg.mixer.music.unload()
        pg.mixer.music.load(path)

        pg.mixer.music.play(-1)

    @classmethod
    def get_screen(cls) -> pg.surface.Surface:
        return cls.screen

    @classmethod
    def set_part(cls, gamepart: pt.Part):
        cls.gamepart = gamepart

    @classmethod
    def set_map(cls, gamemap: mp.Map):
        cls.clear_entities()
        cls.gamemap = gamemap

    @staticmethod
    def wait(time_wait: int):
        """
        :param time_wait: second
        """

        time = float(0)
        Manager.gamepart.can_press_key = False

        Game.ticking_time()
        Game.ticking_time()

        while time < float(time_wait):
            Manager.gamepart.event_action()
            time += Game.get_time()

            Game.ticking_time()

        Manager.gamepart.can_press_key = True
