import pygame as pg
import mapcontainer.map as mp
import presenter.player.playerpresenter as playerpr


class PlayerView(pg.sprite.Sprite):
    """Position by topleft"""
    _instance = None
    screen = None
    gamemap = None

    def __init__(self):
        """
        Call init() instead.
        :exception RuntimeError: when calling
        """
        pg.sprite.Sprite.__init__(self)
        raise RuntimeError("Please call init() when init instance")

    # Singleton init #

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise TypeError("Must init instance first")

        return cls._instance

    @classmethod
    def init(cls, screen: pg.Surface, gamemap: mp.Map, health: float):
        """
        Init instance for Player
        """

        if cls._instance is not None:
            print("Player is created before")
            return cls._instance

        cls._instance = cls.__new__(cls)
        pg.sprite.Sprite.__init__(cls.get_instance())

        cls.screen = screen
        cls.gamemap = gamemap

        cls.presenter = playerpr.PlayerPresenter(cls, screen, health)

        return cls._instance

    def set_position(self, pos: tuple[int, int] | pg.math.Vector2):
        self.presenter.set_position(pos)

    def get_position(self) -> pg.math.Vector2:
        return self.presenter.get_position()

    def get_rect(self) -> pg.rect.Rect:
        return self.presenter.get_rect()

    def set_map(self, gamemap: mp.Map):
        self.gamemap = gamemap

    def get_voice(self, voice: str) -> pg.mixer.Sound:
        """
        passing name of voice file (not path) into this function

        wav file required
        """
        return self.presenter.get_voice(voice)

    def update(self):
        self.draw()
        # pg.draw.rect(self.screen, (0, 255, 0), self.get_rect())

    def draw(self):
        image = self.presenter.get_img()
        rect = self.presenter.get_rect()

        self.screen.blit(image, rect)

    def moving(self, keys):
        self.presenter.handle_moving(keys)
