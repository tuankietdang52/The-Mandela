import pygame as pg
import src.gamemanage.game as gm
import src.gameprogress.part as gp

from src.hud.hudcomp import *


class DayOne(gp.Part):

    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen)

        self.can_press_key = False
        self.can_change_map = True
        self.setup()

        self.spawn_chance = 100

    def setup(self):
        self.update_list_entities()

    def event_action(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if not self.can_press_key:
                    return

    def pressing_key(self):
        player = self.manager.player

        if not self.can_press_key:
            return

        keys = pg.key.get_pressed()

        player.handle_moving(keys)

    def update(self):
        super().update()

        if not self.is_trigger_spawn:
            self.spawn_alternate()

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

    def manage_progress(self):
        progress = self.get_progress_index()

        if progress == 0:
            self.__show_title()
            self.next()

        elif progress == 1:
            pass
