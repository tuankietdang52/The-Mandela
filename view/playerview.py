import pygame
import entity.playercontainer
import mapcontainer.map
import presenter

from presenter import PlayerPresenter


class PlayerView(pygame.sprite.Sprite):
    _instance = None
    screen = None
    gamemap = None

    def __init__(self):
        """
        Call init instead.
        :exception RuntimeError: when calling
        """
        pygame.sprite.Sprite.__init__(self)
        raise RuntimeError("Please call init() when init instance")

    # Singleton init #

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise TypeError("Must init instance first")

        return cls._instance

    @classmethod
    def init(cls, screen, gamemap, health):
        """
        Init instance for Player
        :param pygame.Surface screen: game screen
        :param mapcontainer.map.Map gamemap:
        :param float health:
        """

        if cls._instance is not None:
            print("player is created before")
            return cls._instance

        cls._instance = cls.__new__(cls)
        pygame.sprite.Sprite.__init__(cls.get_instance())

        cls.screen = screen
        cls.gamemap = gamemap

        cls.presenter = PlayerPresenter(cls, screen, health)

        return cls._instance

    def set_position(self, pos: tuple[int, int]):
        self.presenter.set_position(pos)

    def get_position(self):
        return self.presenter.get_position()

    def get_presenter(self) -> presenter.PlayerPresenter:
        return self.presenter

    def get_rect(self) -> pygame.rect.Rect:
        return self.presenter.get_rect()

    def set_map(self, gamemap: mapcontainer.map.Map):
        self.gamemap = gamemap

    def update_player(self):
        size = self.presenter.get_size()
        pos = self.presenter.get_position()

        self.draw(pos, size)
        # pygame.draw.rect(self.screen, (0, 255, 0), self.get_rect())

    def draw(self, pos: tuple[float, float], size: tuple[float, float] = None):
        if size is None:
            size = self.presenter.get_size()
            self.presenter.set_size(size)

        else:
            self.presenter.set_size(size)

        img = self.presenter.get_img()

        self.gamemap.sect.redraw()
        self.screen.blit(img, pos)

    def moving(self, keys):
        self.presenter.handle_moving(keys)
        self.update_player()
