import pytmx


class TileObject:
    def __init__(self, pos, width, height):
        """
        :param tuple[int, int] pos:
        :param float width:
        :param float height:
        """
        self.x, self.y = pos
        self.width = width
        self.height = height
