import pygame as pg

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entity.playercontainer.player import Player


class HungryBar(pg.sprite.Sprite):
    def __init__(self, owner: 'Player', groups: pg.sprite.Group):
        super().__init__(groups)
        self.owner = None
        self.image = pg.image.load("../Assets/HUD/Player/hungrybar.png").convert_alpha()
        self.amount = 100

        self.image = pg.transform.scale(self.image, (300, 100))

        self.rect = self.image.get_rect(topleft=(0, 0))

        self.owner = owner

    def __update_health_bar(self):
        self.owner.screen.blit(self.image, self.rect)

        percent = self.amount / 100
        size = self.image.get_size()
        amount_size = size[0] * percent, 30

        amount_surf = pg.surface.Surface(amount_size)
        amount_surf.fill((255, 126, 1))
        amount_surf.set_alpha(self.image.get_alpha())

        amount_rect = amount_surf.get_rect(topleft=(0, 0)).clamp(self.rect)
        self.image.blit(amount_surf, amount_rect)

    def update(self, *args, **kwargs):
        self.image.set_alpha(self.owner.image.get_alpha())
        self.__update_health_bar()
