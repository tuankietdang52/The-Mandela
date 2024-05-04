import sys
import pygame as pg
import src.gamemanage.game as gm
import src.gameprogress.progressmanager as gp
import src.hud.menu.view.deadmenuhud as dm
import src.gameprogress.other.startmenu as sm
import src.mapcontainer.housenormal as mphouse

from src.utils import *


class DeadMenu(gp.ProgressManager):
    def __init__(self, screen: pg.surface.Surface, current_part: gp.ProgressManager):
        super().__init__(screen)

        self.dead_menu = dm.DeadMenuHUD(self.screen, self.manager.hud_groups)
        self.current_part = current_part

        self.setup()

    def setup(self):
        self.spawn_manager.clear_enemies()
        super().setup()

    def event_action(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

    def pressing_key(self):
        pass

    def update(self):
        if self.get_progress_index() == 2:
            # block event update because in deadmenuhud already have one
            self.manage_progress()
        else:
            super().update()

    def manage_progress(self):
        progress = self.get_progress_index()

        if progress == 0:
            self.__show_dead_msg()
            self.next()

        elif progress == 1:
            SoundUtils.clear_all_sound()
            self.__draw_dead_menu()
            self.next()

        elif progress == 2:
            self.__check_choice()

    def __show_dead_msg(self):
        Effect.fade_out_screen(False)
        self.__hide_hud()

        msg = self.dead_menu.get_dead_msg()

        self.screen.blit(msg[0], msg[1])
        pg.display.update()

        gm.Manager.get_instance().wait(2)
        Effect.fade_out_list(self.screen, [msg])

    def __hide_hud(self):
        self.manager.player.hungry_bar.set_visible(False)
        self.manager.player.sanity_bar.set_visible(False)

    def __draw_dead_menu(self):
        elements = self.dead_menu.get_elements()

        Effect.fade_in_list(self.screen, elements)
        self.dead_menu.init_pointer()
        self.can_press_key = True

    def __check_choice(self):
        self.dead_menu.update()
        choice = self.dead_menu.get_choice()

        if choice == 1:
            self.__replay()

        elif choice == 2:
            self.__to_main_menu()

    def reset_map(self):
        self.manager.set_map(mphouse.HouseNormal(self.screen))
        gamemap = self.manager.gamemap
        player = self.manager.player

        gamemap.sect.create()
        gamemap.change_sect("OutDoor")

        point = gamemap.sect.get_start_point()
        player.set_position(point)

    def __replay(self):
        self.dead_menu.destroy()

        self.reset_map()
        self.manager.player.reset()
        self.manager.set_game_progress(self.current_part)
        self.manager.gameprogress.set_progress_index(self.current_part.load_progress_index)

        self.manager.reset_time()
        Effect.fade_in_screen()
        SoundUtils.clear_all_sound()

    def __to_main_menu(self):
        self.destroy()
        self.destroy_hud()

        self.manager.set_game_progress(sm.StartMenu(self.screen))
        self.manager.gameprogress.set_progress_index(1)

    def destroy(self):
        Effect.fade_out_screen()
        self.dead_menu.destroy()

    def destroy_hud(self):
        for hud in self.manager.hud_groups:
            hud.kill()
