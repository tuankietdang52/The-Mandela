import pygame as pg
import src.gamemanage.game as gm


class Physic:

    @staticmethod
    def is_collide(rect1: pg.rect.Rect, rect2: pg.rect.Rect) -> bool:
        point = rect2.center
        if rect1.collidepoint(point):
            return True

        return False

    @staticmethod
    def is_collide_wall(rect):
        manager = gm.Manager.get_instance()

        bottom_left = round(rect.bottomleft[0] / 32), round(rect.bottomleft[1] / 32)
        bottom_right = round(rect.bottomright[0] / 32), round(rect.bottomright[1] / 32)
        top = round(rect.midbottom[0] / 32), round((rect.midbottom[1] - 10) / 32)

        walls = manager.gamemap.sect.walls

        if (top in walls
                or bottom_right in walls
                or bottom_left in walls):
            return True

        return False
