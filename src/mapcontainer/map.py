import abc
import os

import pygame as pg
import pytmx

from src.tilemap import Area, Tile


class Sect:
    __wall_tile = list()
    walls = set()

    ori_block_size = 0
    size = 0

    CAM_OFFSETX = 0
    """Higher = Left, Lower = Right"""

    CAM_OFFSETY = 0
    """Higher = Up, Lower = Down"""

    def __init__(self,
                 screen: pg.surface.Surface,
                 to_point: str = "",
                 back_point: str = ""):
        """
        :param to_point: name of point where player will appear when go to another sect
        :param back_point: name of point where player will appear when comeback from another sect
        """
        self.screen = screen

        self.map = None
        self.areas = []
        self.tilegroup = pg.sprite.Group()
        self.olptiles = pg.sprite.Group()
        self.is_created = False

        self.back_point = back_point
        self.to_point = to_point

    def set_block_size(self, size: int, ori_block_size: int):
        """
        :param size: size to transform
        :param ori_block_size: origin block size (in Tiled)
        """
        self.size = size
        self.ori_block_size = ori_block_size

    def init_OFFSET(self, offset, offsetfullscr):
        if self.screen.get_size() == (800, 800):
            self.CAM_OFFSETX, self.CAM_OFFSETY = offset

        else:
            self.CAM_OFFSETX, self.CAM_OFFSETY = offsetfullscr

    def load(self, path):
        if os.getcwd() == "C:\\Users\\ADMIN\\PycharmProjects\\Nightmare\\src":
            self.map = pytmx.load_pygame(path)

    def get_start_point(self) -> tuple[float, float] | None:
        if self.back_point is None:
            start_area = ""
        else:
            start_area = self.back_point

        has_point = False
        point = 0, 0
        backup_point = 0, 0

        for area in self.areas:
            if area.name == start_area:
                point = area.x, area.y
                has_point = True

            if area.name == "Start":
                backup_point = area.x, area.y

        return point if has_point else backup_point

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

            group = self.olptiles if layer.name == "OverlapPlayer" else self.tilegroup

            tile = Tile(self.screen, surf, pos, layer.name, layer.id, layer.data[y][x], group)

            if "Wall" in layer.name or "Object" in layer.name:
                self.__wall_tile.append(tile)

            self.screen.blit(tile.image, tile.rect)

    def __init_areas(self, layer):
        for area in layer:
            offset = self.size / self.ori_block_size

            pos = pg.math.Vector2(area.x * offset - self.CAM_OFFSETX,
                                  area.y * offset - self.CAM_OFFSETY)

            width = area.width * offset
            height = area.height * offset

            Area(area.name, pos, width, height, self.areas)

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

    def redraw_overlap_tile(self):
        self.olptiles.draw(self.screen)

    def set_opacity(self, alpha: int):
        group = self.tilegroup
        for tile in group:
            tile.image.set_alpha(alpha)


class Map(abc.ABC):
    ori_block_size = 0
    size = 0

    def __init__(self, screen: pg.surface.Surface, path: str):
        self.screen = screen
        self.path = path

        self.sect = None
        self.sections: list[tuple[str, Sect]] = list()

        self.setup_sections()

    @abc.abstractmethod
    def setup_sections(self):
        pass

    @abc.abstractmethod
    def get_next_map(self, area_name):
        pass

    def change_sect(self, name: str):
        is_set = False
        to_point = self.sect.to_point if self.sect is not None else ""

        for section in self.sections:
            if section[0] == name:
                self.sect = section[1]
                is_set = True
                break

        if not is_set:
            return

        self.sect.back_point = to_point
        self.sect.set_block_size(self.size, self.ori_block_size)
