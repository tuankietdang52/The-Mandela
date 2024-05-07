import src.utils.effect as ge
import src.hud.ending.presenter.endingpresenter as edpr
import src.hud.ending.model.endingmodel as edm

from src.hud.menu.contract import *


class BaseEndingView(EndingContract.IView, pg.sprite.Sprite):
    FONTPATH = "../Assets/Font/Crang.ttf"

    def __init__(self, screen, groups: pg.sprite.Group):
        super().__init__(groups)

        self.image = None
        self.rect = None

        self.is_enter = False

        self.screen = screen
        self.presenter = edpr.EndingPresenter(self, edm.EndingModel())
        self.elements: list[tuple[pg.surface.Surface, pg.rect.Rect]] = list()

    def __write_text(self,
                     text: str,
                     size: int,
                     color: tuple[int, int, int],
                     outline_color: tuple[int, int, int]) -> pg.surface.Surface:
        font = pg.font.Font(self.FONTPATH, size)
        text_surf = ge.Effect.create_text_outline(font,
                                                  text,
                                                  color,
                                                  3,
                                                  outline_color)

        return text_surf

    def create_txt_element(self,
                           text: str,
                           size: int,
                           color: tuple[int, int, int],
                           outline_color: tuple[int, int, int],
                           pos: tuple[float, float]) -> tuple[pg.surface.Surface, pg.rect.Rect]:
        title = self.__write_text(text, size, color, outline_color)

        title_rect = title.get_rect(center=pos)
        return title, title_rect

    def update(self):
        pass

    def setup(self):
        pass

    def get_elements(self):
        pass

    def get_screen(self):
        pass

    def __init_elements(self):
        pass

    def __draw_elements(self):
        for item in self.elements:
            self.image.blit(item[0], item[1])

    def draw(self):
        self.__draw_elements()

    def destroy(self):
        self.kill()
