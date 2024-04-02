import mapcontainer.map as mp
import pygame as pg


class Physic:
    def __init__(self):
        pass

    @staticmethod
    def is_collide_wall(rect: pg.rect.Rect) -> bool:
        """
        :param rect: Next rect
        """

        bottom_left = rect.bottomleft
        bottom_right = rect.bottomright
        top = rect.midbottom[0], rect.midbottom[1] - 10

        walls = mp.Sect.walls

        if (top in walls
                or bottom_right in walls
                or bottom_left in walls):
            return True

        return False

    @staticmethod
    def is_collide(rect1: pg.rect.Rect, rect2: pg.rect.Rect) -> bool:
        top = rect1.midbottom[0], rect1.midbottom[1] - 10
        botlf = rect1.bottomleft
        botrg = rect1.bottomright

        if (rect2.collidepoint(top)
                or rect2.collidepoint(botlf)
                or rect2.collidepoint(botrg)):
            return True

        return False
