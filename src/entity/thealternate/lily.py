import pygame as pg

import src.entity.thealternate.enemy as enenemy


class Lily(enenemy.Enemy):
    """Position by topleft"""
    size = (36, 80)

    def __init__(self,
                 pos: pg.math.Vector2,
                 groups: pg.sprite.Group):
        super().__init__("../Assets/Enemy/Lily/",
                         "lilystand",
                         pos,
                         self.size,
                         groups)

    def update(self, *args, **kwargs):
        self.moving()
        
    def moving(self):
        if self.movement is not None:
            self.movement.moving()
