import random

import pygame as pg
import src.entity.thealternate.enemy as em
import src.gamemanage.game as gm
import src.movingtype.normalmoving as normv
from src.eventhandle.argument.eventargument import EventArgs

from src.tilemap import *
from src.utils import *


class Mimic(em.Enemy):
    __frame = 0
    size = (132, 168)

    def __init__(self, pos: pg.math.Vector2, groups: pg.sprite.Group):
        self.mimic_image, self.mimic_size = self.__random_object()
        super().__init__("../Assets/Enemy/Mimic/",
                         self.mimic_image,
                         pos,
                         self.mimic_size,
                         groups)

        self.active_area = Area("active", pos, self.mimic_size[0] + 200, self.mimic_size[1] + 200)
        self.__is_chasing = False
        self.speed = 1

        self.__flip()
        self.__crying_sound: pg.mixer.Channel | None = None
        
    def get_rect(self) -> pg.rect.Rect:
        if not self.__is_chasing:
            surf = pg.surface.Surface(self.size)
            return surf.get_rect(center=self.position)
        
        else:
            return super().get_rect()

    def __flip(self):
        is_flip = random.randint(0, 1)
        if is_flip == 1:
            self.flip_horizontal()

    def __random_object(self) -> tuple[str, tuple[int, int]]:
        image = [
            ("sewer1", (64, 64)),
            ("sewer2", (32, 32)),
            ("trash", (32, 64)),
            ("lamp", (96, 144)),
            ("warning", (64, 64))
        ]

        index = random.randint(0, len(image) - 1)

        return image[index]

    def __faking(self):
        player_rect = gm.Manager.get_instance().player.get_rect()

        if self.active_area.is_overlap(player_rect):
            self.__is_chasing = True
            self.__return_original()

    def __return_original(self):
        self.set_movement(normv.NormalMovement(self))
        self.set_image("mimic1", self.size)

        self.__crying_sound = SoundUtils.play_sound("../Assets/Sound/MimicVoice/crying.mp3")

    def __moving_animate(self):
        if self.__frame < 15:
            self.set_image("mimic0", self.size)

        else:
            self.set_image("mimic1", self.size)

        self.__frame += 1
        if self.__frame > 35:
            self.__frame = 0

    def update(self, *args, **kwargs):
        if not self.__is_chasing:
            self.__faking()

        else:
            super().update()
            self.set_speed(self.get_speed() + 0.001)
            self.moving()
            
    def moving(self):
        self.movement.moving()
        self.__moving_animate()

    def on_destroy(self, args: EventArgs):
        player = gm.Manager.get_instance().player
        super().on_destroy(args)

        if self.__crying_sound is not None and player.get_state() != EState.DEAD:
            self.__crying_sound.stop()
