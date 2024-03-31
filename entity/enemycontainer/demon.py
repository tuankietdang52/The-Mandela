import random

import pygame

import entity.enemycontainer.enemy
import gamemanage.physic
import mapcontainer.map
import view.playerview


class Demon(entity.enemycontainer.enemy.Enemy):
    """Position by topleft"""
    def __init__(self,
                 screen: pygame.Surface,
                 gamemap: mapcontainer.map.Map,
                 sect: type[mapcontainer.map.Sect],
                 pos: tuple[float, float]):
        super().__init__(screen, gamemap, sect, "demon.png", pos, (36, 80))

        self.speed = 1
        self.is_avoid = False

    path = list()

    def update(self, *args, **kwargs):
        if not self.is_appear():
            return

        self.chase_player()

    def chase_player(self):
        player_rect = view.playerview.PlayerView.get_instance().get_rect()
        src = self.rect.x, self.rect.y
        dest = player_rect.x, player_rect.y

        if len(self.path) == 0:
            self.path = self.find_way(src, dest)

        pair = self.path.pop(0)

        x, y = pair.x, pair.y

        self.rect = self.image.get_rect(topleft=(x, y))

