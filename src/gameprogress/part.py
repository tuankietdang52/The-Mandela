import abc
import random

import src.utils.effect as ge
import src.mapcontainer.map as mp
import src.hud.hudcomp as hud
import src.entity.thealternate.enemy as em
import src.movingtype.ghostmoving as ghmv

from src.entity.thealternate import (themurrayresidence as mr,
                                     doppelganger as dp,
                                     mimic as mm,
                                     flawedimpersonators as fi)
from src.pjenum import *
from src.utils import *


class Part(abc.ABC):
    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen

        self.enemies: list[em.Enemy] = list()
        self.special_enemies: set[tuple[str, em.Enemy, type[mp.Sect]]] = set()

        self.is_occur_start_event = False
        self.is_trigger_spawn = False
        self.can_press_key = False
        self.can_change_map = False

        self.__progress = 0

        self.nextpart = None
        self.to_next = True

        self.spawn_chance = 0

        self.manager = gm.Manager.get_instance()

    @abc.abstractmethod
    def setup(self):
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

    @abc.abstractmethod
    def pressing_key(self):
        pass

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
            self.is_trigger_spawn = False
            self.enemies.clear()

    def changing_map(self, next_map: mp.Map):
        self.manager.set_map(next_map)
        sect = self.manager.gamemap.sect

        ge.Effect.fade_out_screen()

        self.enemies.clear()
        self.manager.clear_entities()
        self.update_list_entities()

        sect.create()
        sect.set_opacity(0)

        self.reposition_player()

        self.manager.wait(1)
        pg.mixer.stop()
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

        self.is_trigger_spawn = False
        self.enemies.clear()
        self.update_list_entities()

        gamemap.sect.create()
        self.reposition_player()

        self.manager.update_UI_ip()

    def reposition_player(self):
        """Place player in map section start point"""
        player = self.manager.player
        sect = self.manager.gamemap.sect
        start_pos = sect.get_start_point()

        player.set_position(start_pos)

    def __is_spawn_alternate(self) -> bool:
        chance = random.randint(0, 100)
        print(chance)
        if chance <= self.spawn_chance:
            return True

        return False

    def __get_spawn_area(self) -> pg.math.Vector2 | None:
        sect = self.manager.gamemap.sect

        index = random.randint(0, sect.spawn_area_count)
        area = sect.get_area(f"SpawnArea{index}")

        if area is None:
            return None

        area_rect = area.get_rect()
        area_tl = area_rect.topleft

        x_limit = round(area_tl[0] + area.width)
        y_limit = round(area_tl[1] + area.height)

        x = random.randint(round(area.x), x_limit)
        y = random.randint(round(area.y), y_limit)

        return pg.math.Vector2(x, y)

    def __get_random_alternate(self, position: pg.math.Vector2) -> em.Enemy:
        chance = random.randint(0, 100)

        if chance < 5:
            return fi.FlawedImpersonators(position)

        elif chance < 15:
            return mr.TheMurrayResidence(position)

        elif chance < 50:
            return mm.Mimic(position)

        else:
            return dp.Doppelganger(position)

    def spawn_alternate(self):
        self.is_trigger_spawn = True
        if not self.__is_spawn_alternate():
            return

        position = self.__get_spawn_area()

        if position is None:
            return

        enemy = self.__get_random_alternate(position)
        # enemy = dp.Doppelganger(position, self.manager.entities)

        if (Physic.is_collide_wall(enemy.get_rect()) and
                type(enemy.get_movement()) != ghmv.GhostMoving):
            self.manager.entities.remove(enemy)
            return

        self.add_enemy(enemy)

    def add_enemy(self, enemy: em.Enemy):
        self.enemies.append(enemy)
        self.update_list_entities()

    def remove_enemy(self, enemy: em.Enemy):
        enemy.kill()
        self.update_list_entities()

    def add_special_enemy(self, name: str, enemy: em.Enemy, section: type[mp.Sect]):
        self.special_enemies.add((name, enemy, section))
        self.update_list_entities()

    def get_special_enemy(self, name: str) -> em.Enemy | None:
        for enemy in self.special_enemies:
            if enemy[0] == name:
                return enemy[1]

        return None

    def remove_special_enemy(self, name: str):
        for item in self.special_enemies:
            if item[0] == name:
                item[1].kill()
                break

    def update_list_entities(self):
        self.manager.clear_entities()

        if len(self.enemies) == 0 and len(self.special_enemies) == 0:
            return

        for enemy in self.enemies:
            self.manager.appear_enemy.add(enemy)
            self.manager.entities.add(enemy)

        for enemy in self.special_enemies:
            if self.__check_appear(enemy[2]):
                self.manager.appear_enemy.add(enemy[1])
                self.manager.entities.add(enemy[1])

        self.manager.update_UI_ip()

    def __check_appear(self, enemy_sect: type[mp.Sect]):
        cur = self.manager.gamemap.sect

        if enemy_sect == type(cur):
            return True

        return False
