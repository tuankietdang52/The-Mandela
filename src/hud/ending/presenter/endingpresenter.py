from src.hud.menu.contract import *


class EndingPresenter(EndingContract.IPresenter):
    def __init__(self, view: EndingContract.IView, model: EndingContract.IModel):
        self.__view = view
        self__model = model
        self.screen = view.get_screen()

    def __get_key(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                return event.key

        return None

    def is_enter(self):
        key = self.__get_key()

        if key == pg.K_RETURN:
            return True

        else:
            return False
