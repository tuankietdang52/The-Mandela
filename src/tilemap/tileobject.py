import pygame as pg
import src.gamemanage.game as gm

from src.pjenum import *


class Area:
    """Position by center"""
    def __init__(self,
                 name: str,
                 pos: pg.math.Vector2,
                 width: float,
                 height: float,
                 pos_type: EPosition = EPosition.CENTER,
                 groups: list = None):
        """
        :param pos_type: Area must be placed by center, if you pass topleft position, set this to TOPLEFT
        """

        self.name = name
        self.width = width
        self.height = height

        if pos_type == EPosition.TOPLEFT:
            self.x, self.y = self.get_center(pos)
        else:
            self.x, self.y = pos

        if groups is not None:
            groups.append(self)

    def get_center(self, pos: pg.math.Vector2) -> tuple[int, int]:
        area = pg.Surface((self.width, self.height))
        area_rect = area.get_rect(topleft=pos)

        return area_rect.center

    def get_rect(self) -> pg.rect.Rect:
        surf = pg.surface.Surface((self.width, self.height))
        rect = surf.get_rect(center=(self.x, self.y))

        return rect

    def is_overlap(self, rect: pg.rect.Rect) -> bool:
        area_rect = self.get_rect()

        # pg.draw.rect(gm.Manager.get_instance().screen, (0, 255, 0), area_rect)

        if area_rect.colliderect(rect):
            return True

        return False

    def draw(self):
        area = pg.Surface((self.width, self.height))
        rect = area.get_rect(topleft=(self.x, self.y))

        points = [
            rect.topleft,
            rect.topright,
            rect.bottomright,
            rect.bottomleft
        ]

        pg.draw.lines(gm.Manager.screen, (0, 0, 0), True, points, 7)
        pg.display.update()


class Point:
    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.x = x
        self.y = y

    def is_in_point(self, rect: pg.rect.Rect) -> bool:
        return rect.collidepoint(self.x, self.y)

