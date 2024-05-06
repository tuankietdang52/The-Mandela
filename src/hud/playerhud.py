import pygame as pg
import src.gamemanage.game as gm

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entity.playercontainer.player import Player


class Bar(pg.sprite.Sprite):
    def __init__(self,
                 bartype: str,
                 pos: pg.math.Vector2,
                 amount_bar_color: tuple[int, int, int],
                 owner: 'Player',
                 groups: pg.sprite.Group):
        """
        :param bartype: name of an image (not include bar.png)
        """

        super().__init__(groups)
        self.image = pg.surface.Surface((300, 100), pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)

        self.amount = 100
        self.color = amount_bar_color

        self.bar = pg.image.load(f"../Assets/HUD/Player/{bartype}bar.png").convert_alpha()
        self.bar = pg.transform.scale(self.bar, (200, 50))

        size = self.image.get_size()
        amount_size = size[0] * 0.8, 20
        self.amount_surf = pg.surface.Surface(amount_size)
        self.amount_surf.fill(self.color)

        self.owner = owner

        self.__update_health_bar()

    def set_visible(self, is_visible: bool):
        if not is_visible:
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(254)

    def __update_health_bar(self):
        self.image.fill((0, 0, 0, 0))

        percent = self.amount / 100
        size = self.image.get_size()

        amount_size = (size[0] * 0.57) * percent, 20

        self.amount_surf = pg.transform.scale(self.amount_surf, amount_size)

        amount_rect = self.amount_surf.get_rect(topleft=(0, 0))
        amount_rect = amount_rect.move(22, 16)

        self.image.blit(self.amount_surf, amount_rect)
        bar_rect = self.bar.get_rect(topleft=(0, 0))

        self.image.blit(self.bar, bar_rect)

    def increase_amount(self, amount: float):
        self.amount += amount

        if self.amount > 100:
            self.amount = 100

    def decrease_amount(self, amount: float):
        self.amount -= amount

        if self.amount < 0:
            self.amount = 0

    def get_amount(self) -> float:
        return self.amount

    def update(self, *args, **kwargs):
        self.amount_surf.fill(self.color)
        self.__update_health_bar()
