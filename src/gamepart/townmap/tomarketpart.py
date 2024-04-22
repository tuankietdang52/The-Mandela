import sys
import random
import pygame as pg
import src.gamemanage.game as gm
import src.gamepart.part as gp


class MarketPart(gp.Part):

    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen)

        self.can_press_key = True
        self.can_change_map = True
        self.setup()

        self.spawn_chance = 50

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

    def manage_progess(self):
        progess = self.get_progess_index()

        if progess == 0:
            pass
