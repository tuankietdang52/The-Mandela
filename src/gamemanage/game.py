from __future__ import annotations

import pygame as pg

import src.hud.timehud
import src.gameprogress.progressmanager as gp
import src.entity.ally.player as pl
import src.mapcontainer.map as mp
import src.gameprogress.other.deadmenu as dm
import src.gameprogress.other.pause as ps

from src.eventhandle import *
from src.pjenum import *

# TEST IMPORT

import src.mapcontainer.housenormal as mphouse
import src.mapcontainer.town as mptown
import src.gameprogress.other.startmenu as sm
import src.gameprogress.mainprogess.nightone as n1
import src.gameprogress.mainprogess.nighttwo as n2
import src.gameprogress.mainprogess.nightthree as n3
import src.gameprogress.mainprogess.nightfour as n4
import src.gameprogress.begin.themandela as tm
import src.gameprogress.begin.beginning as bg


class ProgressStatus:
    def __init__(self):
        self.is_get_potion = False
        self.is_get_gas = False
        self.gas_amount = 0
        self.is_get_shovel = False
        self.is_call_help = False
        self.can_get_in_car = False
        self.get_in_car = False

        self.can_pause = True

    def reset(self):
        self.is_get_potion = False
        self.is_get_gas = False
        self.gas_amount = 0
        self.is_get_shovel = False
        self.is_call_help = False
        self.can_get_in_car = False
        self.get_in_car = False

        self.can_pause = True


class Manager:
    """Please call get_instance() before you use any attribute or not static function in this class"""

    __instance = None
    screen = None
    gameprogress: gp.ProgressManager | None = None
    gamemap: mp.Map | None = None
    player: pl.Player = None

    entities = pg.sprite.Group()
    appear_enemies = pg.sprite.Group()
    appear_object = pg.sprite.Group()
    hud_groups = pg.sprite.Group()

    progress_status = ProgressStatus()

    game_time = 0, 0
    game_time_second = 0
    game_night = 1

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
        cls.on_entities_destroy = EventHandle()

        return cls.__instance

    def unload_map(self):
        self.gamemap = None
        self.screen.fill((0, 0, 0))
        pg.display.update()

    def clear_entities(self):
        self.on_entities_destroy.invoke()

    def update_UI(self):
        self.screen.fill((0, 0, 0))
        if self.gamemap is None:
            return

        self.gamemap.sect.redraw()
        self.appear_object.draw(self.screen)
        self.entities.draw(self.screen)
        self.gamemap.sect.redraw_overlap_tile()
        self.hud_groups.draw(self.screen)

    def update_UI_ip(self):
        self.update_UI()
        pg.display.update()

    def update(self):
        self.gameprogress.update()
        self.update_entities()
        self.update_object()
        self.update_time()
        self.update_hud()
        self.update_UI_ip()

    def update_time(self):
        self.game_time_second += Game.get_time()

        self.game_time = self.game_time[0], round(self.game_time_second)

        if self.game_time[0] == 2:
            self.gameprogress.can_sleep = True

        if self.game_time[0] == 24:
            self.game_time = 0, 0

        if self.game_time[1] == 60:
            self.game_time = self.game_time[0] + 1, 0
            self.game_time_second = 0

    def set_night_and_time(self, night: int, time: tuple[int, int]):
        self.game_night = night
        self.game_time = time
        self.game_time_second = time[1]

    def update_object(self):
        self.appear_object.update()

    def update_entities(self):
        if self.progress_status.get_in_car:
            return

        self.entities.update()

        if len(self.appear_enemies) != 0:
            self.player.decrease_sanity_amount(0.008)

    def update_hud(self):
        self.hud_groups.update()

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

    def set_game_progress(self, gameprogress: gp.ProgressManager):
        self.gameprogress.kill_time_hud()
        self.gameprogress = gameprogress

    def set_map(self, gamemap: mp.Map):
        """Warning: this function will change manager.gamemap address to parameter map"""
        self.clear_entities()
        self.gamemap = gamemap

    def wait(self, time_wait: float, is_enable_input: bool = True):
        """
        :param time_wait: second
        :param is_enable_input: is enable input back for user
        """

        time = float(0)
        self.gameprogress.can_press_key = False

        Game.ticking_time()
        Game.ticking_time()

        while time < time_wait:
            self.gameprogress.event_action()
            time += Game.get_time()

            Game.ticking_time()

        if is_enable_input:
            self.gameprogress.can_press_key = True

    def set_hud_opacity(self, alpha):
        for item in self.hud_groups:
            item.image.set_alpha(alpha)

    def set_appear_enemies_opacity(self, alpha: int):
        for em in self.appear_enemies:
            em.image.set_alpha(alpha)

    def set_appear_item_opacity(self, alpha: int):
        for item in self.appear_object:
            item.image.set_alpha(alpha)

    def reset_time(self):
        self.game_time = 0, 0
        self.game_time_second = 0


class Game:
    ICON_PATH = "../Assets/HUD/icon.jpg"

    FPS = 120
    WIDTH = 800
    HEIGHT = 800

    IS_TEST = False
    IS_FULLSCREEN = True

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
        self.pause = ps.Pause(self.screen)

        self.setup()
        if not self.IS_TEST:
            self.setup_manager()
        else:
            self.test()

    def setup(self):
        icon = pg.image.load(self.ICON_PATH).convert()
        pg.display.set_icon(icon)
        pg.display.set_caption("The Mandela")

    def setup_manager(self):
        self.manager.player = pl.Player(self.screen, self.manager.entities)
        self.manager.gameprogress = sm.StartMenu(self.screen)

    def test(self):
        """test element"""
        self.manager.gamemap = mptown.Town(self.screen)
        self.manager.player = pl.Player(self.screen, self.manager.entities)
        self.manager.gameprogress = n1.NightOne(self.screen)

        self.manager.player.init_hud(self.manager.hud_groups)
        # self.manager.gameprogress.time_hud = src.hud.timehud.TimeHUD(self.manager.hud_groups)

        self.manager.gamemap.change_sect("OutsideMarket")
        self.manager.gameprogress.set_progress_index(6)

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
    def get_time() -> float:
        return Game.dt

    def __is_pause_game(self):
        keys = pg.key.get_pressed()

        if self.manager.player.get_state() == EState.DEAD:
            return False

        if not self.manager.progress_status.can_pause:
            return False

        if keys[pg.K_ESCAPE] and self.pause.is_resume:
            return True

        return False

    def __pausing_game(self):
        self.pause.show()
        self.is_pausing = True

    def __pause_update(self):
        self.pause.update()
        self.manager.update_UI_ip()

    def running_game(self):
        self.manager.wait(1)

        game_running = True
        game_over = False

        player = self.manager.player

        while game_running:
            if self.__is_pause_game():
                self.__pausing_game()

            if not self.pause.is_resume:
                self.__pause_update()
                continue

            if player.get_state() == EState.DEAD and not game_over:
                self.__to_dead_menu()
                game_over = True
            elif player.get_state() != EState.DEAD:
                game_over = False

            self.manager.update()

            Game.ticking_time()

    def __to_dead_menu(self):
        current_progress = self.manager.gameprogress
        self.manager.set_game_progress(dm.DeadMenu(self.screen, current_progress))
