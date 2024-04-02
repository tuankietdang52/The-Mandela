import abc
import heapq

import numpy as np
import pygame as pg

import gamemanage.physic as gp
import mapcontainer.map as mp
import view.player.playerview as pv


class IntVector2:
    def __init__(self, x: int | pg.Vector2, y: int = None):
        if type(x) is pg.Vector2 and y is None:
            self.x, self.y = int(x.x), int(x.y)
            return

        elif y is None:
            raise ValueError("y is None")

        self.x = x
        self.y = y


class Cell:
    def __init__(self, f: float, g: float, h: float, position: IntVector2, parent: IntVector2):
        self.f = f
        self.g = g
        self.h = h

        self.position = position
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __eq__(self, other):
        return self.f == other.f


class Enemy(abc.ABC):
    def __init__(self,
                 screen: pg.Surface,
                 gamemap: mp.Map,
                 sect: type[mp.Sect],
                 image: str,
                 pos: pg.math.Vector2,
                 size: tuple[int, int]):
        self.screen = screen
        self.gamemap = gamemap
        self.sect = sect

        self.image = pg.image.load(image).convert_alpha()
        self.set_size(size)

        self.start_pos = pg.math.Vector2(pos)
        self.position = pg.math.Vector2(pos)

    def set_position(self, pos: tuple[float, float] | pg.math.Vector2):
        if type(pos) is pg.math.Vector2:
            self.position = pos
        else:
            self.position = pg.math.Vector2(pos)

        self.rect = self.image.get_rect(topleft=self.position)

    def get_position(self) -> pg.math.Vector2:
        return self.position

    def set_size(self, size: tuple[int, int]):
        self.image = pg.transform.scale(self.image, size)

    def set_image(self, image: pg.surface.Surface):
        """
        :param image: string: name of image (not path)
        """
        self.image = image

    def get_image(self) -> pg.surface.Surface:
        return self.image

    def get_rect(self) -> pg.rect.Rect:
        return self.image.get_rect(topleft=self.get_position())

    def is_appear(self):
        cur = type(self.gamemap.sect)
        if cur is not self.sect:
            self.set_position(self.start_pos)
            return False

        return True

    @abc.abstractmethod
    def moving(self, velocity: pg.math.Vector2):
        pass

    def can_move(self, pos: pg.math.Vector2):
        rect = self.image.get_rect(topleft=pos)

        if gp.Physic.is_collide_wall(rect):
            return False

        return True

    def check_hit_player(self, rect: pg.rect.Rect):
        player = pv.PlayerView.get_instance()

        if gp.Physic.is_collide(player.get_rect(), rect):
            return True

        return False

    def find_way(self, src: pg.math.Vector2, dest: pg.math.Vector2) -> list:
        src = IntVector2(src)
        dest = IntVector2(dest)

        detail = self.__a_star_search(src, dest)

        if detail is None:
            return [src]

        return self.__trace_path(detail, dest)

    def __trace_path(self, detail: list, dest: IntVector2) -> list:
        path = list()
        x, y = dest.x, dest.y

        while detail[y][x].parent.x != x or detail[y][x].parent.y != y:
            path.append(pg.math.Vector2(x, y))
            tempx, tempy = detail[y][x].parent.x, detail[y][x].parent.y
            x, y = tempx, tempy

        path.reverse()
        return path

    def __a_star_search(self, src: IntVector2, dest: IntVector2):
        col = self.screen.get_width() * 2
        row = self.screen.get_height() * 2

        detail = np.ndarray((row, col), dtype=np.object_)
        closed_list = set()

        start = Cell(0, 0, 0, src, src)
        x, y = int(src.x), int(src.y)
        detail[y][x] = start

        open_list = [start]

        return self.__searching(dest, open_list, detail, closed_list)

    def __searching(self,
                    dest: IntVector2,
                    open_list: list,
                    detail,
                    closed_list: set) -> list | None:

        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        while len(open_list) > 0:
            p = heapq.heappop(open_list)
            cur = p.position
            
            closed_list.add((cur.x, cur.y))

            for di in directions:
                nx_pos = IntVector2(cur.x + di[0], cur.y + di[1])

                if self.__is_in_dest(nx_pos, dest):
                    detail[nx_pos.y][nx_pos.x] = Cell(0, 0, 0, nx_pos, cur)
                    return detail

                if not self.__is_valid(nx_pos) or self.__is_closed(nx_pos, closed_list):
                    continue

                g_new = detail[cur.y][cur.x].g + 1.0
                h_new = self.__get_heuristic(nx_pos, dest)
                f_new = g_new + h_new

                new_cell = Cell(f_new, g_new, h_new, nx_pos, cur)

                if detail[nx_pos.y][nx_pos.x] is None or detail[nx_pos.y][nx_pos.x].f > f_new:
                    heapq.heappush(open_list, new_cell)
                    detail[nx_pos.y][nx_pos.x] = new_cell
                    # pg.draw.circle(self.screen, (0, 0, 150), (nx_pos.x, nx_pos.y), 5)
                    # pg.display.update()

        return None

    def __is_valid(self, cur: IntVector2) -> bool:
        cur = pg.math.Vector2(cur.x, cur.y)
        if self.can_move(cur):
            return True

        return False

    def __is_closed(self, pos: IntVector2, closed_list: set) -> bool:
        if (pos.x, pos.y) in closed_list:
            return True

        return False

    def __is_in_dest(self, cur: IntVector2, dest: IntVector2) -> bool:
        if cur.x == dest.x and cur.y == dest.y:
            return True

        return False

    def __get_heuristic(self, cur: IntVector2, dest: IntVector2) -> float:
        return abs(cur.x - dest.x) + abs(cur.y - dest.y)
