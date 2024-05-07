import pygame as pg
import src.mapcontainer.map as mp
import src.mapcontainer.housenormal as mphouse
import src.mapcontainer.market as mk


class Town(mp.Map):
    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen, "../Assets/Map/Town/MapSect/")

        self.ori_block_size = 16
        self.size = 32

        self.change_sect("Home")

    def get_next_map(self, area_name) -> tuple[mp.Map, str] | None:
        if area_name == "HouseNormal":
            next_map = mphouse.HouseNormal(self.screen)
            next_map.change_sect("OutDoor")
            return next_map, "Enter your house ?"

        elif area_name == "Market":
            next_map = mk.Market(self.screen)
            next_map.change_sect("Market")
            return next_map, "Enter Convenience Store ?"

        return None

    def setup_sections(self):
        self.sections.clear()
        self.sections.extend([
            ("Home", Home(self.screen, self.path)),
            ("Hotel", Hotel(self.screen, self.path)),
            ("Crossroad", CrossRoad(self.screen, self.path)),
            ("RoadToPark", RoadToPark(self.screen, self.path)),
            ("ParkMart", ParkMart(self.screen, self.path)),
            ("Park1", Park1(self.screen, self.path)),
            ("Park2", Park2(self.screen, self.path)),
            ("OutsideMarket", OutsideMarket(self.screen, self.path)),
            ("PublicToilet", PublicToilet(self.screen, self.path)),
            ("RoadToPolice", RoadToPolice(self.screen, self.path)),
            ("PoliceGraveyard", PoliceGraveyard(self.screen, self.path)),
            ("GraveyardEntrance", GraveyardEntrance(self.screen, self.path)),
            ("Graveyard", Graveyard(self.screen, self.path)),
            ("Police", Police(self.screen, self.path)),
            ("RoadToApartment", RoadToApartment(self.screen, self.path)),
            ("Apartment", Apartment(self.screen, self.path)),
        ])


class Home(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "HomeBk", back_point)

        self.sectpath = path + "Home.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((30, 0), (-160, -30))


class Hotel(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "HotelBk", back_point)

        self.sectpath = path + "Hotel.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((-130, -10), (-300, -50))


class CrossRoad(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "CrossroadBk", back_point)

        self.sectpath = path + "Crossroad.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((-115, -100), (-270, -150))


class RoadToPark(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "RoadToParkBk", back_point)

        self.sectpath = path + "RoadToPark.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((-120, -15), (-290, -50))


class ParkMart(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "ParkMartBk", back_point)

        self.sectpath = path + "ParkMart.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((0, 0), (-170, -30))


class Park1(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "Park1Bk", back_point)

        self.sectpath = path + "Park1.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((-78, 15), (-250, -10))


class Park2(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "Park2Bk", back_point)

        self.sectpath = path + "Park2.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((-30, 15), (-220, -10))


class OutsideMarket(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "OutsideMarketBk", back_point)

        self.sectpath = path + "OutsideMarket.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((0, 0), (-170, -10))


class PublicToilet(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "PublicToiletBk", back_point)

        self.sectpath = path + "PublicToilet.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((-92, 15), (-300, 0))


class RoadToPolice(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "RoadToPoliceBk", back_point)

        self.sectpath = path + "RoadToPolice.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((-132, 0), (-300, -25))


class PoliceGraveyard(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "PoliceGraveyardBk", back_point)

        self.sectpath = path + "PoliceGraveyard.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((-80, -70), (-250, -100))


class GraveyardEntrance(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "GraveyardEntranceBk", back_point)

        self.sectpath = path + "GraveyardEntrance.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((-50, -85), (-225, -120))


class Graveyard(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "GraveyardBk", back_point)

        self.sectpath = path + "Graveyard.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((-80, -15), (-240, -40))


class Police(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "PoliceBk", back_point)

        self.sectpath = path + "Police.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((-90, -40), (-280, -70))


class RoadToApartment(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "RoadToApartmentBk", back_point)

        self.sectpath = path + "RoadToApartment.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((-15, -40), (-180, -75))


class Apartment(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "ApartmentBk", back_point)

        self.sectpath = path + "Apartment.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((0, -15), (-175, -45))
