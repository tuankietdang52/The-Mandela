import pygame as pg

import entity.enemycontainer.enemy as enenemy
import mapcontainer.map as mp
import movingtype.normalmoving as normv


class Lily(enenemy.Enemy):
    """Position by topleft"""
    __img_path = "Assets/Enemy/Lily/"

    def __init__(self,
                 screen: pg.Surface,
                 gamemap: mp.Map,
                 sect: type[mp.Sect],
                 pos: pg.math.Vector2):

        super().__init__(screen, gamemap, sect, f"{self.__img_path}lilystand.png", pos, (36, 80))

    __ways = list()

    def moving(self):
        self.movement.moving()

