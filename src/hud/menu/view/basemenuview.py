import src.gamemanage.effect as ge
import src.hud.menu.presenter.menupresenter as smpr
import src.hud.menu.model.menumodel as smm


from src.hud.menu.contract import *


class BaseMenuView(MenuContract.IView):
    fontpath = "../Assets/Font/Crang.ttf"

    def __init__(self, screen, max_choice: int):
        self.screen = screen
        self.presenter = smpr.MenuPresenter(self, smm.MenuModel(max_choice))
        self.elements: list[tuple[pg.surface.Surface, pg.rect.Rect]] = list()

    def __write_text(self, text: str, size: int) -> pg.surface.Surface:
        font = pg.font.Font(self.fontpath, size)
        text_surf = ge.Effect.create_text_outline(font,
                                                  text,
                                                  (255, 255, 255),
                                                  3,
                                                  (255, 0, 0))

        return text_surf

    def create_txt_element(self,
                           text: str,
                           size: int,
                           pos: tuple[float, float]) -> tuple[pg.surface.Surface, pg.rect.Rect]:
        title = self.__write_text(text, size)

        title_rect = title.get_rect(center=pos)

        self.screen.blit(title, title_rect)

        return title, title_rect

    def setup(self):
        pass

    def get_elements(self):
        pass

    def get_screen(self):
        pass

    def set_choice(self, choice: int):
        pass

    def get_choice(self) -> int:
        pass

    def __init_elements(self):
        pass

    def __draw_elements(self):
        for item in self.elements:
            self.screen.blit(item[0], item[1])

    def draw(self):
        gm.Manager.get_instance().update_UI()

        self.__draw_elements()
        pointer = self.presenter.get_pointer()
        pointer.draw()

        pg.display.update()
