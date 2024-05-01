import random

import pygame as pg
import src.entity.thealternate.enemy as em
import src.movingtype.normalmoving as normv
import src.movingtype.randommoving as randmv
import src.gamemanage.game as gm

from src.tilemap.tileobject import *


class Doppelganger(em.Enemy):
    size = (36, 80)
    __frame = 0
    __sound_path = "../Assets/Sound/DoppelgangerVoice/"

    def __init__(self,
                 pos: pg.math.Vector2,
                 groups: pg.sprite.Group):
        colors = ["blue", "red", "yellow", "green"]
        self.color = colors[random.randint(0, len(colors) - 1)]

        super().__init__("../Assets/Enemy/Doppelganger/",
                         f"{self.color}walk1",
                         pos,
                         self.size,
                         groups)

        self.set_movement(randmv.RandomMovement(self, 200))
        self.is_chasing = False

        self.detect_range = random.randint(400, 800)

    def update(self, *args, **kwargs):
        super().update()

        if not self.is_chasing:
            self.__detect_player()

        self.moving()

    def __detect_player(self):
        position = self.get_position()
        area = Area("active", position, self.detect_range, self.detect_range)

        player_rect = gm.Manager.get_instance().player.get_rect()

        if area.is_overlap(player_rect):
            self.__start_chasing()

    def __start_chasing(self):
        self.set_movement(normv.NormalMovement(self))
        self.is_chasing = True

    def __set_animation_moving(self, index: int):
        direction = self.direction

        if direction.y != 0:
            if direction.y == 1:
                path = "up"

            else:
                path = "down"
        else:
            path = "walk"

        animate = f"{self.color + path + str(index)}"
        self.set_image(animate)

        if direction.x == -1:
            self.flip_horizontal()

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
        cur = self.get_position()
        self.movement.moving()

        if cur != self.get_position():
            self.__play_animation_moving()
