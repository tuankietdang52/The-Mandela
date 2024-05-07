import random
import pygame as pg
import src.gamemanage.game as gm
import src.gameobj.gameobject as go
import src.gameobj.food as fd
import src.gameobj.magazine as mg
import src.mapcontainer.map as mp
import src.mapcontainer.market as mk
import src.movingtype.ghostmoving as ghmv
import src.entity.thealternate.enemy as em
import src.mapcontainer.housenormal as mphouse

from src.entity.thealternate import (themurrayresidence as mr,
                                     doppelganger as dp,
                                     mimic as mm,
                                     flawedimpersonators as fi,
                                     instruder as it)

from src.utils import *
from src.tilemap import *
from src.eventhandle.argument import *


class SpawnManager:
    def __init__(self, game_objects: pg.sprite.Group = None):
        self.manager = gm.Manager.get_instance()

        self.special_entities: set[tuple[str, pg.sprite.Sprite, type[mp.Sect]]] = set()

        self.game_objects = pg.sprite.Group()
        self.game_objects_backup = pg.sprite.Group()

        if game_objects is not None:
            self.game_objects = game_objects
            self.game_objects_backup = game_objects.copy()

        self.is_trigger_spawn = False
        self.is_have_instruder = False

        self.enemy_spawn_chance = 0

    def set_enemy_spawn_chance(self, spawn_chance: int):
        self.enemy_spawn_chance = spawn_chance

    def set_game_objects(self, game_objects: pg.sprite.Group):
        self.game_objects = game_objects.copy()

    def reset_game_objects(self):
        self.game_objects = self.game_objects_backup.copy()

        for obj in self.game_objects:
            if obj.is_back_up:
                obj.re_setup()

    def clear_object_and_enemies(self):
        self.clear_enemies()
        self.update_special_entities()
        self.update_list_object()

    def clear_enemies(self):
        for enemy in self.manager.appear_enemies:
            self.remove_enemy(enemy)

    def clear_special_enemies(self):
        self.special_entities.clear()
        self.update_special_entities()

    def get_spawn_position(self, area: Area) -> pg.math.Vector2:
        area_rect = area.get_rect()
        area_tl = area_rect.topleft

        x_limit = round(area_tl[0] + area.width)
        y_limit = round(area_tl[1] + area.height)

        x = random.randint(round(area.x), x_limit)
        y = random.randint(round(area.y), y_limit)

        return pg.math.Vector2(x, y)

    def __is_spawn_alternate(self) -> bool:
        sanity = self.manager.player.get_sanity_amount()
        plus_chance = (100 - sanity) / 8 if 100 - sanity != 0 else 0

        spawn_chance = self.enemy_spawn_chance + plus_chance

        chance = random.randint(0, 100)
        if chance <= spawn_chance:
            return True

        return False

    def __get_spawn_enemy_position(self) -> pg.math.Vector2 | None:
        sect = self.manager.gamemap.sect

        index = random.randint(0, sect.spawn_enemy_area_count)
        area = sect.get_area(f"SpawnArea{index}")

        if area is None:
            return None

        return self.get_spawn_position(area)

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

        position = self.__get_spawn_enemy_position()

        if position is None:
            return

        enemy = self.__get_random_alternate(position)

        if (Physic.is_collide_wall(enemy.get_rect()) and
                type(enemy.get_movement()) != ghmv.GhostMoving):
            self.manager.entities.remove(enemy)
            return

        self.add_enemy(enemy)

    def __get_instruder_spawm_pos(self) -> pg.math.Vector2:
        point = self.manager.gamemap.sect.get_point("Instruder")

        position = pg.math.Vector2(point.x, point.y)

        return position

    def is_spawn_instruder(self) -> bool:
        time = self.manager.game_time[0]
        if time < 3:
            self.is_have_instruder = False
            return False

        if self.is_have_instruder:
            return False

        gamemap = self.manager.gamemap

        if type(gamemap) is not mphouse.HouseNormal:
            return False

        return True

    def spawn_instruder(self):
        position = self.__get_instruder_spawm_pos()

        self.is_have_instruder = True

        instruder = it.Instruder(position)
        self.add_enemy(instruder)

    def add_enemy(self, enemy: em.Enemy):
        self.manager.appear_enemies.add(enemy)
        self.manager.entities.add(enemy)

    def remove_enemy(self, enemy: em.Enemy):
        enemy.on_destroy(EventArgs.empty())
        enemy.kill()

    def add_special_entity(self, name: str, enemy: pg.sprite.Sprite, section: type[mp.Sect]):
        self.special_entities.add((name, enemy, section))
        self.update_special_entities()

    def get_special_entity(self, name: str) -> pg.sprite.Sprite | None:
        for enemy in self.special_entities:
            if enemy[0] == name:
                return enemy[1]

        return None

    def remove_special_entity(self, name: str):
        entity = None
        for item in self.special_entities:
            if item[0] != name:
                continue

            entity = item
            if type(item[1]) is em.Enemy:
                item[1].on_destroy(EventArgs.empty())
            item[1].kill()

        if entity is not None:
            self.special_entities.remove(entity)

    def update_special_entities(self):
        self.manager.clear_entities()

        if len(self.special_entities) == 0:
            return

        for entity in self.special_entities:
            if not self.__check_appear(entity[2]):
                continue

            if type(entity[1]).__mro__[1] is em.Enemy:
                self.manager.appear_enemies.add(entity[1])

            self.manager.on_entities_destroy += entity[1].destroy_callback
            self.manager.entities.add(entity[1])

    def __check_appear(self, entity_sect: type[mp.Sect]):
        cur = self.manager.gamemap.sect

        if type(cur) is entity_sect:
            return True

        return False

    def __get_object_position(self) -> tuple[str, pg.math.Vector2 | None]:
        sect = self.manager.gamemap.sect

        index = random.randint(0, sect.spawn_item_area_count)
        area = sect.get_area(f"ItemSpawn{index}")

        if area is None:
            return "", None

        return area.name, self.get_spawn_position(area)

    def spawn_items_in_market(self):
        i = 0
        while i < 25:
            area_name, position = self.__get_object_position()

            if position is None:
                continue

            if area_name == "ItemSpawn2":
                item = mg.Magazine(position, mk.MarketSect)

            else:
                item = fd.Spam(position, mk.MarketSect)

            self.add_object(item)
            i += 1

    def add_object(self, obj: go.GameObject):
        self.game_objects.add(obj)
        self.update_list_object()

    def remove_object(self, obj: go.GameObject):
        self.game_objects.add(obj)
        self.update_list_object()

    def update_list_object(self):
        sect = self.manager.gamemap.sect
        self.manager.appear_object.empty()

        for item in self.game_objects:
            if item.appear_sect == type(sect):
                self.manager.appear_object.add(item)
