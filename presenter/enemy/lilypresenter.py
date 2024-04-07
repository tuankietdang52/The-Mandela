import pygame as pg
import mapcontainer.map as mp
import entity.enemycontainer.lily as enlily
import view.player.playerview as pv
import movingtype.movement as mv


class LilyPresenter:
    __img_path = "Assets/Enemy/Lily/"

    def __init__(self,
                 view,
                 gamemap: mp.Map,
                 mapsect: type[mp.Sect],
                 pos: pg.Vector2):
        self.view = view
        self.model = enlily.Lily(gamemap, mapsect, pos)

    def set_position(self, pos: pg.math.Vector2 | tuple[float, float]):
        self.model.set_position(pos)

    def get_position(self) -> pg.math.Vector2:
        return self.model.get_position()

    def set_image(self, image: pg.surface.Surface | str):
        """
        :param image: string: name of image
        """
        if type(image) is str:
            image = pg.image.load(self.__img_path + image)

        self.model.set_image(image)

    def get_image(self) -> pg.surface.Surface:
        return self.model.get_image()

    def get_rect(self):
        return self.model.get_rect()

    def is_appear(self):
        return self.model.is_appear()

    def set_movement(self, movement: mv.Movement):
        self.model.set_movement(movement)

    def set_speed(self, speed: int):
        self.model.set_speed(speed)

    def get_speed(self) -> int:
        return self.model.get_speed()

    def update(self):
        self.model.moving()
