import pygame
from entity.playercontainer import Player
from pjenum import EState


class PlayerPresenter:
    def __init__(self, health, view):
        self.model = Player.init(health)
        self.view = view

    def set_health(self, health):
        """:param float health:"""
        self.model.set_health(health)

    def get_health(self) -> float:
        return self.get_health()

    def decrease_health(self, damage):
        """:param float damage:"""
        self.model.decrease_health()

    def get_state(self) -> EState:
        return self.get_state()

    def set_state(self, state):
        """:param EState state:"""
        self.model.set_state(state)

    def set_position(self, x, y):
        self.model.set_position(x, y)

    def get_position(self) -> tuple[float, float]:
        return self.model.get_position()

    def handle_moving(self, keys):
        x, y = self.model.get_position()
        speed = self.model.get_speed()

        if keys[pygame.K_w]:
            self.model.moving(x, y - speed)

        elif keys[pygame.K_d]:
            self.model.moving(x + speed, y)

        elif keys[pygame.K_a]:
            self.model.moving(x - speed, y)

        elif keys[pygame.K_s]:
            self.model.moving(x, y + speed)

        else:
            return