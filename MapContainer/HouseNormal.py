import pygame
import pytmx
from MapContainer import Map
from MapContainer import Tile


class HouseNormal(Map):
    def __init__(self, screen):
        super().__init__(screen)
        self.path = "../Assets/House/housemap.tmx"
        self.map = pytmx.load_pygame(self.path)

    def update_map(self):
        for layer in self.map.visible_layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    rect = (x * 64, y * 64)
                    surf = pygame.transform.scale(surf, (64, 64))

                    tile = Tile(rect, surf)

                    self.screen.blit(tile.img, tile.rect)

