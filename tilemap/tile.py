import pygame


class Tile(pygame.sprite.Sprite):
    """Position by topleft"""
    def __init__(self, img, pos, layername, tid, screen):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)
        self.layername = layername
        self.tid = tid

        self.screen = screen

    def update(self, *args, **kwargs):
        pass
       # if "Wall" in self.layername:
            #pygame.draw.rect(self.screen, (255, 0, 0), self.rect)
