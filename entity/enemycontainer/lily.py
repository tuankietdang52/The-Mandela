import pygame as pg

import entity.enemycontainer.enemy as enenemy
import mapcontainer.map as mp
import movingtype.movement as mv


class Lily(enenemy.Enemy):
    """Position by topleft"""
    __img_path = "Assets/Enemy/Lily/"

    def __init__(self,
                 gamemap: mp.Map,
                 mapsect: type[mp.Sect],
                 pos: pg.math.Vector2):

        super().__init__(gamemap,
                         mapsect,
                         f"{self.__img_path}lilystand.png",
                         pos,
                         (36, 80))

    def set_movement(self, movement: mv.Movement):
        self.movement = movement

    def moving(self):
        self.movement.moving()

