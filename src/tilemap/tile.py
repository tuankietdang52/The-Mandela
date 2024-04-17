import pygame as pg


class Tile(pg.sprite.Sprite):
    """Position by topleft"""
    def __init__(self,
                 screen: pg.surface.Surface,
                 image: pg.surface.Surface,
                 pos: tuple[float, float],
                 layername: str,
                 tid,
                 data,
                 groups: pg.sprite.Group):
        pg.sprite.Sprite.__init__(self, groups)
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.layername = layername
        self.tid = tid
        self.data = data

        self.screen = screen

    def update(self, *args, **kwargs):
        if "Wall" in self.layername:
            pg.draw.rect(self.screen, (0, 0, 50), self.rect)
