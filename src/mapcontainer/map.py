import abc
import os
import pytmx
import pygame as pg

from src.tilemap import *
from src.pjenum import *
from pathlib import Path


class Sect:

    MAP_OFFSETX = 0
    """Higher = Left, Lower = Right"""

    MAP_OFFSETY = 0
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
        self.points = []
        self.tilegroup = pg.sprite.Group()
        self.olptiles = pg.sprite.Group()

        self.__walls_tile = list()
        self.walls = set()

        self.is_created = False
        self.spawn_area_count = 0

        self.ori_block_size = 16
        self.size = 64

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
        if not gm.Game.IS_FULLSCREEN:
            self.MAP_OFFSETX, self.MAP_OFFSETY = offset

        else:
            self.MAP_OFFSETX, self.MAP_OFFSETY = offsetfullscr

    def get_map_OFFSET(self) -> tuple[int, int]:
        return self.MAP_OFFSETX, self.MAP_OFFSETY

    def load(self, path):
        file_path = Path(__file__)
        src_path = file_path.parent.parent
        if Path(os.getcwd()) == src_path:
            self.map = pytmx.load_pygame(path)
        else:
            raise EnvironmentError("Script must start in src directory")

    def get_start_point(self) -> pg.math.Vector2 | None:
        if self.back_point is None:
            start_area = ""
        else:
            start_area = self.back_point

        backup_point = 0, 0

        for point in self.points:
            if point.name == start_area:
                return pg.math.Vector2(point.x, point.y)

            elif point.name == "Start":
                backup_point = pg.math.Vector2(point.x, point.y)

        return backup_point

    def create(self):
        self.areas.clear()
        self.points.clear()
        self.tilegroup.empty()
        self.walls.clear()

        self.is_created = True

        for layer in self.map.layers:
            if hasattr(layer, "data"):
                self.__draw_tile(layer)

            if isinstance(layer, pytmx.TiledObjectGroup):
                if "Area" in layer.name:
                    self.__init_areas(layer)
                elif layer.name == "Points":
                    self.__init_points(layer)

        self.__init_walls()

    def __draw_tile(self, layer):
        for x, y, surf in layer.tiles():
            pos = x * self.size - self.MAP_OFFSETX, y * self.size - self.MAP_OFFSETY

            tilesize = self.size, self.size

            surf = pg.transform.scale(surf, tilesize)

            group = self.olptiles if layer.name == "OverlapPlayer" else self.tilegroup

            tilemp = Tile(self.screen, surf, pos, layer.name, layer.id, layer.data[y][x], group)

            if "Wall" in layer.name or "Object" in layer.name:
                self.__walls_tile.append(tilemp)

            self.screen.blit(tilemp.image, tilemp.rect)

    def __init_areas(self, layer):
        self.spawn_area_count = 0
        for area in layer:
            offset = self.size / self.ori_block_size

            pos = pg.math.Vector2(area.x * offset - self.MAP_OFFSETX,
                                  area.y * offset - self.MAP_OFFSETY)

            width = area.width * offset
            height = area.height * offset

            Area(area.name, pos, width, height, EPosition.TOPLEFT, self.areas)

            if "SpawnArea" in area.name:
                self.spawn_area_count += 1

    def __init_points(self, layer):
        for item in layer:
            offset = self.size / self.ori_block_size

            x = item.x * offset - self.MAP_OFFSETX
            y = item.y * offset - self.MAP_OFFSETY

            point = Point(item.name, x, y)

            self.points.append(point)

    def __init_walls(self):
        for wall in self.__walls_tile:
            left_x, top_y = wall.rect.topleft
            width = wall.rect.width
            height = wall.rect.height

            right_x = left_x + width
            bot_y = top_y + height

            for y in range(top_y, bot_y):
                for x in range(left_x, right_x):
                    self.walls.add((x, y))
                    self.walls.add((x, y))

        self.__walls_tile.clear()

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

    def get_point(self, name):
        for point in self.points:
            if point.name == name:
                return point

        return None

    def redraw(self):
        group = self.tilegroup
        group.draw(self.screen)

    def redraw_overlap_tile(self):
        self.olptiles.draw(self.screen)

    def set_opacity(self, alpha: int):
        for tilemp in self.tilegroup:
            tilemp.image.set_alpha(alpha)

        for olptile in self.olptiles:
            olptile.image.set_alpha(alpha)


class Map(abc.ABC):
    def __init__(self, screen: pg.surface.Surface, path: str):
        self.screen = screen
        self.path = path

        self.sect = None
        self.sections: list[tuple[str, Sect]] = list()

        self.ori_block_size = 16
        self.size = 64

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
