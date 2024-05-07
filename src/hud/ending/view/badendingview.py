import pygame as pg
import src.utils.effect as ge
import src.hud.ending.view.baseendingview as vw

from src.hud.menu.contract import *


class BadEnidngHUD(vw.BaseEndingView):
    def __init__(self, screen: pg.surface.Surface, groups: pg.sprite.Group):
        super().__init__(screen, groups)

        self.screen = screen

        self.size = self.screen.get_width(), self.screen.get_height()
        self.pos = self.screen.get_width() / 2, self.screen.get_height() / 2

        self.image = pg.surface.Surface(self.size, pg.SRCALPHA).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(center=self.pos)

        self.setup()

    def setup(self):
        self.__init_elements()
        self.draw()

    def get_elements(self) -> list[tuple[pg.surface.Surface, pg.rect.Rect]]:
        return self.elements

    def __init_elements(self):
        width, height = self.screen.get_width(), self.screen.get_height()

        self.elements.extend([
            self.create_txt_element("Bad Ending",
                                    70,
                                    (255, 0, 0),
                                    (0, 0, 0), (width / 2, height / 2))
        ])

    def get_thanks_surf(self):
        font = pg.font.Font(self.FONTPATH, 30)

        msg_surf = ge.Effect.create_text_outline(font,
                                                 "Thanks for playing",
                                                 (255, 0, 0),
                                                 3,
                                                 (255, 255, 255))

        pos = self.screen.get_width() / 2, self.screen.get_height() / 2

        rect = msg_surf.get_rect(center=pos)

        return msg_surf, rect

    def get_screen(self):
        return self.screen

    def update(self):
        self.is_enter = self.presenter.is_enter()
