from __future__ import annotations

import pygame as pg

import src.gamepart.part as gp
import src.view.player.playerview as pv
import src.mapcontainer.map as mp
import src.mapcontainer.housenormal as mphouse
import src.mapcontainer.town as mptown
import src.gamepart.townmap.themandela as tm
import src.gamepart.housemap.beginning as bg
import src.gamepart.housemap.startmenu as sm


class Manager:
    """Please call get_instance() before you use any attribute or not static function in this class"""

    __instance = None
    screen = None
    gamepart: gp.Part | None = None
    gamemap: mp.Map | None = None
    player: pv.PlayerView = None
    appear_entities = pg.sprite.Group()

    def __init__(self):
        """Call init() instead"""
        raise RuntimeError("Call init() to init instance")

    @classmethod
    def get_instance(cls) -> Manager:
        if cls.__instance is None:
            raise RuntimeError("Must init instance first")

        return cls.__instance

    @classmethod
    def init(cls, screen: pg.surface.Surface):
        if cls.__instance is not None:
            print("Manager is created before")
            return cls.__instance

        cls.__instance = cls.__new__(cls)

        cls.screen = screen

        return cls.__instance

    def setup(self,
              gamemap: mp.Map,
              player: pv.PlayerView,
              gamepart: gp.Part):
        self.gamemap = gamemap
        self.player = player
        self.gamepart = gamepart

    def unload_map(self):
        self.gamemap = None
        self.screen.fill((0, 0, 0))
        pg.display.update()

    def clear_entities(self):
        self.appear_entities.empty()

    def update_UI(self):
        self.screen.fill((0, 0, 0))
        if self.gamemap is None:
            return

        self.gamemap.sect.redraw()
        self.appear_entities.draw(self.screen)
        self.player.update()
        self.gamemap.sect.redraw_overlap_tile()

    def update_UI_ip(self):
        self.screen.fill((0, 0, 0))
        if self.gamemap is None:
            return

        self.gamemap.sect.redraw()
        self.appear_entities.draw(self.screen)
        self.player.update()
        self.gamemap.sect.redraw_overlap_tile()

        pg.display.update()

    def update_enemy(self):
        if len(Manager.appear_entities) == 0:
            return

        self.appear_entities.update()

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

    def set_part(self, gamepart: gp.Part):
        self.gamepart = gamepart

    def set_map(self, gamemap: mp.Map):
        """Warning: this function will change manager.gamemap address to parameter map"""
        self.clear_entities()
        self.gamemap = gamemap

    def wait(self, time_wait: int):
        """
        :param time_wait: second
        """

        time = float(0)
        self.gamepart.can_press_key = False

        Game.ticking_time()
        Game.ticking_time()

        while time < float(time_wait):
            self.gamepart.event_action()
            time += Game.get_time()

            Game.ticking_time()

        self.gamepart.can_press_key = True

    def set_appear_entity_opacity(self, alpha: int):
        for em in self.appear_entities:
            em.image.set_alpha(alpha)


class Game:
    music_path = "../Assets/Music/"
    icon_path = "../Assets/HUD/icon.jpg"

    FPS = 120
    WIDTH = 800
    HEIGHT = 800

    IS_TEST = False
    IS_FULLSCREEN = True

    game_part_index = 0
    clock = pg.time.Clock()
    dt = 0

    pg.init()

    if IS_FULLSCREEN:
        screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
    else:
        screen = pg.display.set_mode((WIDTH, HEIGHT))

    screen.fill((0, 0, 0))

    # Music Background init #
    pg.mixer.init()

    manager: Manager = None

    def __init__(self):
        self.manager = Manager.init(self.screen)
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
        gamemap = mphouse.HouseNormal(self.screen)
        player = pv.PlayerView(self.screen, 1000)
        gamepart = sm.StartMenu(self.screen)

        self.manager.setup(gamemap, player, gamepart)


    def test(self):
        """test element"""
        gamemap = mphouse.HouseNormal(self.screen)
        player = pv.PlayerView(self.screen, 1000)
        gamepart = bg.BeginStory(self.screen)

        self.manager.setup(gamemap, player, gamepart)

        self.manager.gamemap.change_sect("Corridor")
        self.manager.gamepart.set_progess_index(3)

        self.setup_test()

    def setup_test(self):
        """For test"""
        gamemap = self.manager.gamemap
        player = self.manager.player

        gamemap.sect.create()

        start_point = gamemap.sect.get_start_point()

        player.set_position(start_point)

        self.manager.update_UI()

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
            self.manager.gamepart.event_action()
            self.manager.gamepart.pressing_key()

            if not self.IS_TEST:
                self.manager.gamepart.update()
                self.manager.gamepart.handle_change_sect()

            else:
                self.manager.gamepart.update()
                self.manager.gamepart.handle_change_sect()

            self.manager.update_enemy()

            pg.display.flip()

            Game.ticking_time()
