import pygame

from mapcontainer.map import Map
from tilemap import Tile
from tilemap import TileObject


class HouseNormal(Map):
    outpoint = None
    OFFSETX = 400
    OFFSETY = 200

    def __init__(self, screen):
        super().__init__(screen, "Assets/Map/House/housemap.tmx")
        self.init_obj_point()

    def init_obj_point(self):
        if self.map is None:
            return

        obj = self.map.get_object_by_name("Start")
        self.startpoint = TileObject((obj.x, obj.y), obj.width, obj.height)

        obj = self.map.get_object_by_name("Out")
        self.outpoint = TileObject((obj.x, obj.y), obj.width, obj.height)

    def get_start_point(self) -> tuple[float, float]:
        x = self.startpoint.x + self.OFFSETX
        y = self.startpoint.y + self.OFFSETY

        return x, y

    def update_map(self):
        if len(self.walls) != 0:
            self.walls.clear()

        offsetx = self.player.x
        offsety = self.player.y
        speed = self.player.get_speed()

        for layer in self.map.layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    pos = (x * 64 - offsetx,
                           y * 64 - offsety)

                    surf = pygame.transform.scale(surf, (64, 64))

                    tile = Tile(surf, pos, layer.name, layer.id)

                    self.screen.blit(tile.img, tile.rect)

                    if "Wall" in layer.name or layer.name == "Object":
                        self.walls.append(tile)
