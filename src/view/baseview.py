import abc
import pygame as pg


class BaseView(abc.ABC, pg.sprite.Sprite):
    def __init__(self, screen: pg.surface.Surface, presenter):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.presenter = presenter

    @abc.abstractmethod
    def set_position(self, pos: pg.math.Vector2):
        pass

    @abc.abstractmethod
    def get_position(self) -> pg.math.Vector2:
        pass

    @abc.abstractmethod
    def set_speed(self, speed: int):
        pass

    @abc.abstractmethod
    def get_speed(self) -> int:
        pass

    @abc.abstractmethod
    def get_rect(self) -> pg.rect.Rect:
        pass
