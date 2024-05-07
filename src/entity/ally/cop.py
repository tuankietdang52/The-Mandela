import pygame as pg
import src.movingtype.normalmoving as normv
import src.gamemanage.game as gm

from src.utils import *
from src.eventhandle.argument import *


class Cop(pg.sprite.Sprite):
    IMAGE_PATH = "../Assets/Ally/Cop/"
    __frame = 0

    def __init__(self, pos: pg.math.Vector2, groups: pg.sprite.Group = None):
        if groups is not None:
            super().__init__(groups)
        else:
            pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(f"{self.IMAGE_PATH}stand.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (36, 80))

        self.rect = self.image.get_rect(center=pos)

        self.dest = pos
        self.movement = normv.NormalMovement(self)

        self.direction = pg.math.Vector2()
        self.is_moving = False

        self.speed = 1
        self.destroy_callback = (self.on_destroy, EventArgs.empty())

        gm.Manager.get_instance().on_entities_destroy += self.destroy_callback

    def calculate_direction(self, dest: pg.math.Vector2) -> pg.math.Vector2:
        position = self.get_position()

        distance = (dest - position).magnitude()

        if distance > 0:
            self.direction = (dest - position).normalize()

        else:
            self.direction = pg.math.Vector2()

        self.direction = pg.math.Vector2(round(self.direction.x), round(self.direction.y))

        return self.direction

    def get_speed(self) -> float:
        return self.speed

    def get_rect(self) -> pg.rect.Rect:
        return self.rect

    def go_to(self, dest: pg.math.Vector2):
        self.dest = dest

    def set_position(self, pos: pg.math.Vector2):
        self.rect = self.image.get_rect(center=pos)

    def get_position(self) -> pg.math.Vector2:
        return pg.math.Vector2(self.rect.center)

    def set_size(self, size: tuple[int, int]):
        self.image = pg.transform.scale(self.image, size)

    def get_size(self) -> tuple[int, int]:
        return self.image.get_size()

    def get_voice(self, voice: str) -> pg.mixer.Sound:
        path = f"../Assets/Sound/PoliceVoice/{voice}.wav"
        return pg.mixer.Sound(path)

    def set_image(self, image: pg.surface.Surface | str, size: tuple[int, int] = None):
        """
        :param image: string: name of image
        :param size:
        """
        size = self.get_size() if size is None else size

        if type(image) is str:
            image = pg.image.load(f"{self.IMAGE_PATH + image}.png").convert_alpha()

        self.image = image
        self.set_size(size)

    def get_image(self) -> pg.surface.Surface:
        return self.image

    def can_move(self, pos: pg.math.Vector2):
        rect = self.image.get_rect(center=pos)

        if Physic.is_collide_wall(rect):
            return False

        return True

    def update(self, *args, **kwargs):
        self.movement.update_dest(self.dest)
        self.moving()

    def __set_animation_moving(self, index: int):
        direction = self.direction

        if direction.y != 0:
            if direction.y == 1:
                path = "up"

            else:
                path = "down"
        else:
            path = "walk"

        animate = f"{path + str(index)}"
        self.set_image(animate)

        if direction.x == -1:
            self.image = pg.transform.flip(self.image, True, False)

    def __play_animation_moving(self):
        if self.__frame < 20:
            index = 1

        else:
            index = 0

        self.__frame += 1
        if self.__frame > 40:
            self.__frame = 0

        self.__set_animation_moving(index)

    def moving(self):
        if self.rect.collidepoint(self.dest):
            self.is_moving = False
            return

        self.is_moving = True
        self.movement.moving()
        self.__play_animation_moving()

    def on_destroy(self, args: EventArgs):
        self.kill()
