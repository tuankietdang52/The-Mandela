import abc
import random

import src.utils.effect as ge
import src.mapcontainer.map as mp
import src.hud.hudcomp as hud
import src.gamemanage.spawnmanager as spm

from src.hud.timehud import *
from src.pjenum import *
from src.utils import *


class ProgressManager(abc.ABC):
    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen

        self.is_occur_start_event = False
        self.can_press_key = False
        self.can_change_map = False

        self.__progress = 0
        self.load_progress_index = 0

        self.nextpart = None
        self.to_next = True

        self.manager = gm.Manager.get_instance()
        self.spawn_manager = spm.SpawnManager()
        self.time_hud: TimeHUD | None = None

    def setup(self):
        self.spawn_manager.update_list_entities()
        self.spawn_manager.update_list_object()

    def update(self):
        self.event_action()
        self.pressing_key()

        self.handle_change_map()
        self.handle_change_sect()
        self.manage_progress()

    @abc.abstractmethod
    def event_action(self):
        pass

    def pressing_key(self):
        player = self.manager.player

        if not self.can_press_key:
            return

        keys = pg.key.get_pressed()

        player.action_key(keys)

    @abc.abstractmethod
    def manage_progress(self):
        pass

    def set_progress_index(self, progress_index: int):
        self.__progress = progress_index
        self.is_occur_start_event = False

    def next(self):
        self.__progress += 1
        self.is_occur_start_event = False

    def previous(self):
        self.__progress -= 1

    def get_progress_index(self) -> int:
        return self.__progress

    def handle_change_map(self):
        if not self.can_change_map:
            return

        sect = self.manager.gamemap.sect
        player = self.manager.player

        area = sect.in_area(player.get_rect())
        keys = pg.key.get_pressed()

        if not keys[pg.K_f]:
            return

        map_comp = self.manager.gamemap.get_next_map(area)
        if map_comp is None:
            return

        next_map, text = map_comp

        hud.HUDComp.create_board_text(text)
        choice = hud.HUDComp.create_accept_board().yes_choice

        if choice:
            self.changing_map(next_map)
            self.spawn_manager.clear_enemies()
            self.spawn_manager.is_trigger_spawn = False

    def changing_map(self, next_map: mp.Map):
        self.manager.set_map(next_map)
        sect = self.manager.gamemap.sect

        ge.Effect.fade_out_screen()

        self.spawn_manager.clear_object_and_enemies()
        self.spawn_manager.is_trigger_spawn = False

        sect.create()
        sect.set_opacity(0)
        self.reposition_player()

        self.manager.wait(1)
        SoundUtils.clear_all_sound()
        ge.Effect.fade_in_screen()

    def handle_change_sect(self):
        gamemap = self.manager.gamemap
        player = self.manager.player

        if gamemap is None or player.get_state() == EState.DEAD:
            return

        sect_name = gamemap.sect.in_area(player.get_rect())
        current = gamemap.sect

        gamemap.change_sect(sect_name)

        if gamemap.sect == current:
            return

        self.spawn_manager.clear_object_and_enemies()
        self.spawn_manager.is_trigger_spawn = False

        gamemap.sect.create()
        self.reposition_player()

        self.manager.update_UI_ip()

    def reposition_player(self):
        """Place player in map section start point"""
        player = self.manager.player
        sect = self.manager.gamemap.sect
        start_pos = sect.get_start_point()

        player.set_position(start_pos)

    def kill_time_hud(self):
        if self.time_hud is not None:
            self.time_hud.kill()
