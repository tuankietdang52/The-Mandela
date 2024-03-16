import pygame
from mapcontainer import Map
from tilemap import Tile
from tilemap import TileObject


class HouseNormal(Map):
    outpoint = None

    def __init__(self, screen):
        super().__init__(screen, "Assets/Map/House/housemap.tmx")
        self.init_obj_point()

    def init_obj_point(self):
        obj = self.map.get_object_by_name("Start")
        self.startpoint = TileObject((obj.x, obj.y), obj.width, obj.height)

        obj = self.map.get_object_by_name("Out")
        self.outpoint = TileObject((obj.x, obj.y), obj.width, obj.height)

    def update_map(self):
        for layer in self.map.visible_layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    rect = (x * 64, y * 64)
                    surf = pygame.transform.scale(surf, (64, 64))

                    tile = Tile(rect, surf)

                    self.screen.blit(tile.img, tile.rect)
