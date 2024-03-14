import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, img):
        pygame.sprite.Sprite.__init__(self)
        self.img = img
        self.rect = self.img.get_rect(topleft = pos)
