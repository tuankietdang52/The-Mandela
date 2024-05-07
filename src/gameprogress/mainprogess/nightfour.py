import sys
import pygame as pg
import src.entity.ally.cop as cp
import src.mapcontainer.market as mk
import src.mapcontainer.town as mptown
import src.gameobj.otherobj as otherobj
import src.gameprogress.progressmanager as gp
import src.mapcontainer.housenormal as mphouse
import src.gameprogress.other.badending as bd
import src.gameprogress.other.goodending as gd
import src.entity.thealternate.doppelganger as dp

from src.hud.timehud import *
from src.hud.hudcomp import *


class NightFour(gp.ProgressManager):
    def __init__(self, screen: pg.surface.Surface, game_objects: pg.sprite.Group = None):
        super().__init__(screen, game_objects)

        self.can_change_map = False
        self.can_press_key = True
        self.can_sleep = False
        self.gas_fill = set()

        self.manager.progress_status.is_get_gas = False
        self.manager.progress_status.gas_amount = 0

        self.manager.progress_status.is_call_help = True
        self.manager.progress_status.is_get_potion = True

        self.is_check = False
        self.__is_dizzy = False
        self.__is_spawn_gas_can = False

        self.__alpha = 255
        self.__time = 0
        self.__end_time = 10

        self.__init_time_hud()
        self.spawn_manager.set_enemy_spawn_chance(70)

    def re_setup(self):
        self.can_change_map = False
        self.can_press_key = True
        self.can_sleep = False
        self.can_change_sect = True
        self.is_occur_start_event = False

        self.manager.progress_status.is_get_gas = False
        self.manager.progress_status.gas_amount = 0

        self.__time = 0

        self.is_check = False
        self.__is_dizzy = False
        self.__is_spawn_gas_can = False

        self.spawn_manager.set_enemy_spawn_chance(50)
        self.gas_fill = set()
        self.spawn_manager.special_entities = set()

        self.__init_time_hud()
        self.spawn_manager.reset_game_objects()

    def __init_time_hud(self):
        self.manager.set_night_and_time(4, (0, 0))
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

        sect = self.manager.gamemap.sect

        if not self.spawn_manager.is_trigger_spawn and type(sect) is not mptown.PublicToilet:
            self.spawn_manager.spawn_alternate()

        self.three_am_event()

    def manage_progress(self):
        progress = self.get_progress_index()
        if progress == 0:
            self.show_title("Four")
            self.next()

        elif progress == 1:
            self.__to_ending()

        elif progress == 2:
            self.__check_news()

        elif progress == 3:
            self.__spawn_police()
            self.__spawn_car_and_gas()

        elif progress == 4:
            self.__talk_to_officer()

        elif progress == 5:
            self.__spawn_car_and_gas()
            self.__spawn_fill_gas_point()
            self.__bring_gas_to_officer()

        elif progress == 6:
            self.__spawn_doppelganger()

        elif progress == 7:
            self.__baiting()

        elif progress == 8:
            self.__get_to_car()

        elif progress == 9:
            self.__to_good_ending()

    def __to_ending(self):
        if not self.manager.progress_status.is_call_help:
            self.__not_call_help_ending()
            return

        if not self.__is_dizzy:
            HUDComp.create_board_text("Why Im so dizzy", self.manager.player.get_voice("voice28"))
            self.__is_dizzy = True

        if not self.manager.progress_status.is_get_potion:
            self.manager.player.set_speed(0.5)
            self.__not_have_potion_ending()
            return

        self.__drinking_potion()
        self.next()

    def __drinking_potion(self):
        HUDComp.create_board_text("Maybe I should drink the potion from the doctor",
                                  self.manager.player.get_voice("voice29"))

        HUDComp.create_board_text("...")
        HUDComp.create_board_text("I feel better", self.manager.player.get_voice("voice30"))

    def __not_call_help_ending(self):
        Effect.to_black_screen()
        SoundUtils.play_sound("../Assets/Sound/GrabielVoice/ending.mp3")
        self.manager.wait(10)
        self.__jumpscare()
        self.manager.wait(7)

        self.manager.set_game_progress(bd.BadEnding(self.screen))

    def __jumpscare(self):
        SoundUtils.play_sound("../Assets/Sound/Other/notcalljumpscare.mp3")
        screen = gm.Manager.get_instance().screen

        jumpscare = pg.image.load("../Assets/HUD/badending.png").convert()
        size = screen.get_size()

        jumpscare = pg.transform.scale(jumpscare, size)
        screen.blit(jumpscare, (0, 0))
        pg.display.update()

    def __not_have_potion_ending(self):
        self.__alpha -= 0.2
        Effect.set_opacity_all(round(self.__alpha))
        if not self.is_check:
            self.__check_news()

        if self.__alpha <= 0:
            SoundUtils.play_sound("../Assets/Sound/Other/fall.mp3")
            self.manager.wait(1)
            self.manager.set_game_progress(bd.BadEnding(self.screen))

    def __check_news(self):
        text = """Today, we have an accident at Park in the Mandela town. According to report, a drunk man driving a car 
        and crashed into a wall in Park. 
        |Fortunately, no one in the Park at that time so there is no casualties. The police will come up soon
        """

        if not self.watching_tv(text, "../Assets/Sound/NarratorVoice/voice3.mp3"):
            return

        HUDComp.create_board_text("I need to go", self.manager.player.get_voice("voice27"))
        HUDComp.create_board_text("Find your way to the help near market")

        if self.manager.progress_status.is_get_potion:
            self.can_change_map = True
            self.next()

        self.is_check = True

    def __spawn_car_and_gas(self):
        self.__spawn_broken_car()
        self.__spawn_gas_can()

    def __spawn_broken_car(self):
        if self.__is_spawn_gas_can:
            return

        sect = self.manager.gamemap.sect

        if type(sect) is not mptown.Park2:
            return

        point = sect.get_point("Broken Car")
        position = pg.math.Vector2(point.x, point.y)

        broken_car = otherobj.BrokenCar(position, mptown.Park2)
        self.spawn_manager.add_object(broken_car)

    def __spawn_gas_can(self):
        sect = self.manager.gamemap.sect

        if self.__is_spawn_gas_can:
            return

        if type(sect) is not mptown.Park2:
            return

        print("spawn")

        point = sect.get_point("GasCan")
        position = pg.math.Vector2(point.x, point.y)

        gas = otherobj.Gas(position, mptown.Park2)
        self.spawn_manager.add_object(gas)

        self.__is_spawn_gas_can = True

    def __spawn_fill_gas_point(self):
        sect = self.manager.gamemap.sect

        if not self.manager.progress_status.is_get_gas:
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

    def __spawn_police(self):
        sect = self.manager.gamemap.sect

        if type(sect) is not mptown.PublicToilet:
            return

        police_point = sect.get_point("Police")
        police_car_point = sect.get_point("PoliceCar")

        police_position = pg.math.Vector2(police_point.x, police_point.y)
        police_car_position = pg.math.Vector2(police_car_point.x, police_car_point.y)

        police = cp.Cop(police_position)
        self.spawn_manager.add_special_entity("cop", police, mptown.PublicToilet)

        police_car = otherobj.PoliceCar(police_car_position, mptown.PublicToilet)
        self.spawn_manager.add_object(police_car)

        self.next()

    def __talk_to_officer(self):
        police: cp.Cop = self.spawn_manager.get_special_entity("cop")
        position = police.get_position()

        area = Area("", position, 100, 100)

        player = self.manager.player
        keys = pg.key.get_pressed()

        if not keys[pg.K_f] or not area.is_overlap(player.get_rect()):
            return

        viole_speech = "Hi Officer. Why are you standing here. I think we need to get out of here quickly"
        HUDComp.create_board_text(viole_speech, player.get_voice("voice31"))

        officer_speech = """You are the guy who call help ? 
        I need you to do this and we can get out of here immediately"""
        HUDComp.create_board_text(officer_speech, police.get_voice("voice4"))

        HUDComp.create_board_text("Huh? What do you want me to do, officer ?", player.get_voice("voice32"))

        officer_speech = """These goddamn alternate block the shortest way. 
        I've taken the long detour to get here and my fuel are empty"""

        HUDComp.create_board_text(officer_speech, police.get_voice("voice5"))

        officer_speech = """Now can you find gas around this town and get it to me ?"""
        HUDComp.create_board_text(officer_speech, police.get_voice("voice6"))

        viole_speech = """Okay. I will find it, please hang in here"""
        HUDComp.create_board_text(viole_speech, player.get_voice("voice33"))

        HUDComp.create_board_text("Take care", police.get_voice("voice7"))

        HUDComp.create_board_text("I need to get gas for officer before 3AM")

        self.next()

    def __bring_gas_to_officer(self):
        if self.manager.progress_status.gas_amount < 100:
            return

        police: cp.Cop = self.spawn_manager.get_special_entity("cop")
        position = police.get_position()

        area = Area("", position, 100, 100)

        player = self.manager.player
        keys = pg.key.get_pressed()

        if not keys[pg.K_f] or not area.is_overlap(player.get_rect()):
            return

        HUDComp.create_board_text("Good job. I will pump it", police.get_voice("voice8"))

        dest = pg.math.Vector2(position.x + 90, position.y - 30)
        police.go_to(dest)

        self.next()

    def __spawn_doppelganger(self):
        sect = self.manager.gamemap.sect
        player = self.manager.player
        self.can_change_sect = False

        point = sect.get_point("OutsideMarketBk")
        position = pg.math.Vector2(point.x - 40, point.y)

        enemy = dp.Doppelganger(position)
        enemy.set_speed(2)
        player.set_speed(2.2)

        self.spawn_manager.add_enemy(enemy)
        self.next()

    def __baiting(self):
        police: cp.Cop = self.spawn_manager.get_special_entity("cop")

        if not self.is_occur_start_event:
            HUDComp.create_board_text("What ? That is a doppelganger, baiting him. I will refill this car quickly",
                                      police.get_voice("voice9"))

            self.is_occur_start_event = True

        self.__time += gm.Game.get_time()

        if self.__time >= self.__end_time:
            self.next()

    def __get_to_car(self):
        police: cp.Cop = self.spawn_manager.get_special_entity("cop")

        if not self.is_occur_start_event:
            position = police.get_position()
            HUDComp.create_board_text("Hurry, Get in car",
                                      police.get_voice("voice10"))

            dest = pg.math.Vector2(position.x + 100, position.y)
            police.go_to(dest)

            self.is_occur_start_event = True
            return

        self.manager.progress_status.can_get_in_car = True

        if police is not None and not police.is_moving:
            self.spawn_manager.remove_special_entity("cop")

        if self.manager.progress_status.get_in_car:
            self.__disable_player()
            self.next()

    def __disable_player(self):
        player = self.manager.player

        player.get_image().set_alpha(0)
        self.can_press_key = False

    def __to_good_ending(self):
        good_ending = gd.GoodEnding(self.screen)
        self.manager.set_game_progress(good_ending)

