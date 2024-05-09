from __future__ import annotations
from typing import Callable

import abc
import random

import src.utils.effect as ge
import src.mapcontainer.map as mp
import src.hud.hudcomp as hud
import src.gamemanage.spawnmanager as spm
import src.mapcontainer.town as mptown
import src.entity.thealternate.enemy as em
import src.mapcontainer.housenormal as mphouse

from src.hud.timehud import *
from src.hud.hudcomp import *
from src.pjenum import *
from src.utils import *


class ProgressManager(abc.ABC):
    def __init__(self,
                 screen: pg.surface.Surface,
                 game_objects: pg.sprite.Group = None):
        self.screen = screen

        self.is_occur_start_event = False
        self.can_press_key = False
        self.can_change_map = False
        self.can_change_sect = True
        self.can_sleep = False

        self.__progress = 0

        self.nextpart = None
        self.to_next = True

        self.manager = gm.Manager.get_instance()

        self.spawn_manager = spm.SpawnManager(game_objects)
        self.time_hud: TimeHUD | None = None

    def setup(self):
        self.spawn_manager.update_special_entities()
        self.spawn_manager.update_list_object()

    @abc.abstractmethod
    def re_setup(self):
        pass

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
        if not self.can_change_sect:
            return

        gamemap = self.manager.gamemap
        player = self.manager.player

        if gamemap is None or player.get_state() == EState.DEAD:
            return

        sect_name = gamemap.sect.in_area(player.get_rect())
        current = gamemap.sect

        gamemap.change_sect(sect_name)

        if gamemap.sect == current:
            return

        self.changing_sect()

    def changing_sect(self):
        gamemap = self.manager.gamemap
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

    # FOR NIGHT
    def __get_title(self, night: str) -> tuple[pg.surface.Surface, pg.rect.Rect]:
        fontpath = "../Assets/Font/Crang.ttf"
        center = self.screen.get_size()

        font = pg.font.Font(fontpath, 40)
        title_surf = Effect.create_text_outline(font,
                                                f"Night {night}",
                                                (255, 255, 255),
                                                2,
                                                (255, 0, 0))

        title_rect = title_surf.get_rect(center=(center[0] / 2, center[1] / 2))
        return title_surf, title_rect

    def __draw_title(self, title_surf: pg.surface.Surface, title_rect: pg.rect.Rect):
        self.screen.blit(title_surf, title_rect)
        pg.display.update()

    def show_title(self, night: str):
        Effect.to_black_screen()
        title = self.__get_title(night)
        self.__draw_title(title[0], title[1])

        self.manager.wait(2)

        Effect.fade_out_list(self.screen, [title])
        Effect.set_full_opacity_screen()

        self.can_press_key = True

    def watching_tv(self, text: str, path_voice: str) -> bool:
        player = self.manager.player
        sect = self.manager.gamemap.sect

        if type(sect) is not mphouse.Room:
            if self.is_occur_start_event:
                pg.mixer.stop()

            self.is_occur_start_event = False
            return False

        if not self.is_occur_start_event:
            SoundUtils.play_sound("../Assets/Sound/Other/tvlost.mp3", True)
            self.is_occur_start_event = True

        area = sect.get_area("TV")
        keys = pg.key.get_pressed()

        if not area.is_overlap(player.get_rect()) or not keys[pg.K_f]:
            return False

        pg.mixer.stop()

        voice = pg.mixer.Sound(path_voice)
        HUDComp.create_board_text(text, voice)

        return True

    def is_sleep(self):
        keys = pg.key.get_pressed()

        if not self.can_sleep:
            return False

        if not keys[pg.K_f]:
            return False

        area = self.manager.gamemap.sect.get_area("Bed")
        player = self.manager.player

        if area is None or not area.is_overlap(player.get_rect()):
            return False

        if player.get_hungry_amount() < 50:
            HUDComp.create_board_text("Im too hungry. I cannot sleep", player.get_voice("hungry"))
            return False

        return True

    def changing_night_when_sleep(self, night: ProgressManager):
        ge.Effect.fade_out_screen()
        self.manager.set_game_progress(night)

    def kill_time_hud(self):
        if self.time_hud is not None:
            self.time_hud.kill()

    def three_am_event(self):
        if self.spawn_manager.is_spawn_instruder():
            self.can_sleep = False
            self.spawn_manager.spawn_instruder()

        if self.is_grabiel_coming():
            self.grabiel_coming()

    def is_grabiel_coming(self):
        time = self.manager.game_time[0]
        if time < 3:
            return False

        gamemap = self.manager.gamemap

        if type(gamemap) is not mptown.Town:
            return False

        return True

    def grabiel_coming(self):
        SoundUtils.play_sound("../Assets/Sound/GrabielVoice/voice3.mp3")
        self.manager.wait(1)

        self.__set_grabiel_image("icon.jpg")

        self.__pray()

    def __set_grabiel_image(self, image: str):
        screen = gm.Manager.get_instance().screen

        jumpscare = pg.image.load(f"../Assets/HUD/{image}").convert()
        size = screen.get_size()

        jumpscare = pg.transform.scale(jumpscare, size)
        screen.blit(jumpscare, (0, 0))
        pg.display.update()

    def __pray(self):
        self.can_press_key = False

        SoundUtils.play_sound("../Assets/Sound/GrabielVoice/pray.mp3")
        self.manager.wait(5)
        self.__set_grabiel_image("grabielcorrupt.png")
        self.manager.wait(6)

        self.manager.player.set_state(EState.DEAD)
