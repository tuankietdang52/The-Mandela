import abc

import pygame as pg
import view.player.playerview as pv
import gamemanage.physic as gp
import mapcontainer.map as mp
import movingtype.movement as mv


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
    def moving(self):
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
