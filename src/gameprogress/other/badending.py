import sys
import src.gameprogress.progressmanager as gp
import src.hud.ending.view.badendingview as bdhud
import src.gameprogress.other.startmenu as sm

from src.utils import *


class BadEnding(gp.ProgressManager):
    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen)

        self.bad_ending_hud = bdhud.BadEnidngHUD(self.screen, self.manager.hud_groups)
        self.setup()

    def setup(self):
        self.spawn_manager.clear_enemies()
        super().setup()

    def re_setup(self):
        pass

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
            Effect.to_black_screen()
            self.next()

        elif progress == 1:
            SoundUtils.clear_all_sound()
            self.__draw_bad_ending_menu()
            self.next()

        elif progress == 2:
            self.__check_enter()

        elif progress == 3:
            self.__draw_thanks_screen()

        elif progress == 4:
            self.__to_main_menu()

    def __hide_hud(self):
        self.manager.player.hungry_bar.set_visible(False)
        self.manager.player.sanity_bar.set_visible(False)

    def __draw_bad_ending_menu(self):
        elements = self.bad_ending_hud.get_elements()

        Effect.fade_in_list(self.screen, elements)
        self.bad_ending_hud.image.set_alpha(254)

        self.can_press_key = True

    def __draw_thanks_screen(self):
        Effect.fade_out_list(self.screen, [(self.bad_ending_hud.image, self.bad_ending_hud.rect)])

        msg = self.bad_ending_hud.get_thanks_surf()

        Effect.fade_in_list(self.screen, [msg])
        gm.Manager.get_instance().wait(2)
        Effect.fade_out_list(self.screen, [msg])
        self.bad_ending_hud.draw()

        self.next()

    def __check_enter(self):
        self.bad_ending_hud.image.set_alpha(255)

        if self.bad_ending_hud.is_enter:
            self.next()

    def __to_main_menu(self):
        self.destroy()
        self.destroy_hud()

        self.manager.set_game_progress(sm.StartMenu(self.screen))
        self.manager.gameprogress.set_progress_index(1)

    def destroy(self):
        Effect.to_black_screen()
        self.bad_ending_hud.destroy()

    def destroy_hud(self):
        for hud in self.manager.hud_groups:
            hud.kill()
