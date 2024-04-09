import pygame as pg
import src.gamemanage.effect as ge

from src.hud import Pointer


class StartMenuHUD:
    fontpath = "Assets/Font/Crang.ttf"

    __element = dict()

    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen

        self.pointer = Pointer(self.screen)

        self.init_element()

    def get_start_title(self) -> tuple[pg.surface.Surface, pg.rect.Rect]:
        pos = (self.screen.get_width() / 2, self.screen.get_height() / 2)

        font = pg.font.Font(self.fontpath, 40)
        title = ge.Effect.create_text_outline(font,
                                              "For Python Project",
                                              (255, 255, 255),
                                              3,
                                              (0, 0, 0))

        title_rect = title.get_rect(center=pos)

        return title, title_rect

    def __write_text(self, text: str, size: int) -> pg.Surface:
        font = pg.font.Font(self.fontpath, size)
        text_surf = ge.Effect.create_text_outline(font,
                                                  text,
                                                  (255, 255, 255),
                                                  3,
                                                  (255, 0, 0))

        return text_surf

    def init_txt_element(self, name: str, text: str, size: int, pos: tuple[float, float]):
        elementname = name

        title = self.__write_text(text, size)

        title_rect = title.get_rect(center=pos)

        self.add_element(elementname, (title, title_rect))

    def init_element(self):
        width, height = self.screen.get_width(), self.screen.get_height()

        self.init_txt_element("Title", "NIGHTMARE", 80, (width / 2, 200))

        self.init_txt_element("StartChoice", "Start", 30, (width / 2, height - 250))
        self.init_txt_element("LoadChoice", "Load", 30, (width / 2, height - 200))
        self.init_txt_element("QuitChoice", "Quit", 30, (width / 2, height - 150))

    def add_element(self, name: str, value: tuple[pg.Surface, pg.Rect]):
        dct = {
            name: value
        }

        self.__element.update(dct)

    def get_elements(self) -> dict[str, tuple[pg.surface.Surface, pg.rect.Rect]]:
        return self.__element

    def draw_elements(self):
        for ele in self.__element.values():
            self.screen.blit(ele[0], ele[1])

    def change_choice(self, choice: int):
        width, height = self.screen.get_width(), self.screen.get_height()

        if choice == 1:
            self.pointer.set_position((width / 2 - 100, height - 270))

        elif choice == 2:
            self.pointer.set_position((width / 2 - 100, height - 220))

        elif choice == 3:
            self.pointer.set_position((width / 2 - 100, height - 170))
