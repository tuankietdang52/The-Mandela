import abc
import pygame as pg
import src.gamemanage.game as gm
import src.mapcontainer.map as mp
import src.gameitem.item as gi

from src.tilemap import *
from src.eventhandle.argument import *


class Spam(gi.Item):
    def __init__(self, pos: pg.math.Vector2, appear_sect: type[mp.Sect]):
        super().__init__(pos, "../Assets/Food/Spam.png", appear_sect)

        self.full_amount = 10
        self.full_time = 10

    def player_interact(self, args: EventArgs):
        player = gm.Manager.get_instance().player

        if not self.area.is_overlap(player.get_rect()):
            return

        if player.full_time > 0:
            return

        player.set_full_time(self.full_time)
        player.increase_hungry_amount(self.full_amount)
        self.kill()
        self.manager.update_UI_ip()
