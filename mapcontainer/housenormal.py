import pygame

from mapcontainer.map import Map
from tilemap import Tile
from tilemap import TileObject


class HouseNormal(Map):
    outpoint = None
    OFFSETX = 0
    OFFSETY = 0

    def __init__(self, screen, group):
        super().__init__(screen, "Assets/Map/House/housemap.tmx", group)

        if screen.get_size() == (1024, 768):
            self.OFFSETX = 474
            self.OFFSETY = 368

        else:
            self.OFFSETX = 630
            self.OFFSETY = 368

    def create_map(self):
        if len(self.walls) != 0:
            self.walls.clear()

        for layer in self.map.layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    pos = x * 64 - self.OFFSETX, y * 64 - self.OFFSETY

                    surf = pygame.transform.scale(surf, (64, 64))

                    tile = Tile(surf, pos, layer.name, layer.id, self.screen)

                    self.screen.blit(tile.image, tile.rect)

                    self.tilegroup.add(tile)

                    if "Wall" in layer.name or layer.name == "Object":
                        self.walls.append(tile)
