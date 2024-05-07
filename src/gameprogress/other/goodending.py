import sys
import pygame as pg
import src.gamemanage.game as gm
import src.mapcontainer.road as rd
import src.gameobj.otherobj as otherobj
import src.gameprogress.progressmanager as gp
import src.gameprogress.other.startmenu as sm
import src.mapcontainer.housenormal as mphouse
import src.hud.ending.view.goodendingview as gdhud

from src.utils import *


class GoodEnding(gp.ProgressManager):
    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen)
        self.manager.hud_groups.empty()
        self.manager.entities.empty()

        self.good_ending_hud = gdhud.GoodEnidngHUD(self.screen, self.manager.hud_groups)
        self.car: otherobj.PoiceCarFront | None = None

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
        super().update()

    def manage_progress(self):
        progress = self.get_progress_index()

        if progress == 0:
            Effect.fade_out_screen()
            self.next()

        elif progress == 1:
            SoundUtils.clear_all_sound()
            self.__draw_good_ending_scene()

        elif progress == 2:
            self.__draw_good_ending_title()

        elif progress == 3:
            self.__is_go_to_end()

        elif progress == 4:
            self.__draw_author()
            self.__draw_thanks_screen()

        elif progress == 5:
            self.__to_main_menu()

    def __draw_good_ending_scene(self):
        self.manager.entities.empty()

        self.manager.set_map(rd.Road(self.screen))
        self.manager.gamemap.sect.create()

        sect = self.manager.gamemap.sect

        point = sect.get_point("Car")

        if not gm.Game.IS_FULLSCREEN:
            position = pg.math.Vector2(point.x / 4 - 200, point.y / 4 - 10)
        else:
            position = pg.math.Vector2(point.x / 4 - 200, point.y / 4 + 70)

        self.car = otherobj.PoiceCarFront(position, rd.RoadSect)

        self.spawn_manager.add_object(self.car)

        Effect.fade_in_screen()
        self.next()

    def __draw_good_ending_title(self):
        elements = self.good_ending_hud.get_elements()

        Effect.fade_in_list(self.screen, elements)
        self.good_ending_hud.draw()
        self.next()

    def __is_go_to_end(self):
        self.good_ending_hud.image.set_alpha(255)

        if self.car.rect.topleft[0] > self.screen.get_width():
            self.next()

    def __draw_author(self):
        msg = self.good_ending_hud.get_me()

        Effect.fade_in_list(self.screen, [msg])
        gm.Manager.get_instance().wait(2)
        Effect.fade_out_list(self.screen, [msg])
        self.good_ending_hud.draw()

    def __draw_thanks_screen(self):
        msg = self.good_ending_hud.get_thanks_surf()

        Effect.fade_in_list(self.screen, [msg])
        gm.Manager.get_instance().wait(2)
        Effect.fade_out_list(self.screen, [msg])
        self.good_ending_hud.draw()

        Effect.fade_out_screen()

        self.next()

    def __to_main_menu(self):
        self.destroy()

        self.manager.set_game_progress(sm.StartMenu(self.screen))
        self.manager.gameprogress.set_progress_index(1)

    def destroy(self):
        Effect.to_black_screen()
        for obj in self.manager.appear_object:
            obj.kill()

    def destroy_hud(self):
        for hud in self.manager.hud_groups:
            hud.kill()
