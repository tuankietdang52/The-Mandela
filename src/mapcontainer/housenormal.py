import pygame as pg
import src.mapcontainer.map as mp
import src.mapcontainer.town as mptown


class HouseNormal(mp.Map):
    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen, "../Assets/Map/House/MapSect/")

        self.change_sect("OutDoor")

    def get_next_map(self, area_name: mp.Map) -> tuple[mp.Map, str] | None:
        if area_name == "Town":
            next_map = mptown.Town(self.screen)
            next_map.change_sect("Home")
            return next_map, "Go Outside ?"

        return None

    def setup_sections(self):
        self.sections.clear()
        self.sections.extend([
            ("Room", Room(self.screen, self.path)),
            ("Corridor", Corridor(self.screen, self.path)),
            ("OutDoor", OutDoor(self.screen, self.path)),
            ("Kitchen", Kitchen(self.screen, self.path)),
            ("Toilet", Toilet(self.screen, self.path)),
        ])


class Room(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "RoomBk", back_point)

        self.sectpath = path + "Room.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((30, 40), (-160, 30))


class Corridor(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "CorridorBk", back_point)

        self.sectpath = path + "Corridor.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((40, -150), (-110, -200))


class OutDoor(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "OutDoorBk", back_point)

        self.sectpath = path + "OutDoor.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((50, -70), (-170, -130))


class Kitchen(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "KitchenBk", back_point)

        self.sectpath = path + "Kitchen.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((-80, 0), (-255, -20))


class Toilet(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "ToiletBk", back_point)

        self.sectpath = path + "Toilet.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((-260, 20), (-430, 20))
