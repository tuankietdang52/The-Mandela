import abc
import os

import pygame as pg
import pytmx

from tilemap import Area, Tile


class Map(abc.ABC):
    path = ""
    screen = None
    sect = None

    def change_sect(self, name: str):
        pass


class Sect:
    __wall_tile = list()
    walls = set()

    CAM_OFFSETX = 0
    """Higher = Left, Lower = Right"""

    CAM_OFFSETY = 0
    """Higher = Up, Lower = Down"""

    size = 64

    def __init__(self, screen, prev_sect=None):
        self.screen = screen

        self.map = None
        self.areas = []
        self.back_point = {}
        self.tilegroup = pg.sprite.Group()
        self.is_created = False

        if prev_sect is not None:
            self.prev_sect = prev_sect

    def init_OFFSET(self, offset, offsetfullscr):
        if self.screen.get_size() == (800, 800):
            self.CAM_OFFSETX, self.CAM_OFFSETY = offset

        else:
            self.CAM_OFFSETX, self.CAM_OFFSETY = offsetfullscr

    def load(self, path):
        if os.getcwd() == "C:\\Users\\ADMIN\\PycharmProjects\\Nightmare":
            self.map = pytmx.load_pygame(path)

    def set_pre_sect(self, prev_sect: str):
        self.prev_sect = prev_sect

    def get_start_point(self) -> tuple[float, float] | None:
        if self.prev_sect != "" and self.prev_sect is not None:
            start_area = self.prev_sect
        else:
            start_area = "Start"

        for area in self.areas:
            if area.name == start_area:
                return area.x, area.y

        return None

    def create(self):
        self.__wall_tile.clear()
        self.walls.clear()
        self.areas.clear()
        self.tilegroup.empty()

        self.is_created = True

        for layer in self.map.layers:
            if hasattr(layer, "data"):
                self.__draw_tile(layer)

            if isinstance(layer, pytmx.TiledObjectGroup):
                self.__init_areas(layer)

        self.__init_walls()

    def __draw_tile(self, layer):
        for x, y, surf in layer.tiles():
            pos = x * self.size - self.CAM_OFFSETX, y * self.size - self.CAM_OFFSETY

            tilesize = self.size, self.size

            surf = pg.transform.scale(surf, tilesize)

            tile = Tile(surf, pos, layer.name, layer.id, self.screen, layer.data[y][x], self.tilegroup)

            if "Wall" in layer.name or layer.name == "Object":
                self.__wall_tile.append(tile)

            self.screen.blit(tile.image, tile.rect)

    def __init_areas(self, layer):
        for area in layer:
            pos = pg.math.Vector2(area.x / 16 * self.size - self.CAM_OFFSETX,
                                  area.y / 16 * self.size - self.CAM_OFFSETY)

            width = area.width / 16 * self.size
            height = area.height / 16 * self.size

            tileobj = Area(area.name, pos, width, height)

            self.areas.append(tileobj)

    def __init_walls(self):
        for wall in self.__wall_tile:
            left_x, top_y = wall.rect.topleft
            width = wall.rect.width
            height = wall.rect.height

            right_x = left_x + width
            bot_y = top_y + height

            for y in range(top_y, bot_y):
                for x in range(left_x, right_x):
                    self.walls.add((x, y))
                    self.walls.add((x, y))

    def in_area(self, rect) -> str | None:
        for area in self.areas:
            if area.is_overlap(rect):
                return area.name

        return None

    def get_area(self, name: str) -> Area | None:
        """Return area with "name" """
        for area in self.areas:
            if area.name == name:
                return area

        return None

    def get_list_area(self, name: str) -> list[Area]:
        """Return list of area have "name" in their name"""
        ls = list()

        for area in self.areas:
            if name in area.name:
                ls.append(area)

        return ls

    def redraw(self):
        group = self.tilegroup

        group.draw(self.screen)
        # group.update()
