import sys
import pygame as pg
import src.mapcontainer.market as mk
import src.mapcontainer.town as mptown
import src.gameobj.otherobj as otherobj
import src.entity.thealternate.mimic as mm
import src.gameprogress.progressmanager as gp
import src.mapcontainer.housenormal as mphouse
import src.gameprogress.mainprogess.nightfour as n4

from src.hud.timehud import *
from src.hud.hudcomp import *


class NightThree(gp.ProgressManager):
    def __init__(self, screen: pg.surface.Surface, game_objects: pg.sprite.Group = None):
        super().__init__(screen, game_objects)

        self.can_change_map = True
        self.can_press_key = True
        self.can_sleep = False

        self.manager.progress_status.is_call_help = False
        self.manager.progress_status.is_get_shovel = False

        self.spawn_manager.set_enemy_spawn_chance(50)

        # self.a = False

        self.__init_time_hud()

    def re_setup(self):
        self.can_change_map = True
        self.can_press_key = True
        self.can_sleep = False
        self.is_occur_start_event = False

        self.manager.progress_status.is_call_help = False
        self.manager.progress_status.is_get_shovel = False

        self.spawn_manager.set_enemy_spawn_chance(50)
        self.spawn_manager.reset_game_objects()
        self.__init_time_hud()

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
            tomorrow = n4.NightFour(self.screen, self.spawn_manager.game_objects)
            self.changing_night_when_sleep(tomorrow)

        self.three_am_event()

    def manage_progress(self):
        progress = self.get_progress_index()

        if progress == 0:
            self.show_title("Three")
            self.next()

        elif progress == 1:
            self.__make_player_hungry()

        elif progress == 2:
            self.__check_cashier_table()
            self.__spawn_mimic()

        elif progress == 3:
            self.__break_cashier_box()

        elif progress == 4:
            self.__call_for_help()

    def __make_player_hungry(self):
        player = self.manager.player

        player.set_hungry_amount(25)
        player.hungry_bar.update()
        self.manager.update_UI_ip()

        HUDComp.create_board_text("Why Im so hungry ? Like one week no eat", player.get_voice("voice22"))
        HUDComp.create_board_text("I need to go get food quickly", player.get_voice("voice23"))

        self.next()

    def __check_cashier_table(self):
        sect = self.manager.gamemap.sect
        player = self.manager.player

        if type(sect) is not mk.MarketSect:
            return

        # if not self.a:
        #     self.manager.gameprogress.spawn_manager.spawn_items_in_market()
        #     self.a = True

        if not self.is_occur_start_event:
            if player.get_hungry_amount() < 99:
                return

            HUDComp.create_board_text("Wait, Maybe I can get coins in cashier table",
                                      player.get_voice("voice19"))

            self.is_occur_start_event = True

        area = sect.get_area("Cashier Table")
        keys = pg.key.get_pressed()

        if not keys[pg.K_f] or not area.is_overlap(player.get_rect()):
            return

        HUDComp.create_board_text("Its locked. I cant open it", player.get_voice("voice20"))
        HUDComp.create_board_text("I need to find something to break it, something big",
                                  player.get_voice("voice21"))

    def __spawn_mimic(self):
        sect = self.manager.gamemap.sect

        if type(sect) is not mptown.Graveyard:
            return

        if not self.manager.progress_status.is_get_shovel:
            return

        area = sect.get_area("SpawnArea0")
        position = self.spawn_manager.get_spawn_position(area)

        mimic = mm.Mimic(position)
        mimic.set_speed(1.8)
        mimic.is_chasing = True

        self.spawn_manager.add_enemy(mimic)
        self.next()

    def __break_cashier_box(self):
        sect = self.manager.gamemap.sect
        player = self.manager.player

        if type(sect) is not mk.MarketSect:
            return

        area = sect.get_area("Cashier Table")
        keys = pg.key.get_pressed()

        if not keys[pg.K_f] or not area.is_overlap(player.get_rect()):
            return

        if not self.manager.progress_status.is_get_shovel:
            HUDComp.create_board_text("I need to find something to break it, something big",
                                      player.get_voice("voice21"))
            return

        SoundUtils.play_sound("../Assets/Sound/Other/smash.mp3")
        self.manager.wait(3)

        HUDComp.create_board_text("You got the coin")
        self.next()

    def __call_for_help(self):
        sect = self.manager.gamemap.sect
        player = self.manager.player

        if type(sect) is not mptown.Police:
            return

        area = sect.get_area("Phone")
        keys = pg.key.get_pressed()
        if not keys[pg.K_f] or not area.is_overlap(player.get_rect()):
            return

        SoundUtils.play_sound("../Assets/Sound/Other/coin.mp3")
        self.manager.wait(1.5)
        self.__conversation()

    def __conversation(self):
        player = self.manager.player
        police_voice_path = "../Assets/Sound/PoliceVoice/"

        HUDComp.create_board_text("This is 911 emergency, what's your situation ?",
                                  pg.mixer.Sound(f"{police_voice_path}voice1.wav"))

        HUDComp.create_board_text("I need help, I now in the Mandela Town, can you guys come and get me out of here ?",
                                  player.get_voice("voice24"))

        long_text = """The Mandela Town ? There were supposed not having anyone live there 
        |How are you still there alive ?"""
        HUDComp.create_board_text(long_text, pg.mixer.Sound(f"{police_voice_path}voice2.wav"))

        long_text = """I swear to god Im still alive, Im not a doppelganger. 
                |Please come quickly, I will go crazy if I stay here another day"""
        HUDComp.create_board_text(long_text, player.get_voice("voice25"))

        long_text = """Okay. 
                |We understand, we will send rescue to there, but it takes 1 day to get there 
                |Can you survive until tomorrow ?"""
        HUDComp.create_board_text(long_text, pg.mixer.Sound(f"{police_voice_path}voice3.wav"))

        HUDComp.create_board_text("Ok. I will try my best.", player.get_voice("voice26"))

        self.next()
