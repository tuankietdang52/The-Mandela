import mapcontainer.map


class HouseNormal(mapcontainer.map.Map):
    def __init__(self, screen):
        self.screen = screen
        self.path = "Assets/Map/House/MapSect/"
        self.sect = Room(screen, self.path)

    def change_sect(self, name):
        """
        :param str name: name section
        """
        try:
            prev_sect = self.sect.back_point[name]
        except KeyError:
            prev_sect = ""

        if name == "Room":
            self.sect = Room(self.screen, self.path, prev_sect)

        if name == "Corridor":
            self.sect = Corridor(self.screen, self.path,  prev_sect)

        if name == "OutDoor":
            self.sect = OutDoor(self.screen, self.path, prev_sect)

        if name == "Kitchen":
            self.sect = Kitchen(self.screen, self.path, prev_sect)

        if name == "Toilet":
            self.sect = Toilet(self.screen, self.path, prev_sect)

        else:
            return


class Room(mapcontainer.map.Sect):
    def __init__(self, screen, path, prev_sect=None):
        super().__init__(screen, prev_sect)
        self.sectpath = path + "Room.tmx"

        self.load_sect(self.sectpath)
        self.init_OFFSET((160, 170), (0, 160))

    def get_spawn_point(self) -> tuple[float, float] | None:
        for area in self.areas:
            if area.name == "Spawn":
                return area.x, area.y

        return None


class Corridor(mapcontainer.map.Sect):
    back_point = {
        "Room": "RoomBk",
    }

    def __init__(self, screen, path, prev_sect=None):
        super().__init__(screen, prev_sect)

        self.sectpath = path + "Corridor.tmx"

        self.load_sect(self.sectpath)
        self.init_OFFSET((150, 150), (0, 100))


class OutDoor(mapcontainer.map.Sect):
    back_point = {
        "Corridor": "CorridorBk"
    }

    def __init__(self, screen, path, prev_sect=None):
        super().__init__(screen, prev_sect)

        self.sectpath = path + "OutDoor.tmx"

        self.load_sect(self.sectpath)
        self.init_OFFSET((50, 100), (-170, 40))


class Kitchen(mapcontainer.map.Sect):
    back_point = {
        "OutDoor": "OutDoorBk1"
    }

    def __init__(self, screen, path, prev_sect=None):
        super().__init__(screen, prev_sect)

        self.sectpath = path + "Kitchen.tmx"

        self.load_sect(self.sectpath)
        self.init_OFFSET((60, 120), (-150, 100))


class Toilet(mapcontainer.map.Sect):
    back_point = {
        "OutDoor": "OutDoorBk2"
    }

    def __init__(self, screen, path, prev_sect=None):
        super().__init__(screen, prev_sect)

        self.sectpath = path + "Toilet.tmx"

        self.load_sect(self.sectpath)
        self.init_OFFSET((0, 120), (-170, 120))
