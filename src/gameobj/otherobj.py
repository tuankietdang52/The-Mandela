import abc
import pygame as pg
import src.gamemanage.game as gm
import src.mapcontainer.map as mp
import src.gameobj.gameobject as go

from src.tilemap import *
from src.hud.hudcomp import *
from src.eventhandle.argument import *


class Potion(go.GameObject):
    def __init__(self, pos: pg.math.Vector2, appear_sect: type[mp.Sect]):
        super().__init__(pos, "../Assets/Other/Potion.png", (25, 50), appear_sect)

        self.set_area_size((150, 150))

    def player_interact(self, args: EventArgs):
        sect = self.manager.gamemap.sect
        player = self.manager.player

        if type(sect) is not self.appear_sect:
            return

        if not self.area.is_overlap(player.get_rect()):
            return

        self.manager.player.interact -= self.callback
        self.kill()
        self.manager.update_UI_ip()

        self.manager.is_get_potion = True
        HUDComp.create_board_text("You've pick up the anti-sleep potion")


class BrokenCar(go.GameObject):
    def __init__(self, pos: pg.math.Vector2, appear_sect: type[mp.Sect]):
        super().__init__(pos, "../Assets/Other/brokencar.png", (171, 209), appear_sect)
        self.can_walk_through = False

    def player_interact(self, args: EventArgs):
        pass


class Gas(go.GameObject):
    def __init__(self, pos: pg.math.Vector2, appear_sect: type[mp.Sect]):
        super().__init__(pos, "../Assets/Other/gas.png", (50, 50), appear_sect)

        self.set_area_size((150, 150))

    def player_interact(self, args: EventArgs):
        sect = self.manager.gamemap.sect
        player = self.manager.player

        if type(sect) is not self.appear_sect:
            return

        if not self.area.is_overlap(player.get_rect()):
            return

        self.manager.player.interact -= self.callback
        self.kill()
        self.manager.update_UI_ip()

        self.manager.is_get_gas = True
        HUDComp.create_board_text("You've pick up an empty gas can. You need to fill it")


class GasFill(go.GameObject):
    def __init__(self, pos: pg.math.Vector2, appear_sect: type[mp.Sect]):
        super().__init__(pos, "", (50, 50), appear_sect)

        self.amount = 50
        self.set_area_size((100, 100))

    def player_interact(self, args: EventArgs):
        player = self.manager.player
        sect = self.manager.gamemap.sect

        if type(sect) is not self.appear_sect:
            return

        if not self.area.is_overlap(player):
            return

        self.manager.gas_amount += self.amount

        if self.manager.gas_amount == 50:
            HUDComp.create_board_text("You've refill 1/2 gas tank")
        elif self.manager.gas_amount >= 100:
            HUDComp.create_board_text("You've refill full gas tank")

        self.kill()
        player.interact -= self.callback
