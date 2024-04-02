import pygame as pg

import entity.enemycontainer.enemy as enenemy
import mapcontainer.map as mp
import view.player.playerview as pv


class Lily(enenemy.Enemy):
    """Position by topleft"""
    __img_path = "Assets/Enemy/Lily/"

    def __init__(self,
                 screen: pg.Surface,
                 gamemap: mp.Map,
                 sect: type[mp.Sect],
                 pos: pg.math.Vector2):

        super().__init__(screen, gamemap, sect, f"{self.__img_path}lilystand.png", pos, (36, 80))
        self.speed = 1

    __ways = list()

    def bypass_to_player(self):
        player_position = pv.PlayerView.get_instance().get_position()
        src = self.position
        dest = player_position

        if len(self.__ways) == 0:
            self.__ways = self.find_way(src, dest)

        self.position = self.__ways.pop(0)

    def moving(self, velocity: pg.math.Vector2):
        self.__ways.clear()

        self.position += velocity
