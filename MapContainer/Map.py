import abc
import pytmx
import pygame


class Map(abc.ABC):
    def __init__(self, screen, path):
        self.screen = screen
        self.path = path
        self.map = pytmx.load_pygame(path)

    @abc.abstractmethod
    def update_map(self):
        pass
