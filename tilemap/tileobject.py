import pygame as pg


class Area:
    """Position by topleft"""
    def __init__(self, name: str, pos: tuple[float, float], width: float, height: float):
        self.name = name
        self.x, self.y = pos
        self.width = width
        self.height = height

    def is_overlap(self, rect) -> bool:
        area = pg.Surface((self.width, self.height))
        _rect = area.get_rect(topleft=(self.x, self.y))

        # pg.draw.rect(screen, (0, 255, 0), _rect)

        if _rect.colliderect(rect):
            return True

        return False
