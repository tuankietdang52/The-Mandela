import abc
import pygame as pg
import src.gamemanage.game as gm
import src.mapcontainer.map as mp

from src.eventhandle.argument import *
from src.tilemap import *


class Item(pg.sprite.Sprite):
    def __init__(self, pos: pg.math.Vector2, image: str, appear_sect: type[mp.Sect]):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(image).convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=pos)

        self.manager = gm.Manager.get_instance()
        self.appear_sect = appear_sect

        self.area = Area("active", pos, 80, 80)
        self.manager.player.interact += (self.player_interact, EventArgs.empty())

    @abc.abstractmethod
    def player_interact(self, args: EventArgs):
        pass
