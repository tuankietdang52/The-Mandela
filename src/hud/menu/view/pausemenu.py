import pygame as pg
import src.utils.effect as ge
import src.hud.menu.view.basemenuview as vw

from src.hud.menu.contract import *


class PasueMenuHUD(vw.BaseMenuView):
    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen, 3)

        self.choice = -1

        self.size = self.screen.get_width(), self.screen.get_height()
        self.pos = self.screen.get_width() / 2, self.screen.get_height() / 2

        self.image = pg.surface.Surface(self.size, pg.SRCALPHA).convert_alpha()
        self.image.fill((0, 0, 0, 0))

        self.rect = self.image.get_rect(center=self.pos)

        self.black_surf = pg.surface.Surface(self.size, pg.SRCALPHA)
        self.black_surf.fill((0, 0, 0))
        self.black_surf_rect = self.black_surf.get_rect(topleft=(0, 0))

        self.black_surf.set_alpha(100)
        self.image.blit(self.black_surf, self.black_surf_rect)

        self.setup()

    def get_screen(self):
        return self.screen

    def show(self, groups: pg.sprite.Group):
        groups.add(self)
        groups.add(self.presenter.get_pointer())

        self.choice = -1
        self.presenter.reset_choice()

        self.image.set_alpha(254)
        self.black_surf.set_alpha(100)
        self.init_pointer()
        self.set_alpha_elements(254)
        self.draw()

    def set_alpha_elements(self, alpha: int):
        for ele in self.elements:
            ele[0].set_alpha(alpha)

        self.presenter.get_pointer().image.set_alpha(alpha)

    def setup(self):
        self.__init_elements()
        self.set_alpha_elements(0)
        self.presenter.get_pointer().destroy()

    def init_pointer(self):
        width, height = self.screen.get_width(), self.screen.get_height()
        self.presenter.set_pointer_position((width / 2 - 150, height - 320))
        self.presenter.get_pointer().set_visible(False)

    def set_choice(self, choice: int):
        self.choice = choice

    def get_choice(self) -> int:
        return self.choice

    def get_elements(self) -> list[tuple[pg.surface.Surface, pg.rect.Rect]]:
        return self.elements

    def __init_elements(self):
        width, height = self.screen.get_width(), self.screen.get_height()

        self.elements.extend([
            self.create_txt_element("Pause",
                                    80,
                                    (255, 255, 255),
                                    (255, 0, 0),
                                    (width / 2, 200)),

            self.create_txt_element("Resume",
                                    30,
                                    (255, 255, 255),
                                    (255, 0, 0),
                                    (width / 2, height - 300)),

            self.create_txt_element("To Main Menu",
                                    30,
                                    (255, 255, 255),
                                    (255, 0, 0),
                                    (width / 2, height - 250)),

            self.create_txt_element("Exit Game",
                                    30,
                                    (255, 255, 255),
                                    (255, 0, 0),
                                    (width / 2, height - 200))
        ])

    def update(self):
        self.presenter.selecting()
