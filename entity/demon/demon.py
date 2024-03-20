import pygame
import gamemanage.physic


class Demon(pygame.sprite.Sprite):
    __path = "Assets/Enemy/"

    def __init__(self, screen, pos):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(f"{self.__path}demon.png").convert_alpha()
        self.rect = self.img.get_rect(topleft=pos)

        self.screen = screen
        self.pos = pos
