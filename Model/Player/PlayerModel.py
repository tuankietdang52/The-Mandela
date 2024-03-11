import pygame


class PlayerModel(pygame.sprite.Sprite):
    _health = 1000
    x = 0
    y = 0

    def __init__(self, health):
        self._health = health
        pygame.sprite.Sprite.__init__(self)

    def set_health(self, health):
        self._health = health

    def get_health(self):
        return self._health

    def decrease_health(self, damage):
        self._health -= damage

