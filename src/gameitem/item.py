import abc
import pygame as pg
import src.gamemanage.game as gm
import src.mapcontainer.map as mp

from src.eventhandle.argument import *
from src.tilemap import *


class Item(pg.sprite.Sprite):
    def __init__(self, pos: pg.math.Vector2, image: str, size: tuple[int, int], appear_sect: type[mp.Sect]):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(image).convert_alpha()
        self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=pos)

        self.manager = gm.Manager.get_instance()
        self.appear_sect = appear_sect

        self.area = Area("active", pos, 80, 80)

        self.callback = (self.player_interact, EventArgs.empty())
        self.manager.player.interact += self.callback

    @abc.abstractmethod
    def player_interact(self, args: EventArgs):
        pass

    def destroy(self):
        self.manager.player.interact -= self.callback
        self.kill()
