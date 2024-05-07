import abc
import pygame as pg
import src.gamemanage.game as gm
import src.mapcontainer.map as mp

from src.eventhandle.argument import *
from src.tilemap import *


class GameObject(pg.sprite.Sprite):
    def __init__(self, pos: pg.math.Vector2, image: str, size: tuple[int, int], appear_sect: type[mp.Sect]):
        pg.sprite.Sprite.__init__(self)

        if image != "":
            self.image = pg.image.load(image).convert_alpha()
            self.image = pg.transform.scale(self.image, size)

        else:
            self.image = pg.surface.Surface(size, pg.SRCALPHA)

        self.rect = self.image.get_rect(center=pos)

        self.manager = gm.Manager.get_instance()
        self.appear_sect = appear_sect

        self.area = Area("active", pos, 80, 80)

        self.callback = (self.player_interact, EventArgs.empty())
        self.add_interact()

        self.can_walk_through = True
        self.is_back_up = False

    def re_setup(self):
        self.add_interact()
        self.is_back_up = False

    def set_position(self, pos: pg.math.Vector2):
        self.rect = self.image.get_rect(center=pos)

    def get_position(self) -> pg.math.Vector2:
        return pg.math.Vector2(self.rect.center)

    def add_interact(self):
        if not self.manager.player.alive():
            return

        self.manager.player.interact += self.callback

    def set_area_size(self, size: tuple[int, int]):
        self.area.set_size(size)

    @abc.abstractmethod
    def player_interact(self, args: EventArgs):
        pass

    def destroy(self):
        self.manager.player.interact -= self.callback
        self.kill()

        if not self.is_back_up:
            return

        back_up = self.manager.gameprogress.spawn_manager.game_objects_backup
        back_up.add(self)
