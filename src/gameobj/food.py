import abc
import pygame as pg
import src.gamemanage.game as gm
import src.mapcontainer.map as mp
import src.gameobj.gameobject as go

from src.tilemap import *
from src.eventhandle.argument import *


class Spam(go.GameObject):
    def __init__(self, pos: pg.math.Vector2, appear_sect: type[mp.Sect]):
        super().__init__(pos, "../Assets/Food/Spam.png", (50, 50), appear_sect)

        self.amount = 30
        self.full_time = 20

    def __is_valid(self) -> bool:
        sect = gm.Manager.get_instance().gamemap.sect
        player = gm.Manager.get_instance().player

        if type(sect) is not self.appear_sect:
            return False

        if not self.area.is_overlap(player.get_rect()):
            return False

        if player.full_time > 0 or player.busy_time > 0:
            return False

        return True

    def player_interact(self, args: EventArgs):
        player = gm.Manager.get_instance().player

        if not self.__is_valid():
            return

        player.increase_hungry_amount(self.amount)
        amount = player.get_hungry_amount()

        if amount >= 100:
            player.set_full_time(self.full_time)

        player.set_busy_time(1)

        self.is_back_up = True
        self.destroy()
