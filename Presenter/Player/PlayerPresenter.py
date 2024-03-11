from Model.Player.PlayerModel import PlayerModel


class PlayerPresenter:
    _instance = None
    _player = None

    def __init__(self):
        raise RuntimeError("Call init() instead")

    # Singleton init #

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            return cls.init(1000)
        return cls._instance

    @classmethod
    def init(cls, health):
        if cls._instance is not None:
            print("Player is created before")
            return cls._instance

        cls._instance = cls.__new__(cls)
        cls._player = PlayerModel(health)

        return cls._instance

    # Draw #

    def set_health(self, health):
        self._player.set_health(health)

    def get_health(self):
        return self._player.get_health()

    def decrease_health(self, damage):
        self._player.decrease_health(damage)

