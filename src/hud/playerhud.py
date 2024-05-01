import pygame as pg

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entity.playercontainer.player import Player


class HungryBar(pg.sprite.Sprite):
    def __init__(self, owner: 'Player', groups: pg.sprite.Group):
        super().__init__(groups)
        self.image = pg.surface.Surface((300, 100), pg.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect(topleft=(0, 0))

        self.amount = 100

        self.bar = pg.image.load("../Assets/HUD/Player/hungrybar.png").convert_alpha()
        self.bar = pg.transform.scale(self.bar, (300, 100))

        self.owner = owner

        self.__update_health_bar()

    def __update_health_bar(self):
        self.image.fill((0, 0, 0, 0))

        percent = self.amount / 100
        size = self.image.get_size()

        amount_size = (size[0] * 0.72) * percent, 25
        amount_surf = pg.surface.Surface(amount_size)
        amount_surf.fill((255, 126, 1))
        amount_surf.set_alpha(self.image.get_alpha())

        inside_rect = amount_surf.get_rect(topleft=(0, 0)).clamp(self.rect)
        amount_rect = inside_rect.move(inside_rect.x + 40, inside_rect.y + 35)

        self.image.blit(amount_surf, amount_rect)

        bar_rect = self.bar.get_rect(topleft=(0, 0)).clamp(self.rect)

        self.image.blit(self.bar, bar_rect)

    def decrease_amount(self, amount: float):
        self.amount -= amount

        if self.amount < 0:
            self.amount = 0

    def update(self, *args, **kwargs):
        self.image.set_alpha(self.owner.image.get_alpha())
        self.__update_health_bar()
