import sys
import pygame as pg
import src.gameprogress.part as gp
import src.gamemanage.effect as ge
import src.hud.menu.view.deadmenuhud as dm
import src.gamemanage.game as gm


class DeadMenu(gp.Part):
    def __init__(self, screen: pg.surface.Surface, current_part: gp.Part):
        super().__init__(screen)

        self.dead_menu = dm.DeadMenuHUD(self.screen)
        self.current_part = current_part

        self.setup()

    def setup(self):
        self.enemies.clear()
        self.update_list_entities()

    def event_action(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

    def pressing_key(self):
        if not self.can_press_key:
            return

        keys = pg.key.get_pressed()

    def update(self):
        if self.get_progress_index() != 2:
            super().update()
        else:
            self.manage_progress()

    def manage_progress(self):
        progress = self.get_progress_index()

        if progress == 0:
            self.__show_dead_msg()
            self.next()

        elif progress == 1:
            self.__draw_dead_menu()
            self.next()

        elif progress == 2:
            self.__check_choice()

    def __show_dead_msg(self):
        ge.Effect.fade_out_screen(False)
        msg = self.dead_menu.get_dead_msg()

        self.screen.blit(msg[0], msg[1])
        pg.display.update()

        gm.Manager.get_instance().wait(2)
        ge.Effect.fade_out_list(self.screen, [msg])

    def __draw_dead_menu(self):
        elements = self.dead_menu.get_elements()

        ge.Effect.fade_in_list(self.screen, elements)
        self.dead_menu.init_pointer()
        self.can_press_key = True

    def __check_choice(self):
        self.dead_menu.update()
        choice = self.dead_menu.get_choice()

        if choice == 1:
            pass

        elif choice == 2:
            pass
