import pygame as pg

import mapcontainer.map as mp
import presenter.enemy.lilypresenter as lilypr


class LilyView(pg.sprite.Sprite):
    def __init__(self,
                 screen: pg.surface.Surface,
                 gamemap: mp.Map,
                 gamesect: type[mp.Sect],
                 start_pos: pg.math.Vector2):
        pg.sprite.Sprite.__init__(self)

        self.screen = screen
        self.presenter = lilypr.LilyPresenter(self.screen, self, gamemap, gamesect, start_pos)

        self.image = self.presenter.get_image()
        self.rect = self.presenter.get_rect()

    def is_appear(self):
        if not self.presenter.is_appear():
            self.rect = self.presenter.get_rect()
            return False

        else:
            return True

    def update(self, *args, **kwargs):
        self.presenter.update()

        self.image = self.presenter.get_image()
        self.rect = self.presenter.get_rect()

