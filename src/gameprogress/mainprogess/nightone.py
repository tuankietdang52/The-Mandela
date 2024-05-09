from typing import Callable
import pygame as pg
import src.gamemanage.game as gm
import src.gameobj.otherobj as otherobj
import src.mapcontainer.market as mk
import src.gameprogress.progressmanager as gp
import src.gameprogress.mainprogess.nighttwo as n2

import src.mapcontainer.town as mptown
import src.gameobj.food as fd

from src.hud.hudcomp import *
from src.hud.timehud import *


class NightOne(gp.ProgressManager):
    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen)

        self.can_press_key = False
        self.can_change_map = True
        self.can_sleep = False

        self.setup()

        self.visited_sect = set()

        self.spawn_manager.set_enemy_spawn_chance(5)

    def re_setup(self):
        self.can_press_key = False
        self.can_change_map = True
        self.can_sleep = False
        self.visited_sect = set()

        self.is_occur_start_event = False

        self.manager.progress_status.reset()
        self.manager.on_entities_destroy.clear_callback()
        self.manager.player.interact.clear_callback()

        self.spawn_manager.set_enemy_spawn_chance(5)
        self.manager.hud_groups.empty()
        self.spawn_manager.set_game_objects(pg.sprite.Group())

    def event_action(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if not self.can_press_key:
                    return

    def __setup_hud(self):
        self.manager.player.init_hud(self.manager.hud_groups)
        self.manager.player.decrease_hungry_amount(70)

        self.manager.set_night_and_time(1, (0, 0))
        self.time_hud = TimeHUD(self.manager.hud_groups)

    def __show_guide(self):
        guide = """In the upper left corner, there are 2 bars.
        |One show how hungry you are, if the bar is down to empty. You'll die
        |Other will show your sanity. The lower sanity you are, the more alternate spawn, read magazine will increase it
        | |You can only sleep after 2 AM |[Go to bed and press F]
        | | | |WARNING: COMEBACK HOME AND SLEEP BEFORE 3 AM"""

        HUDComp.show_note(guide, 20)
        self.__show_next_guide()

    def __show_next_guide(self):
        guide = """You need to survive until night 4. 
        | |You need to call for help before night 4 or you will never get out of here
        """

        HUDComp.show_note(guide, 20)

    def update(self):
        super().update()

        if not self.spawn_manager.is_trigger_spawn:
            self.spawn_manager.spawn_alternate()

        if self.is_sleep():
            tomorrow = n2.NightTwo(self.screen, self.spawn_manager.game_objects)
            self.changing_night_when_sleep(tomorrow)

        self.three_am_event()

    def manage_progress(self):
        progress = self.get_progress_index()

        if progress == 0:
            self.show_title("One")
            self.next()

        elif progress == 1:
            self.__setup_hud()
            self.next()

        elif progress == 2:
            self.__show_guide()
            self.next()

        elif progress == 3:
            self.__mission()
            self.next()

        elif progress == 4:
            self.__spawn_items()

        elif progress == 5:
            self.__find_someone()

        elif progress == 6:
            self.__visit_police_sect()
            self.__visit_graveyard_sect()
            self.__visit_sect()

    def __mission(self):
        HUDComp.create_board_text("Before going, I should call someone for help",
                                  self.manager.player.get_voice("voice9"))
        HUDComp.create_board_text("...")
        HUDComp.create_board_text("My phone is broke. How ??",
                                  self.manager.player.get_voice("voice10"))
        HUDComp.create_board_text("Maybe I should go find some food first or I will starve to death",
                                  self.manager.player.get_voice("voice11"))

    def __spawn_items(self):
        sect = self.manager.gamemap.sect
        if type(sect) is not mk.MarketSect:
            return

        HUDComp.create_board_text("Where is everyone ?!", self.manager.player.get_voice("voice12"))

        self.spawn_manager.spawn_items_in_market()
        self.next()

    def __find_someone(self):
        player = self.manager.player

        if player.get_hungry_amount() < 98:
            return

        HUDComp.create_board_text("Im full. Now I think I should looking for someone",
                                  player.get_voice("voice13"))

        self.next()

    def __visit_sect(self):
        gamemap = self.manager.gamemap

        if type(gamemap) is not mptown.Town:
            self.can_change_map = True
            return
        else:
            self.can_change_map = False

        self.visited_sect.add(gamemap.sect)

        if len(self.visited_sect) != len(gamemap.sections):
            return

        HUDComp.create_board_text("Why is there no one in this town ?",
                                  self.manager.player.get_voice("voice14"))

        self.can_change_map = True
        self.next()

    def __visit_police_sect(self):
        sect = self.manager.gamemap.sect

        if type(sect) is mptown.Police and sect not in self.visited_sect:
            HUDComp.create_board_text("There is phone booth! |I can call for help",
                                      self.manager.player.get_voice("voice17"))
        else:
            self.__check_phone()

    def __check_phone(self):
        sect = self.manager.gamemap.sect

        if type(sect) is not mptown.Police:
            return

        area = sect.get_area("Phone")
        player = self.manager.player
        keys = pg.key.get_pressed()

        if not keys[pg.K_f] or not area.is_overlap(player.get_rect()):
            return

        HUDComp.create_board_text("Unfortunately, I dont have coin",
                                  player.get_voice("voice18"))

        HUDComp.create_board_text("I should keep looking for someone",
                                  player.get_voice("voice34"))

    def __visit_graveyard_sect(self):
        sect = self.manager.gamemap.sect

        if type(sect) is not mptown.Graveyard or sect in self.visited_sect:
            return

        point = sect.get_point("Shovel")
        position = pg.math.Vector2(point.x, point.y)

        shovel = otherobj.Shovel(position, mptown.Graveyard)
        self.spawn_manager.add_object(shovel)
