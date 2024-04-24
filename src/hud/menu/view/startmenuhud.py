import src.gamemanage.effect as ge
import src.hud.menu.view.basemenuview as vw

from src.hud.menu.contract import *


class StartMenuHUD(vw.BaseMenuView):
    fontpath = "../Assets/Font/Crang.ttf"

    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen, 3)

        self.__sponsor_list: list[tuple[pg.surface.Surface, pg.rect.Rect]] = []

        self.choice = -1
        self.setup()

    def get_screen(self):
        return self.screen

    def setup(self):
        self.__setup_list_sponsor()
        self.__init_elements()

    def init_pointer(self):
        width, height = self.screen.get_width(), self.screen.get_height()
        self.presenter.set_pointer_position((width / 2 - 100, height - 270))

    def set_choice(self, choice: int):
        self.choice = choice

    def get_choice(self) -> int:
        return self.choice

    def __setup_list_sponsor(self):
        self.__sponsor_list.extend([
            self.create_for_python_project(),
        ])

    def get_sponsor_list(self) -> list[tuple[pg.surface.Surface, pg.rect.Rect]]:
        return self.__sponsor_list

    def get_elements(self) -> list[tuple[pg.surface.Surface, pg.rect.Rect]]:
        return self.elements

    def create_for_python_project(self) -> tuple[pg.surface.Surface, pg.rect.Rect]:
        pos = (self.screen.get_width() / 2, self.screen.get_height() / 2)

        font = pg.font.Font(self.fontpath, 40)
        title = ge.Effect.create_text_outline(font,
                                              "For Python Project",
                                              (255, 255, 255),
                                              3,
                                              (0, 0, 0))

        title_rect = title.get_rect(center=pos)
        return title, title_rect

    def draw_sponsor(self, index: int):
        self.screen.blit(self.__sponsor_list[index][0], self.__sponsor_list[index][1])

    def __init_elements(self):
        width, height = self.screen.get_width(), self.screen.get_height()

        self.elements.extend([
            self.create_txt_element("NIGHTMARE", 80, (width / 2, 200)),
            self.create_txt_element("Start", 30, (width / 2, height - 250)),
            self.create_txt_element("Load", 30, (width / 2, height - 200)),
            self.create_txt_element("Quit", 30, (width / 2, height - 150))
        ])

    def update(self):
        self.presenter.selecting()
