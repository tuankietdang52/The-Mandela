import random
import pygame as pg
import src.gamemanage.game as gm
import src.gameitem.food as fd
import src.movingtype.ghostmoving as ghmv
import src.entity.thealternate.enemy as em
import src.mapcontainer.map as mp

from src.entity.thealternate import (themurrayresidence as mr,
                                     doppelganger as dp,
                                     mimic as mm,
                                     flawedimpersonators as fi)

from src.utils import *


class SpawnManager:
    def __init__(self):
        self.manager = gm.Manager.get_instance()

        self.enemies: list[em.Enemy] = list()
        self.special_enemies: set[tuple[str, em.Enemy, type[mp.Sect]]] = set()
        self.game_items = pg.sprite.Group()

        self.is_trigger_spawn = False

        self.enemy_spawn_chance = 0

    def set_enemy_spawn_chance(self, spawn_chance):
        self.enemy_spawn_chance = spawn_chance

    def clear_object_and_enemies(self):
        self.enemies.clear()
        self.update_list_entities()
        self.update_list_object()

    def clear_enemies(self):
        self.enemies.clear()
        self.update_list_entities()

    def clear_special_enemies(self):
        self.special_enemies.clear()
        self.update_list_entities()

    def __is_spawn_alternate(self) -> bool:
        chance = random.randint(0, 100)
        print(chance)
        if chance <= self.enemy_spawn_chance:
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

    def add_food(self, food):
        self.game_items.add(food)
        self.update_list_object()

    def remove_food(self, food):
        self.game_items.add(food)
        self.update_list_object()

    def update_list_object(self):
        sect = self.manager.gamemap.sect
        self.manager.appear_object.empty()

        for food in self.game_items:
            if food.appear_sect == type(sect):
                self.manager.appear_object.add(food)
