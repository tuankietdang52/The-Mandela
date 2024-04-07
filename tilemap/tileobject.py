import pygame as pg

import gamemanage.game


class Area:
    """Position by topleft"""
    def __init__(self, name: str, pos: pg.math.Vector2, width: float, height: float):
        self.name = name
        self.x, self.y = pos
        self.width = width
        self.height = height

    def is_overlap(self, rect: pg.rect.Rect) -> bool:
        area = pg.Surface((self.width, self.height))
        _rect = area.get_rect(topleft=(self.x, self.y))

        # pg.draw.rect(screen, (0, 255, 0), _rect)

        if _rect.colliderect(rect):
            return True

        return False

    def draw(self):
        area = pg.Surface((self.width, self.height))
        rect = area.get_rect(topleft=(self.x, self.y))

        points = [
            rect.topleft,
            rect.topright,
            rect.bottomright,
            rect.bottomleft
        ]

        pg.draw.lines(gamemanage.game.Manager.get_screen(), (0, 0, 0), True, points, 7)
        pg.display.update()
