import pygame as pg
import src.mapcontainer.map as mp
import src.mapcontainer.town as mptown


class Market(mp.Map):
    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen, "../Assets/Map/Market/MapSect/")

        self.ori_block_size = 16
        self.size = 32

        self.change_sect("Market")

    def get_next_map(self, area_name):
        if area_name == "Town":
            next_map = mptown.Town(self.screen)
            next_map.change_sect("OutsideMarket")
            return next_map, "Going Outside ?"

    def setup_sections(self):
        self.sections.clear()
        self.sections.append(
            ("Market", MarketSect(self.screen, self.path))
        )


class MarketSect(mp.Sect):
    def __init__(self,
                 screen: pg.surface.Surface,
                 path: str,
                 back_point: str = ""):
        super().__init__(screen, "MarketBk", back_point)

        self.sectpath = path + "Market.tmx"
        self.load(self.sectpath)
        self.init_OFFSET((15, -140), (-170, -170))
