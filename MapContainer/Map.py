import abc


class Map(abc.ABC):
    def __init__(self, screen):
        self.screen = screen

    @abc.abstractmethod
    def update_map(self):
        pass
