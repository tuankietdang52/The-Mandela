import pygame as pg

import src.entity.thealternate.enemy as enenemy
import src.gamemanage.game as gm


class Lily(enenemy.Enemy):
    """Position by topleft"""
    size = (36, 80)

    def __init__(self,
                 pos: pg.math.Vector2,
                 groups: pg.sprite.Group):

        self.img_path = "../Assets/Enemy/Lily/"
        super().__init__(f"{self.img_path}lilystand.png",
                         pos,
                         self.size,
                         groups)

    def update(self, *args, **kwargs):
        self.moving()
