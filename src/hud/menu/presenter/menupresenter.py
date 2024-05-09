from src.hud.menu.contract import *


class MenuPresenter(MenuContract.IPresenter):
    def __init__(self, view: MenuContract.IView, model: MenuContract.IModel):
        self.__view = view
        self.__model = model
        self.screen = view.get_screen()
        self.pointer = Pointer(self.screen)
        self.pointer.set_visible(False)

    def get_pointer(self) -> Pointer:
        return self.pointer

    def __get_key(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                return event.key

        return None

    def reset_choice(self):
        self.__model.set_choice(1)

    def selecting(self):
        key = self.__get_key()
        prev_choice = self.__model.get_choice()

        if key == pg.K_RETURN:
            self.pointer.play_choose_sound()
            self.__update_choice()
            return

        if key == pg.K_w:
            self.__model.decrease_choice()
            direction = "up"

        elif key == pg.K_s:
            self.__model.increase_choice()
            direction = "down"

        else:
            return

        choice = self.__model.get_choice()

        if prev_choice == choice:
            return

        self.pointer.play_select_sound()
        self.__move_cur(direction)
        self.__view.draw()

    def __move_cur(self, direction: str):
        pos = self.pointer.get_position()
        if direction == "up":
            new_pos = pos[0], pos[1] - 50
        else:
            new_pos = pos[0], pos[1] + 50

        self.set_pointer_position(new_pos)

    def set_pointer_position(self, pos: tuple[float, float]):
        self.pointer.set_position(pos)
        self.__view.draw()

    def __update_choice(self):
        self.__view.set_choice(self.__model.get_choice())
