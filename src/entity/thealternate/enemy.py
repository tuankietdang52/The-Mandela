import abc

import pygame as pg
import src.gamemanage.physic as gph
import src.movingtype.movement as mv
import src.mapcontainer.map as mp
import src.gamemanage.game as gm


class Enemy(abc.ABC):
    def __init__(self,
                 gamemap: mp.Map,
                 mapmapsect: type[mp.Sect],
                 image: str,
                 pos: pg.math.Vector2,
                 size: tuple[int, int]):
        self.gamemap = gamemap
        self.mapsect = mapmapsect

        self.image = pg.image.load(image).convert_alpha()
        self.set_size(size)
        self.rect = self.image.get_rect()

        self.start_pos = pg.math.Vector2(pos)
        self.position = pg.math.Vector2(pos)

        self.speed = 1
        self.movement = mv.Movement()

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
        self.image = image

    def get_image(self) -> pg.surface.Surface:
        return self.image

    def get_rect(self) -> pg.rect.Rect:
        return self.image.get_rect(topleft=self.get_position())

    def set_speed(self, speed: int):
        self.speed = speed

    def get_speed(self) -> int:
        return self.speed

    def is_appear(self):
        cur = type(self.gamemap.sect)
        if cur is not self.mapsect:
            self.set_position(self.start_pos)
            return False

        return True

    @abc.abstractmethod
    def moving(self):
        pass

    def can_move(self, pos: pg.math.Vector2):
        rect = self.image.get_rect(topleft=pos)

        if gph.Physic.is_collide_wall(rect):
            return False

        return True

    def is_hit_player(self) -> bool:
        player = gm.Manager.get_instance().player

        rect = self.rect
        player_rect = player.get_rect()

        if gph.Physic.is_collide(player_rect, rect):
            return True

        return False
