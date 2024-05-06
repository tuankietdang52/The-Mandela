import abc
import pygame as pg
import src.gamemanage.game as gm
import src.mapcontainer.map as mp
import src.gameobj.gameobject as go

from src.tilemap import *
from src.eventhandle.argument import *
from src.pjenum.estate import *


class Magazine(go.GameObject):
    def __init__(self, pos: pg.math.Vector2, appear_sect: type[mp.Sect]):
        super().__init__(pos, "../Assets/Magazine/magazine.png", (40, 50), appear_sect)

        self.amount = 10

    def __is_valid(self) -> bool:
        sect = gm.Manager.get_instance().gamemap.sect
        player = gm.Manager.get_instance().player

        if type(sect) is not self.appear_sect:
            return False

        if not self.area.is_overlap(player.get_rect()):
            return False

        if player.get_sanity_amount() >= 100 or player.busy_time > 0:
            return False

        return True

    def player_interact(self, args: EventArgs):
        player = gm.Manager.get_instance().player

        if not self.__is_valid():
            return

        player.increase_sanity_amount(self.amount)
        player.set_busy_time(1)
        self.destroy()
