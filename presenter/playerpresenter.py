import pygame
import entity.playercontainer
from pjenum import EState


class PlayerPresenter:
    frame = 0

    def __init__(self, health, view, screen, gamemap):
        self.model = entity.Player(health, screen, gamemap)
        self.view = view

    def set_img(self, img):
        self.model.set_img(img)

    def get_img(self):
        return self.model.get_img()

    def set_health(self, health):
        """:param float health:"""
        self.model.set_health(health)

    def get_health(self) -> float:
        return self.get_health()

    def decrease_health(self, damage):
        """:param float damage:"""
        self.model.decrease_health(damage)

    def get_state(self) -> EState:
        return self.get_state()

    def set_state(self, state):
        """:param EState state:"""
        self.model.set_state(state)

    def set_position(self, x, y):
        self.model.set_position(x, y)

    def get_position(self) -> tuple[float, float]:
        return self.model.get_position()

    def set_size(self, size):
        """
        :param tuple[float, float] size:
        :return:
        """
        self.model.set_size(size)

    def get_size(self) -> tuple[float, float]:
        return self.model.get_size()

    def get_model(self) -> entity.Player:
        return self.model

    def moving_animation(self, direction):
        index = 0

        if self.frame < 20:
            index = 1
        else:
            index = 0

        self.frame += 1
        if self.frame > 40:
            self.frame = 0

        self.model.set_img(direction + str(index))

    def handle_moving(self, keys):
        x, y = 0, 0

        speed = self.model.get_speed()

        direction = "down"

        if keys[pygame.K_w]:
            y -= speed
            direction = "up"

        elif keys[pygame.K_d]:
            x += speed
            direction = "right"

        elif keys[pygame.K_a]:
            x -= speed
            direction = "left"

        elif keys[pygame.K_s]:
            y += speed
            direction = "down"

        else:
            return

        if self.model.can_move(x, y):
            self.model.moving(x, y)
            self.moving_animation(direction)
