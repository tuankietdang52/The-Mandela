from pjenum.estate import EState


class Player:
    _instance = None
    __state = EState.FREE
    __speed = 2

    # Stats
    _health = 1000
    x = 0
    y = 0

    def __init__(self):
        """Call init() instead"""
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
            print("playercontainer is created before")
            return cls._instance

        cls._instance = cls.__new__(cls)
        cls._health = health

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

    def set_position(self, x, y):
        """
        :param int x:
        :param int y:
        """
        self.x = x
        self.y = y

    def get_position(self) -> tuple[float, float]:
        return self.x, self.y

    def set_speed(self, speed):
        """
        :param float speed:
        """
        self.__speed = speed

    def get_speed(self) -> float:
        return self.__speed

    # Movement #
    def moving(self, x, y):
        if self.__state != EState.FREE:
            return

        self.set_position(x, y)

