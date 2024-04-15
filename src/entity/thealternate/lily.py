import pygame as pg

import src.entity.thealternate.enemy as enenemy
import src.movingtype.movement as mv
import src.mapcontainer.map as mp


class Lily(enenemy.Enemy):
    """Position by topleft"""
    __img_path = "../Assets/Enemy/Lily/"
    size = (36, 80)

    def __init__(self,
                 gamemap: mp.Map,
                 mapsect: type[mp.Sect],
                 pos: pg.math.Vector2):

        super().__init__(gamemap,
                         mapsect,
                         f"{self.__img_path}lilystand.png",
                         pos,
                         self.size)

    def set_movement(self, movement: mv.Movement):
        self.movement = movement

    def moving(self):
        self.movement.moving()
