import abc
import os

import pygame
import pytmx


class Map(abc.ABC):
    startpoint = None
    walls = list()

    map = None

    tilegroup = pygame.sprite.Group()

    def __init__(self, screen, path, group):
        self.screen = screen
        self.path = path
        self.tilegroup = group

        if os.getcwd() == "C:\\Users\\ADMIN\\PycharmProjects\\Nightmare":
            self.map = pytmx.load_pygame(path)

    @abc.abstractmethod
    def create_map(self):
        pass

    def update_map(self, x, y):
        group = self.tilegroup

        for tile in group:
            tile.rect.x -= x
            tile.rect.y -= y

        group.draw(self.screen)
