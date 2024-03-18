import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, img, pos, layername, tid):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.img = img
        self.rect = self.img.get_rect(topleft=pos)
        self.layername = layername
        self.tid = tid
