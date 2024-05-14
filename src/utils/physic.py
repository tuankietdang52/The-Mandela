import pygame as pg
import src.gamemanage.game as gm

from src.tilemap import *


class Physic:
    @staticmethod
    def is_collide(rect1: pg.rect.Rect, rect2: pg.rect.Rect) -> bool:
        point = rect2.center
        if rect1.collidepoint(point):
            return True

        return False

    @staticmethod
    def is_collide_object(rect: pg.rect.Rect):
        manager = gm.Manager.get_instance()

        bottom_left = rect.bottomleft
        bottom_right = rect.bottomright
        top = rect.midbottom[0], rect.midbottom[1] - 10

        game_objects = manager.appear_object

        for obj in game_objects:
            if obj.can_walk_through:
                continue

            if (obj.rect.collidepoint(bottom_left)
                    or obj.rect.collidepoint(bottom_right)
                    or obj.rect.collidepoint(top)):
                return True

        return False

    @staticmethod
    def is_collide_wall(rect: pg.rect.Rect):
        manager = gm.Manager.get_instance()

        bottom_left = rect.bottomleft
        bottom_right = rect.bottomright
        top = rect.midbottom[0], rect.midbottom[1] - 10

        walls = manager.gamemap.sect.walls

        if (top in walls
                or bottom_left in walls
                or bottom_right in walls):
            return True

        return False
