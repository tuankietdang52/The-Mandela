import abc
import os
import pytmx
import view


class Map(abc.ABC):
    startpoint = None
    walls = list()

    map = None

    def __init__(self, screen, path):
        self.screen = screen
        self.path = path
        self.player = view.PlayerView.get_instance().get_model()

        if os.getcwd() == "C:\\Users\\ADMIN\\PycharmProjects\\Nightmare":
            self.map = pytmx.load_pygame(path)

    @abc.abstractmethod
    def init_obj_point(self):
        pass

    @abc.abstractmethod
    def update_map(self):
        pass
