import pygame


class Tile(pygame.sprite.Sprite):
    """Position by topleft"""
    def __init__(self, img, pos, layername, tid, screen, data):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)
        self.layername = layername
        self.tid = tid
        self.data = data

        self.screen = screen

    def update(self, *args, **kwargs):
        if "Wall" in self.layername:
            pygame.draw.rect(self.screen, (0, 0, 50), self.rect)
