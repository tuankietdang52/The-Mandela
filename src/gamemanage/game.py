import pygame as pg

import src.gamepart.part as gp
import src.view.player.playerview as pv
import src.mapcontainer.map as mp

import src.mapcontainer.housenormal as mphouse
import src.mapcontainer.town as mptown
import src.gamepart.townmap.themandela as tm
import src.gamepart.housemap.beginning as bg
import src.gamepart.housemap.startmenu as sm


class Game:
    music_path = "../Assets/Music/"
    icon_path = "../Assets/HUD/icon.jpg"

    FPS = 120
    WIDTH = 800
    HEIGHT = 800

    IS_TEST = True

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
        self.setup()
        if not self.IS_TEST:
            self.setup_manager()
        else:
            self.test()

    def setup(self):
        icon = pg.image.load(self.icon_path).convert()
        pg.display.set_icon(icon)
        pg.display.set_caption("Nightmare")

    def setup_manager(self):
        Manager.screen = self.screen
        Manager.gamemap = mphouse.HouseNormal(self.screen)
        Manager.player = pv.PlayerView.init(self.screen, 1000)
        Manager.gamepart = sm.StartMenu(self.screen)


    def test(self):
        """test element"""
        Manager.screen = self.screen
        Manager.gamemap = mphouse.HouseNormal(self.screen)
        Manager.player = pv.PlayerView.init(self.screen, 1000)
        Manager.gamepart = tm.TheMandela(self.screen)

        Manager.gamemap.change_sect("Corridor")
        Manager.gamepart.set_progess_index(3)

        self.setup_test()

    def setup_test(self):
        """For test"""
        gamemap = Manager.gamemap
        player = Manager.player

        gamemap.sect.create()

        start_point = gamemap.sect.get_start_point()

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
            Manager.gamepart.event_action()
            Manager.gamepart.pressing_key()

            if not self.IS_TEST:
                Manager.gamepart.update()
                Manager.gamepart.handle_change_sect()

            else:
                Manager.gamepart.update()
                Manager.gamepart.handle_change_sect()

            Manager.update_enemy()

            pg.display.flip()

            Game.ticking_time()


class Manager:
    screen = None
    gamepart: gp.Part | None = None
    gamemap: mp.Map | None = None
    player: pv.PlayerView = None
    appear_entities = pg.sprite.Group()

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
        cls.screen.fill((0, 0, 0))
        if cls.gamemap is None:
            return

        cls.gamemap.sect.redraw()
        cls.appear_entities.draw(cls.screen)
        cls.player.update()
        cls.gamemap.sect.redraw_overlap_tile()

    @classmethod
    def update_UI_ip(cls):
        cls.screen.fill((0, 0, 0))
        if cls.gamemap is None:
            return

        cls.gamemap.sect.redraw()
        cls.appear_entities.draw(cls.screen)
        cls.player.update()
        cls.gamemap.sect.redraw_overlap_tile()

        pg.display.update()

    @classmethod
    def update_enemy(cls):
        if len(Manager.appear_entities) == 0:
            return

        cls.appear_entities.update()

    @staticmethod
    def play_theme(path: str, volume: float = None):
        """
        :param path:
        :param volume: between 0.0 -> 1.0:
        """
        pg.mixer.music.unload()
        pg.mixer.music.load(path)

        if volume is not None:
            pg.mixer.music.set_volume(volume)

        pg.mixer.music.play(-1)

    @classmethod
    def get_screen(cls) -> pg.surface.Surface:
        return cls.screen

    @classmethod
    def set_part(cls, gamepart: gp.Part):
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
