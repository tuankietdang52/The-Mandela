import heapq
import pygame as pg
import numpy as np
import src.entity.thealternate.enemy as enenemy
import src.movingtype.movement as mv
import src.gamemanage.game as gm

from src.utils import *


class Cell:
    def __init__(self, f: float, g: float, h: float, position: mv.IntVector2, parent: mv.IntVector2):
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


class NormalMovement(mv.Movement):
    def __init__(self, enemy: enenemy.Enemy):
        self.owner = enemy
        self.manager = gm.Manager.get_instance()
        self.player = self.manager.player

    def moving(self):
        rect = self.owner.get_rect()
        player_rect = self.player.get_rect()

        if Physic.is_collide(player_rect, rect):
            return

        self.__chasing_player()

    __ways = list()

    def __chasing_player(self):
        player_position = self.player.get_position()
        src = self.owner.get_position()
        dest = player_position

        speed = self.owner.get_speed()
        position = src

        for step in range(int(speed) + 1):
            if len(self.__ways) == 0:
                break

            position = self.__ways.pop(0)
            self.owner.calculate_direction(position)

        self.owner.set_position(position)
        self.__ways = self.__find_way(self.owner.get_position(), dest)

        if len(self.__ways) == 0:
            self.__approach_player()

    def __approach_player(self):
        player_position = self.player.get_position()

        direction = self.owner.calculate_direction(player_position)
        velocity = direction * self.owner.get_speed()

        next_position = self.owner.get_position() + velocity

        self.owner.set_position(next_position)

    # A STAR PATHFINDING

    def __check_valid_dest(self, dest: pg.math.Vector2):
        if self.owner.can_move(dest):
            return True

        return False

    def __find__valid_dest(self, dest: pg.math.Vector2) -> pg.math.Vector2:
        left, right = dest.x, dest.x
        up, down = dest.y, dest.y

        while True:
            left -= 1
            right += 1
            up -= 1
            down += 1

            if self.owner.can_move(pg.math.Vector2(left, dest.y)):
                return pg.math.Vector2(left, dest.y)
            elif self.owner.can_move(pg.math.Vector2(right, dest.y)):
                return pg.math.Vector2(right, dest.y)
            elif self.owner.can_move(pg.math.Vector2(dest.x, up)):
                return pg.math.Vector2(dest.x, up)
            elif self.owner.can_move(pg.math.Vector2(dest.x, down)):
                return pg.math.Vector2(dest.x, down)

    def __find_way(self, src: pg.math.Vector2, dest: pg.math.Vector2) -> list:
        src_int = mv.IntVector2(round(src.x / 32), round(src.y / 32))

        if not self.__check_valid_dest(dest):
            dest = self.__find__valid_dest(dest)

        dest_int = mv.IntVector2(round(dest.x / 32), round(dest.y / 32))

        detail = self.__a_star_search(src_int, dest_int)

        if detail is None:
            return [src]

        return self.__trace_path(detail, dest_int)

    def __trace_path(self, detail: list, dest: mv.IntVector2) -> list:
        path = list()
        x, y = dest.x, dest.y

        while detail[y][x].parent.x != x or detail[y][x].parent.y != y:
            path.append(pg.math.Vector2(x, y))
            tempx, tempy = detail[y][x].parent.x, detail[y][x].parent.y
            x, y = tempx, tempy

        path.reverse()

        real_path = self.__make_real_path(path)

        # for i in real_path:
        #     pg.draw.circle(self.manager.screen, (255, 0, 0), (i.x, i.y), 5)
        #     pg.display.update()

        # self.manager.wait(0.5)

        return real_path

    def __make_real_path(self, path: list[pg.math.Vector2]) -> list[pg.math.Vector2]:
        real_path = []
        for i in range(len(path) - 1):
            direction = (path[i + 1] - path[i])
            [x, y] = path[i]
            [real_path.append(
                pg.math.Vector2(x * 32 + j * direction.x, y * 32 + j * direction.y))
                for j in range(32)]

        if len(real_path) == 0:
            return real_path

        real_path.reverse()
        real_path = self.__connect_to_src(real_path)
        real_path.reverse()

        return real_path

    def __connect_to_src(self, real_path: list[pg.math.Vector2]) -> list[pg.math.Vector2]:
        cur = pg.math.Vector2(real_path[len(real_path) - 1])
        src = self.owner.get_position()
        src = pg.math.Vector2(round(src.x), round(src.y))

        while cur != src:
            direction = (src - cur).normalize()
            direction = pg.math.Vector2(round(direction.x), round(direction.y))

            next_pos = pg.math.Vector2(cur.x + direction.x, cur.y + direction.y)
            real_path.append(next_pos)
            cur = next_pos

        return real_path

    def __a_star_search(self, src: mv.IntVector2, dest: mv.IntVector2):
        screen = self.manager.screen

        col = round(screen.get_width() / 32)
        row = round(screen.get_height() / 32)

        detail = np.ndarray((row, col), dtype=np.object_)
        closed_list = set()

        start = Cell(0, 0, 0, src, src)
        x, y = src.x, src.y
        detail[y][x] = start

        open_list = [start]

        res = self.__searching(dest, open_list, detail, closed_list)
        return res

    def __searching(self,
                    dest: mv.IntVector2,
                    open_list: list,
                    detail,
                    closed_list: set) -> list | None:

        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        while len(open_list) > 0:
            p = heapq.heappop(open_list)
            cur = p.position

            closed_list.add((cur.x, cur.y))

            for di in directions:
                nx_pos = mv.IntVector2(cur.x + di[0], cur.y + di[1])

                if self.__is_in_dest(nx_pos, dest):
                    detail[nx_pos.y][nx_pos.x] = Cell(0, 0, 0, nx_pos, cur)
                    return detail

                if not self.__is_valid(nx_pos) or self.__is_closed(nx_pos, closed_list):
                    continue

                g_new = detail[cur.y][cur.x].g + 1.0
                h_new = self.__get_heuristic(nx_pos, dest)
                f_new = g_new + h_new

                new_cell = Cell(f_new, g_new, h_new, nx_pos, cur)

                if (nx_pos.x >= len(detail)
                        or nx_pos.x < 0
                        or nx_pos.y >= len(detail)
                        or nx_pos.y < 0):
                    continue

                if detail[nx_pos.y][nx_pos.x] is None or detail[nx_pos.y][nx_pos.x].f > f_new:
                    heapq.heappush(open_list, new_cell)
                    detail[nx_pos.y][nx_pos.x] = new_cell

        return None

    def __is_valid(self, cur: mv.IntVector2) -> bool:
        rect = self.owner.get_image().get_rect(center=(cur.x * 32, cur.y * 32))

        if Physic.is_collide_wall(rect):
            return False

        return True

    def __is_closed(self, pos: mv.IntVector2, closed_list: set) -> bool:
        if (pos.x, pos.y) in closed_list:
            return True

        return False

    def __is_in_dest(self, cur: mv.IntVector2, dest: mv.IntVector2) -> bool:
        if cur.x == dest.x and cur.y == dest.y:
            return True

        return False

    def __get_heuristic(self, cur: mv.IntVector2, dest: mv.IntVector2) -> float:
        return abs(cur.x - dest.x) + abs(cur.y - dest.y)