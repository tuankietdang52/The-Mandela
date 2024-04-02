import pygame as pg

import mapcontainer.map as mp
import presenter.enemy.lilypresenter as lilypr


class LilyView(pg.sprite.Sprite):
    def __init__(self,
                 screen: pg.surface.Surface,
                 gamemap: mp.Map,
                 start_pos: pg.math.Vector2):
        pg.sprite.Sprite.__init__(self)

        self.screen = screen
        self.presenter = lilypr.LilyPresenter(self.screen, self, gamemap, type(gamemap.sect), start_pos)

        self.image = self.presenter.get_image()
        self.rect = self.presenter.get_rect()

    def is_appear(self):
        if not self.presenter.is_appear():
            self.rect = self.presenter.get_rect()
            return False

        else:
            return True

    def update(self, *args, **kwargs):
        self.presenter.chase_player()

        self.image = self.presenter.get_image()
        self.rect = self.presenter.get_rect()

