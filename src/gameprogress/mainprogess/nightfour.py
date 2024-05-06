import sys
import pygame as pg
import src.mapcontainer.town as mptown
import src.gameobj.otherobj as otherobj
import src.gameprogress.progressmanager as gp
import src.entity.other.doctor as doc
import src.mapcontainer.market as mk
import src.mapcontainer.housenormal as mphouse

from src.hud.timehud import *
from src.hud.hudcomp import *


class NightFour(gp.ProgressManager):
    def __init__(self, screen: pg.surface.Surface, game_objects: pg.sprite.Group = None):
        super().__init__(screen, game_objects)

        self.can_change_map = True
        self.can_press_key = True
        self.can_sleep = False
        self.gas_fill = set()
        self.manager.gas_amount = 0

        self.__init_time_hud()
        self.spawn_manager.set_enemy_spawn_chance(50)

    def re_setup(self):
        self.can_change_map = True
        self.can_press_key = True
        self.can_sleep = False

        self.manager.is_get_gas = False
        self.manager.gas_amount = 0

        self.spawn_manager.set_enemy_spawn_chance(50)
        self.gas_fill = set()

        self.spawn_manager.set_game_objects(self.game_objects_backup)

    def __init_time_hud(self):
        self.manager.set_night_and_time(3, (0, 0))
        self.time_hud = TimeHUD(self.manager.hud_groups)

    def event_action(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if not self.can_press_key:
                    return

    def update(self):
        super().update()

        if not self.spawn_manager.is_trigger_spawn:
            self.spawn_manager.spawn_alternate()

        if self.is_sleep():
            pass
            # tomorrow = nt.NightTwo(self.screen, self.spawn_manager.game_object)
            # self.changing_night_when_sleep(tomorrow)

        self.three_am_event()

    def manage_progress(self):
        progress = self.get_progress_index()
        if progress == 0:
            self.show_title("Four")
            self.next()

        elif progress == 1:
            self.__check_news()

        elif progress == 2:
            self.__spawn_gas_and_car()

        elif progress == 3:
            if self.manager.gas_amount < 100:
                self.__filling_gas()
            else:
                self.next()

    def __check_news(self):
        text = """Today, we have an accident at Park in the Mandela town. According to report, a drunk man driving a car 
        and crashed into a wall in Park. 
        |Fortunately, no one in the Park at that time so there is no casualties. The police will come up soon
        """

        if not self.watching_tv(text, "../Assets/Sound/NarratorVoice/voice3.mp3"):
            return

        self.next()

    def __spawn_gas_and_car(self):
        sect = self.manager.gamemap.sect

        if type(sect) is not mptown.Park2:
            return

        self.__spawn_broken_car()
        self.__spawn_gas_can()
        self.next()

    def __spawn_broken_car(self):
        sect = self.manager.gamemap.sect

        point = sect.get_point("Broken Car")
        position = pg.math.Vector2(point.x, point.y)

        broken_car = otherobj.BrokenCar(position, mptown.Park2)
        self.spawn_manager.add_object(broken_car)

    def __spawn_gas_can(self):
        sect = self.manager.gamemap.sect

        point = sect.get_point("Gas")
        position = pg.math.Vector2(point.x, point.y)

        gas = otherobj.Gas(position, mptown.Park2)
        self.spawn_manager.add_object(gas)

    def __filling_gas(self):
        sect = self.manager.gamemap.sect

        if not self.manager.is_get_gas:
            return

        if type(sect) is not mptown.Park1 and type(sect) is not mptown.RoadToApartment:
            return

        if type(sect) in self.gas_fill:
            return

        self.gas_fill.add(type(sect))

        point = sect.get_point("Fill Gas")
        position = pg.math.Vector2(point.x, point.y)
        fill_gas = otherobj.GasFill(position, type(sect))

        self.spawn_manager.add_object(fill_gas)
