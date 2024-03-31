import abc
import heapq
import math

import numpy
import pygame

import gamemanage.game
import gamemanage.physic
import mapcontainer.map
import view.playerview


class Pair:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __lt__(self, other):
        pass

    def __eq__(self, other):
        pass


class Cell:
    def __init__(self, f: float, g: float, h: float, position: Pair, parent: Pair):
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


class Enemy(pygame.sprite.Sprite, abc.ABC):
    __path = "Assets/Enemy/"

    def __init__(self,
                 screen: pygame.Surface,
                 gamemap: mapcontainer.map.Map,
                 sect: type[mapcontainer.map.Sect],
                 image: str,
                 pos: tuple[float, float],
                 size: tuple[float, float]):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.gamemap = gamemap
        self.sect = sect

        self.image = pygame.image.load(self.__path + image).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect(topleft=pos)
        self.start_pos = pos

    def is_appear(self):
        cur = type(self.gamemap.sect)
        if cur is not self.sect:
            self.rect = self.image.get_rect(topleft=self.start_pos)
            return False

        return True

    @abc.abstractmethod
    def chase_player(self):
        pass

    def can_move(self, pos):
        rect = self.image.get_rect(topleft=pos)

        if self.check_hit_player():
            return False

        if gamemanage.physic.Physic.is_collide_wall(rect):
            return False

        return True

    def check_hit_player(self):
        center = self.rect.center
        botlf = self.rect.bottomleft
        botrg = self.rect.bottomright

        player = view.playerview.PlayerView.get_instance()

        if (player.get_rect().collidepoint(center)
                or player.get_rect().collidepoint(botlf)
                or player.get_rect().collidepoint(botrg)):
            return True

        return False

    def find_way(self, src: tuple[int, int], dest: tuple[int, int]) -> list:
        if src[0] == dest[0] and src[1] == dest[1]:
            return [Pair(src[0], src[1])]

        detail = self.__a_star_search(src, dest)

        if detail is None:
            return [Pair(src[0], src[1])]

        return self.__trace_path(detail, dest)

    def __trace_path(self, detail: list, dest: tuple[float, float]) -> list:
        path = list()
        x, y = dest[0], dest[1]

        while detail[y][x].parent.x != x or detail[y][x].parent.y != y:
            path.append(Pair(x, y))
            tempx, tempy = detail[y][x].parent.x, detail[y][x].parent.y
            x, y = tempx, tempy

        path.reverse()
        return path

    def __a_star_search(self, src: tuple[int, int], dest: tuple[int, int]):
        col = self.screen.get_width() * 2
        row = self.screen.get_height() * 2

        detail = numpy.ndarray((row, col), dtype=numpy.object_)

        closed_list = set()

        x, y = src[0], src[1]
        pair = Pair(x, y)

        start = Cell(0, 0, 0, pair, pair)
        detail[y][x] = start

        open_list = [start]

        dest = Pair(dest[0], dest[1])

        return self.__searching(dest, open_list, detail, closed_list)

    def __searching(self,
                    dest: Pair,
                    open_list: list,
                    detail,
                    closed_list: set) -> list | None:

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        while len(open_list) > 0:
            p = heapq.heappop(open_list)
            cur = Pair(p.position.x, p.position.y)

            closed_list.add((cur.x, cur.y))

            for di in directions:
                nx_pos = Pair(cur.x + di[0], cur.y + di[1])

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
                    pygame.draw.circle(self.screen, (0, 0, 150), (nx_pos.x, nx_pos.y), 5)
                    pygame.display.update()

        return None

    def __is_valid(self, cur: Pair) -> bool:
        if self.can_move((cur.x, cur.y)):
            return True

        return False

    def __is_closed(self, pos: Pair, closed_list: set) -> bool:
        if (pos.x, pos.y) in closed_list:
            return True

        return False

    def __is_in_dest(self, cur: Pair, dest: Pair) -> bool:
        if cur.x == dest.x and cur.y == dest.y:
            return True

        return False

    def __get_heuristic(self, cur: Pair, dest: Pair) -> float:
        return math.sqrt(math.pow(cur.x - dest.x, 2) + math.pow(cur.y - dest.y, 2))
