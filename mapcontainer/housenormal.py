import mapcontainer.map as mp


class HouseNormal(mp.Map):
    def __init__(self, screen):
        self.screen = screen
        self.path = "Assets/Map/House/MapSect/"
        self.sect = Room(screen, self.path)

    def change_sect(self, name: str):
        try:
            prev_sect = self.sect.back_point[name]
        except KeyError:
            prev_sect = ""

        if name == "Room":
            self.sect = Room(self.screen, self.path, prev_sect)

        elif name == "Corridor":
            self.sect = Corridor(self.screen, self.path,  prev_sect)

        elif name == "OutDoor":
            self.sect = OutDoor(self.screen, self.path, prev_sect)

        elif name == "Kitchen":
            self.sect = Kitchen(self.screen, self.path, prev_sect)

        elif name == "Toilet":
            self.sect = Toilet(self.screen, self.path, prev_sect)

        else:
            return


class Room(mp.Sect):
    def __init__(self, screen, path, prev_sect=None):
        super().__init__(screen, prev_sect)
        self.sectpath = path + "Room.tmx"

        self.load(self.sectpath)
        self.init_OFFSET((160, 170), (0, 160))

    def get_spawn_point(self) -> tuple[float, float] | None:
        for area in self.areas:
            if area.name == "Spawn":
                return area.x, area.y

        return None


class Corridor(mp.Sect):
    def __init__(self, screen, path, prev_sect=None):
        super().__init__(screen, prev_sect)

        self.sectpath = path + "Corridor.tmx"

        self.back_point = {
            "Room": "RoomBk",
        }

        self.load(self.sectpath)
        self.init_OFFSET((150, 150), (0, 100))


class OutDoor(mp.Sect):
    def __init__(self, screen, path, prev_sect=None):
        super().__init__(screen, prev_sect)

        self.sectpath = path + "OutDoor.tmx"

        self.back_point = {
            "Corridor": "CorridorBk"
        }

        self.load(self.sectpath)
        self.init_OFFSET((50, 100), (-170, 40))


class Kitchen(mp.Sect):
    def __init__(self, screen, path, prev_sect=None):
        super().__init__(screen, prev_sect)

        self.sectpath = path + "Kitchen.tmx"

        self.back_point = {
            "OutDoor": "OutDoorBk1"
        }

        self.load(self.sectpath)
        self.init_OFFSET((170, 120), (-5, 100))


class Toilet(mp.Sect):
    def __init__(self, screen, path, prev_sect=None):
        super().__init__(screen, prev_sect)

        self.sectpath = path + "Toilet.tmx"

        self.back_point = {
            "OutDoor": "OutDoorBk2"
        }

        self.load(self.sectpath)
        self.init_OFFSET((0, 120), (-170, 120))
