import pygame as pg

import view.baseview as vw
import mapcontainer.map as mp
import presenter.enemy.lilypresenter as lilypr
import movingtype.movement as mv


class LilyView(vw.BaseView):
    def __init__(self,
                 screen: pg.surface.Surface,
                 gamemap: mp.Map,
                 mapsect: type[mp.Sect],
                 start_pos: pg.math.Vector2):
        super().__init__(screen,
                         lilypr.LilyPresenter(self, gamemap, mapsect, start_pos))

        self.image = self.presenter.get_image()
        self.rect = self.presenter.get_rect()

    def is_appear(self):
        if not self.presenter.is_appear():
            self.rect = self.presenter.get_rect()
            return False

        else:
            return True

    def set_position(self, pos: pg.math.Vector2):
        self.presenter.set_position(pos)

    def get_position(self) -> pg.math.Vector2:
        return self.presenter.get_position()

    def set_speed(self, speed: int):
        self.presenter.set_speed(speed)

    def get_speed(self) -> int:
        return self.presenter.get_speed()

    def get_rect(self) -> pg.rect.Rect:
        return self.presenter.get_rect()

    def update(self, *args, **kwargs):
        self.presenter.update()

        self.image = self.presenter.get_image()
        self.rect = self.presenter.get_rect()

