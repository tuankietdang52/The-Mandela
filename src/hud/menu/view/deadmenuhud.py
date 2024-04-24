import pygame as pg
import src.gamemanage.effect as ge
import src.hud.menu.view.basemenuview as vw

from src.hud.hudcomp import *
from src.hud.menu.contract import *


class DeadMenuHUD(vw.BaseMenuView):
    fontpath = "../Assets/Font/Crang.ttf"

    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen, 2)
        self.choice = -1

        self.setup()

    def setup(self):
        self.__init_elements()

    def get_elements(self) -> list[tuple[pg.surface.Surface, pg.rect.Rect]]:
        return self.elements

    def init_pointer(self):
        width, height = self.screen.get_width(), self.screen.get_height()
        self.presenter.set_pointer_position((width / 2 - 150, height - 270))

    def get_dead_msg(self) -> tuple[pg.surface.Surface, pg.rect.Rect]:
        font = pg.font.Font(self.fontpath, 30)

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
            self.create_txt_element("Respawn", 30, (width / 2, height - 250)),
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
