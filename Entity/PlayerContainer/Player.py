import pygame

from Enum.EState import EState


class Player(pygame.sprite.Sprite):
    _instance = None
    __state = EState.FREE

    # Stats
    _health = 1000
    x = 0
    y = 0

    def __init__(self):
        """Call init() instead"""
        pygame.sprite.Sprite.__init__(self)
        raise RuntimeError("Call init() instead")

    # Singleton init #

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            return cls.init(1000)
        return cls._instance

    @classmethod
    def init(cls, health):
        """
        Init instance for Player
        :param float health:
        """
        if cls._instance is not None:
            print("PlayerContainer is created before")
            return cls._instance

        cls._instance = cls.__new__(cls)
        cls._health = health
        pygame.sprite.Sprite.__init__(cls._instance)

        return cls._instance

    # Get Set #
    def set_health(self, health):
        """:param float health:"""
        self._health = health

    def get_health(self) -> float:
        return self._health

    def decrease_health(self, damage):
        """:param float damage:"""
        self._health -= damage

    def get_state(self) -> EState:
        return self.__state

    def set_state(self, state):
        """:param EState state:"""
        self.__state = state

    # Movement #
    def moving(self, keys):
        if self.__state != EState.FREE:
            return

        ismoving = True

        if keys[pygame.K_w]:
            self.y += 1

        elif keys[pygame.K_d]:
            self.x += 1

        elif keys[pygame.K_a]:
            self.x -= 1

        elif keys[pygame.K_s]:
            self.y -= 1

        else:
            ismoving = False

        if not ismoving:
            return

        print(f"x: {self.x}\n", f"y: {self.y}\n")

