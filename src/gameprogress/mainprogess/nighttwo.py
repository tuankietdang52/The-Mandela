import sys
import pygame as pg
import src.gameobj.otherobj as otherobj
import src.mapcontainer.market as mk
import src.entity.other.doctor as doc
import src.mapcontainer.town as mptown
import src.gameprogress.progressmanager as gp
import src.mapcontainer.housenormal as mphouse
import src.gameprogress.mainprogess.nightthree as n3

from src.hud.timehud import *
from src.hud.hudcomp import *


class NightTwo(gp.ProgressManager):
    def __init__(self, screen: pg.surface.Surface, game_objects: pg.sprite.Group = None):
        super().__init__(screen, game_objects)

        self.can_change_map = False
        self.can_press_key = True
        self.can_sleep = False
        self.manager.progress_status.is_get_potion = False

        self.spawn_manager.set_enemy_spawn_chance(20)
        self.doctor_corpse: doc.Doctor | None = None

        self.__init_time_hud()

    def re_setup(self):
        self.can_change_map = False
        self.can_press_key = True
        self.can_sleep = False
        self.is_occur_start_event = False
        self.manager.progress_status.is_get_potion = False

        self.doctor_corpse: doc.Doctor | None = None

        self.spawn_manager.set_enemy_spawn_chance(20)
        self.spawn_manager.reset_game_objects()
        self.__init_time_hud()

    def __init_time_hud(self):
        self.manager.set_night_and_time(2, (0, 0))
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
            tomorrow = n3.NightThree(self.screen, self.spawn_manager.game_objects)
            self.changing_night_when_sleep(tomorrow)

        self.three_am_event()

    def manage_progress(self):
        progress = self.get_progress_index()

        if progress == 0:
            self.show_title("Two")
            self.next()

        elif progress == 1:
            self.__check_news()

        elif progress == 2:
            self.__spawn_doctor_corpse()

        elif progress == 3:
            self.__spawn_potion()

    def __check_news(self):
        text = """Next, a famous doctor, Mr.Shiba, is missing, last seen in the Mandela town, near the road to Graveyard 
        |If someone sees him, please call the government
        """

        if not self.watching_tv(text, "../Assets/Sound/NarratorVoice/voice2.mp3"):
            return

        self.can_change_map = True
        self.next()

    def __spawn_doctor_corpse(self):
        sect = self.manager.gamemap.sect

        if type(sect) is not mptown.GraveyardEntrance:
            return

        point = sect.get_point("DoctorCorpse")
        position = pg.math.Vector2(point.x, point.y)

        self.doctor_corpse = doc.Doctor(position, mptown.GraveyardEntrance)
        self.spawn_manager.add_object(self.doctor_corpse)

        self.next()

    def __spawn_potion(self):
        sect = self.manager.gamemap.sect

        if type(sect) is not mptown.Apartment:
            return

        point = sect.get_point("Potion")
        position = pg.math.Vector2(point.x, point.y)

        potion = otherobj.Potion(position, mptown.Apartment)

        self.spawn_manager.add_object(potion)
        self.next()
