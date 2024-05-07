import pygame as pg

import src.entity.thealternate.enemy as em


class Lily(em.Enemy):
    """Position by topleft"""
    size = (36, 80)

    def __init__(self, pos: pg.math.Vector2):
        super().__init__("../Assets/Enemy/Lily/",
                         "lilystand",
                         pos,
                         self.size)

    def update(self, *args, **kwargs):
        super().update()
        self.moving()
        
    def moving(self):
        if self.movement is not None:
            self.movement.moving()
