import abc
import pygame as pg
import src.gamemanage.game as gm
import src.mapcontainer.map as mp
import src.gameobj.gameobject as go

from src.tilemap import *
from src.hud.hudcomp import *
from src.eventhandle.argument import *


class Arrow(go.GameObject):
    def __init__(self, pos: pg.math.Vector2, appear_sect: type[mp.Sect]):
        super().__init__(pos, "../Assets/Map/pointer.png", (32, 64), appear_sect)

        self.manager.player.interact -= self.callback

    def player_interact(self, args: EventArgs):
        pass


class Potion(go.GameObject):
    def __init__(self, pos: pg.math.Vector2, appear_sect: type[mp.Sect]):
        super().__init__(pos, "../Assets/Other/Potion.png", (25, 50), appear_sect)

        self.set_area_size((150, 150))

    def player_interact(self, args: EventArgs):
        sect = self.manager.gamemap.sect
        player = self.manager.player

        night = self.manager.game_night

        if type(sect) is not self.appear_sect:
            return

        if not self.area.is_overlap(player.get_rect()):
            return

        if night != 2:
            self.is_back_up = True

        self.destroy()
        self.manager.update_UI_ip()

        self.manager.progress_status.is_get_potion = True
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

        self.destroy()
        self.manager.update_UI_ip()

        self.manager.progress_status.is_get_gas = True
        HUDComp.create_board_text("You've pick up an empty gas can. You need to fill it")


class GasFill(go.GameObject):
    def __init__(self, pos: pg.math.Vector2, appear_sect: type[mp.Sect]):
        super().__init__(pos, "", (50, 50), appear_sect)

        self.amount = 50
        self.set_area_size((100, 100))

    def player_interact(self, args: EventArgs):
        player = self.manager.player
        sect = self.manager.gamemap.sect

        if not self.manager.progress_status.is_get_gas:
            return

        if type(sect) is not self.appear_sect:
            return

        if not self.area.is_overlap(player):
            return

        gas_amount = self.manager.progress_status.gas_amount
        gas_amount += self.amount

        if gas_amount == 50:
            HUDComp.create_board_text("You've refill 1/2 gas tank")
        elif gas_amount >= 100:
            HUDComp.create_board_text("You've refill full gas tank")

        self.manager.progress_status.gas_amount = gas_amount
        self.destroy()


class Shovel(go.GameObject):
    def __init__(self, pos: pg.math.Vector2, appear_sect: type[mp.Sect]):
        super().__init__(pos, "../Assets/Other/shovel.png", (108, 24), appear_sect)

        self.amount = 50
        self.set_area_size((100, 100))

    def player_interact(self, args: EventArgs):
        night = self.manager.game_night

        if night != 3:
            return

        sect = self.manager.gamemap.sect

        if type(sect) is not self.appear_sect:
            return

        player = self.manager.player
        if not self.area.is_overlap(player):
            return

        HUDComp.create_board_text("You've pick up a shovel")
        self.manager.progress_status.is_get_shovel = True

        self.is_back_up = True
        self.destroy()


class PoliceCar(go.GameObject):
    def __init__(self, pos: pg.math.Vector2, appear_sect: type[mp.Sect]):
        super().__init__(pos, "../Assets/Ally/Cop/policecar.png", (190, 95), appear_sect)
        self.can_walk_through = False

        self.set_area_size((181, 219))

    def update(self, *args, **kwargs):
        if not self.manager.progress_status.get_in_car:
            return

        position = self.get_position()
        self.set_position(pg.math.Vector2(position.x + 10, position.y))

    def player_interact(self, args: EventArgs):
        sect = self.manager.gamemap.sect

        if type(sect) is not self.appear_sect:
            return

        player = self.manager.player

        if not self.area.is_overlap(player.get_rect()):
            return

        if not self.manager.progress_status.can_get_in_car:
            return

        self.manager.progress_status.get_in_car = True


class PoiceCarFront(go.GameObject):
    def __init__(self, pos: pg.math.Vector2, appear_sect: type[mp.Sect]):
        super().__init__(pos, "../Assets/Ally/Cop/policecarfront.png", (308, 112), appear_sect)

        self.image = pg.transform.flip(self.image, True, False)

    def update(self, *args, **kwargs):
        position = self.get_position()
        self.set_position(pg.math.Vector2(position.x + 2, position.y))

    def player_interact(self, args: EventArgs):
        pass
