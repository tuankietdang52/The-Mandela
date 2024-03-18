import pygame
import entity.playercontainer
import mapcontainer.map

from presenter import PlayerPresenter


class PlayerView(pygame.sprite.Sprite):
    _instance = None

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
            raise NotImplementedError("Must init instance first")

        return cls._instance

    @classmethod
    def init(cls, screen, health, gamemap):
        """
        Init instance for Player
        :param float health:
        :param pygame.Surface screen: game screen
        :param mapcontainer.Map gamemap: game map
        """

        if cls._instance is not None:
            print("player is created before")
            return cls._instance

        cls._instance = cls.__new__(cls)
        pygame.sprite.Sprite.__init__(cls.get_instance())

        cls.screen = screen

        cls.presenter = PlayerPresenter(health, cls, screen, gamemap)

        return cls._instance

    def moving(self, keys):
        self.presenter.handle_moving(keys)
        self.update_player()

    def update_player(self):
        size = self.presenter.get_size()
        pos = self.presenter.model.centerx, self.presenter.model.centery

        self.draw(pos, size)

    def get_model(self) -> entity.playercontainer.Player:
        return self.presenter.get_model()

    def draw(self, pos, size=None):
        if size is None:
            size = self.presenter.get_size()
            self.presenter.set_size(size)

        else:
            self.presenter.set_size(size)

        img = self.presenter.get_img()

        self.screen.blit(img, pos)

