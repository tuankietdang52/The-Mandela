import sys

import src.hud.startmenuhud as hud_sm
import src.gamemanage.effect as ge
import src.gamepart.housemap.beginning as bg
import src.gamepart.part as gp

from src.pjenum import EState
from src.hud import *


class StartMenu(gp.Part):
    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen)

        self.startmenu = hud_sm.StartMenuHUD(screen)
        self.title_start = self.startmenu.get_start_title()
        self.elements = self.startmenu.get_elements()

        self.__is_open_board = False

        self.alpha = 0
        self.choice = 1

    def setup(self):
        gamemap = self.manager.gamemap
        player = self.manager.player

        gamemap.change_sect("Room")
        gamemap.sect.create()

        start_point = gamemap.sect.get_start_point()

        player.set_position(start_point)

        player.set_state(EState.BUSY)
        player.set_image("sit", player.size)

        self.manager.update_UI_ip()
        pg.time.wait(1000)

    def __fade_in(self, ls):
        if self.alpha == 255:
            return

        self.alpha += 1
        ge.Effect.set_list_opacity(self.screen, ls, self.alpha)

    def __fade_out(self, ls):
        manager = self.manager.get_instance()
        sect = manager.gamemap.sect

        if self.alpha <= 0:
            return

        if sect.is_created:
            manager.update_UI()

        self.alpha -= 1
        ge.Effect.set_list_opacity(self.screen, ls, self.alpha)

    def pressing_key(self):
        if not self.can_press_key:
            return

        keys = pg.key.get_pressed()

        if keys[pg.K_ESCAPE]:
            if self.__is_open_board:
                self.__closing_load_board()

    def __open_load_board(self):
        pos = self.manager.screen.get_width() / 2, self.manager.screen.get_height() / 2
        load_board = Board(self.screen, pos, (700, 600))
        load_board.draw()
        self.__is_open_board = True

    def __closing_load_board(self):
        self.manager.update_UI_ip()
        self.__is_open_board = False

        self.startmenu.draw_elements()
        self.startmenu.change_choice(2)

    def event_action(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if not self.can_press_key:
                    return

                key = event.key
                self.__move_cur(key)

    def __move_cur(self, key):
        if self.__is_open_board:
            return

        if key == pg.K_RETURN:
            self.startmenu.pointer.play_choose_sound()
            self.__check_choice()
            return

        elif key == pg.K_w:
            if self.choice == 1:
                return
            self.choice -= 1

        elif key == pg.K_s:
            if self.choice == 3:
                return
            self.choice += 1

        else:
            return

        self.manager.update_UI()
        self.startmenu.draw_elements()
        self.startmenu.change_choice(self.choice)

    def __check_choice(self):
        if self.choice == 1:
            self.can_press_key = False
            self.next()

        elif self.choice == 2:
            self.__open_load_board()

        elif self.choice == 3:
            sys.exit()

    def update(self):
        self.manage_progess()

    def manage_progess(self):
        progess = self.get_progess_index()
        if progess == 0:
            self.__begin()

        elif progess == 1:
            self.__to_start_menu()

        elif progess == 2:
            self.setup()
            self.next()

        elif progess == 3:
            self.__setup_start_menu()

        elif progess == 4:
            self.__fade_out(self.elements.values())
            pg.mixer.music.fadeout(1000)
            if self.alpha <= 0:
                self.__destroying()

    def __begin(self):
        self.__fade_in([self.title_start])
        if self.alpha == 255:
            self.next()

    def __to_start_menu(self):
        self.screen.fill((0, 0, 0))
        self.__fade_out([self.title_start])
        if self.alpha > 0:
            return

        self.alpha = 0
        self.next()

    def __setup_start_menu(self):
        if not pg.mixer.music.get_busy():
            gm.Manager.play_theme("../Assets/Sound/Other/rain.mp3")

        self.__fade_in(self.elements.values())
        if self.alpha == 255 and not self.startmenu.pointer.is_set:
            self.startmenu.change_choice(1)
            self.can_press_key = True

    def __destroying(self):
        player = self.manager.player

        x, y = player.get_position()

        player.set_position((x - 50, y))
        player.set_image("walk1")
        player.flip_horizontal()

        self.manager.update_UI_ip()
        player.set_state(EState.FREE)

        self.manager.set_part(bg.BeginStory(self.screen))