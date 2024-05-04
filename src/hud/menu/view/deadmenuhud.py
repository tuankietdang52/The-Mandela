import pygame as pg
import src.utils.effect as ge
import src.hud.menu.view.basemenuview as vw

from src.hud.menu.contract import *


class DeadMenuHUD(vw.BaseMenuView):
    def __init__(self, screen: pg.surface.Surface, groups: pg.sprite.Group):
        super().__init__(screen, 2, groups)
        self.choice = -1

        self.size = self.screen.get_width(), self.screen.get_height()
        self.pos = self.screen.get_width() / 2, self.screen.get_height() / 2

        self.image = pg.surface.Surface(self.size, pg.SRCALPHA).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(center=self.pos)

        self.setup()

    def setup(self):
        self.__init_elements()

    def get_elements(self) -> list[tuple[pg.surface.Surface, pg.rect.Rect]]:
        return self.elements

    def init_pointer(self):
        width, height = self.screen.get_width(), self.screen.get_height()
        self.presenter.set_pointer_position((width / 2 - 150, height - 270))
        self.presenter.get_pointer().set_visible(True)

    def get_dead_msg(self) -> tuple[pg.surface.Surface, pg.rect.Rect]:
        font = pg.font.Font(self.FONTPATH, 30)

        msg_surf = ge.Effect.create_text_outline(font,
                                                 "uh oh bad decision viole...",
                                                 (255, 0, 0),
                                                 3,
                                                 (255, 255, 255))

        pos = self.screen.get_width() / 2, self.screen.get_height() / 2 - 200

        rect = msg_surf.get_rect(center=pos)

        return msg_surf, rect

    def __init_elements(self):
        width, height = self.screen.get_width(), self.screen.get_height()

        self.elements.extend([
            self.create_txt_element("You Died", 70, (width / 2, 200)),
            self.create_txt_element("Replay", 30, (width / 2, height - 250)),
            self.create_txt_element("Exit To Menu", 30, (width / 2, height - 200)),
        ])

    def get_screen(self):
        return self.screen

    def set_choice(self, choice: int):
        self.choice = choice

    def get_choice(self) -> int:
        return self.choice

    def update(self):
        self.presenter.selecting()
