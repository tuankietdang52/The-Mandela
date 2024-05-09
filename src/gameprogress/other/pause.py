import sys
import pygame as pg
import src.gamemanage.game as gm
import src.gameprogress.progressmanager as gp
import src.hud.menu.view.pausemenu as ps
import src.gameprogress.other.startmenu as sm
import src.mapcontainer.housenormal as mphouse

from src.utils import *


class Pause(gp.ProgressManager):
    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen)
        self.pause_hud = ps.PasueMenuHUD(self.screen)

        self.is_resume = True

    def setup(self):
        pass

    def re_setup(self):
        pass

    def event_action(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

    def pressing_key(self):
        pass

    def update(self):
        self.manage_progress()

    def manage_progress(self):
        self.__check_choice()

    def show(self):
        self.is_resume = False
        self.pause_hud.show(self.manager.hud_groups)

    def __check_choice(self):
        self.pause_hud.update()
        choice = self.pause_hud.get_choice()

        if choice == 1:
            self.destroy()

        elif choice == 2:
            self.__to_main_menu()

        elif choice == 3:
            sys.exit()

    def __to_main_menu(self):
        self.destroy()
        self.destroy_hud()

        Effect.fade_out_screen()

        self.manager.set_game_progress(sm.StartMenu(self.screen))
        self.manager.gameprogress.set_progress_index(1)

    def destroy(self):
        self.is_resume = True
        self.pause_hud.destroy()

    def destroy_hud(self):
        for hud in self.manager.hud_groups:
            hud.kill()
