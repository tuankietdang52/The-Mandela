import pygame as pg
import src.gamemanage.game as gm
import src.gameprogress.progressmanager as gp
import src.mapcontainer.market as mk

import src.mapcontainer.town as mptown
import src.gameitem.food as fd

from src.hud.hudcomp import *
from src.hud.timehud import *


class NightOne(gp.ProgressManager):

    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen)

        self.can_press_key = False
        self.can_change_map = True
        self.setup()

        self.load_progress_index = 0

        self.spawn_manager.set_enemy_spawn_chance(20)

    def event_action(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if not self.can_press_key:
                    return

    def __get_title(self) -> tuple[pg.surface.Surface, pg.rect.Rect]:
        fontpath = "../Assets/Font/Crang.ttf"
        center = self.screen.get_size()

        font = pg.font.Font(fontpath, 40)
        title_surf = Effect.create_text_outline(font,
                                                "Day One",
                                                (255, 255, 255),
                                                2,
                                                (255, 0, 0))

        title_rect = title_surf.get_rect(center=(center[0] / 2, center[1] / 2))
        return title_surf, title_rect

    def __draw_title(self, title_surf: pg.surface.Surface, title_rect: pg.rect.Rect):
        self.screen.blit(title_surf, title_rect)
        pg.display.update()

    def __show_title(self):
        Effect.to_black_screen()
        title = self.__get_title()
        self.__draw_title(title[0], title[1])

        self.manager.wait(2)

        Effect.fade_out_list(self.screen, [title])
        Effect.set_full_opacity_screen()

        self.can_press_key = True

    def __setup_hud(self):
        self.manager.player.init_hud(self.manager.hud_groups)
        self.time_hud = TimeHUD(self.manager.hud_groups)

    def __show_guide(self):
        guide = """In the upper left corner, there are 2 bars.
        |One show how hungry you are, if the bar is down to empty. You'll die
        |Other will show your sanity. The lower sanity you are, the more alternate spawn
        | |You can only sleep after 2 AM |[Go to bed and press F]
        | | | |WARNING: COMEBACK HOME AND SLEEP BEFORE 3 AM"""

        width, height = self.screen.get_size()
        board = BoardText(self.screen, guide, 20, (width / 2, height / 2), (width * 0.7, height - 20))

        board.draw()
        pg.display.update()

        while not HUDComp.is_closing_board():
            self.can_press_key = False

        self.can_press_key = True
        self.manager.update_UI_ip()

    def update(self):
        super().update()

        if not self.spawn_manager.is_trigger_spawn:
            self.spawn_manager.spawn_alternate()

    def manage_progress(self):
        progress = self.get_progress_index()

        if progress == 0:
            self.__show_title()
            self.next()

        elif progress == 1:
            self.__setup_hud()
            self.next()

        elif progress == 2:
            self.__show_guide()
            self.next()

        elif progress == 3:
            self.__spawn_food()
            self.next()

        # elif progress == 4:

    def __spawn_food(self):
        sect = self.manager.gamemap.sect
        if type(sect) is not mk.MarketSect:
            return

        self.spawn_manager.spawn_food_in_market()
        self.next()

    # def __get_to_phone(self):
    #
