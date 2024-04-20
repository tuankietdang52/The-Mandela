import abc
import pygame as pg
import src.gamemanage.game as gm

class IntVector2:
    """Vector2 but x,y is int type"""
    def __init__(self, x: int | pg.Vector2, y: int = None):
        if type(x) is pg.Vector2 and y is None:
            self.x, self.y = int(x.x), int(x.y)
            return

        elif y is None:
            raise ValueError("y is None")

        self.x = x
        self.y = y


class Movement(abc.ABC):
    @abc.abstractmethod
    def moving(self):
        pass
