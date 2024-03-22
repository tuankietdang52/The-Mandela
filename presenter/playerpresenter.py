import pygame
import entity.playercontainer
from pjenum import EState


class PlayerPresenter:
    frame = 0

    def __init__(self, view, screen, health):
        self.model = entity.Player(screen, health)
        self.view = view

    def set_img(self, img):
        self.model.set_img(img)

    def get_img(self):
        return self.model.get_img()

    def set_health(self, health: float):
        self.model.set_health(health)

    def get_health(self) -> float:
        return self.get_health()

    def decrease_health(self, damage: float):
        self.model.decrease_health(damage)

    def set_speed(self, speed: int):
        self.model.set_speed(speed)

    def get_speed(self) -> int:
        return self.model.get_speed()

    def get_state(self) -> EState:
        return self.get_state()

    def set_state(self, state: EState):
        self.model.set_state(state)

    def set_position(self, pos: tuple[int, int]):
        self.model.set_position(pos)

    def get_position(self) -> tuple[float, float]:
        """Get position of player (middle of screen)"""
        return self.model.x, self.model.y

    def set_size(self, size: tuple[float, float]):
        self.model.set_size(size)

    def get_size(self) -> tuple[float, float]:
        return self.model.get_size()

    def get_rect(self):
        return self.model.get_rect()

    def set_sound_effect(self, sound_effect):
        self.model.set_sound_effect(sound_effect)

    def get_sound_effect(self) -> pygame.mixer.Sound:
        return self.model.get_sound_effect()

    def moving_animation(self, direction):
        self.set_sound_effect("Assets/Sound/footstep.mp3")

        if self.frame < 20:
            index = 1

        else:
            index = 0

        self.frame += 1
        if self.frame > 40:
            self.frame = 0
            self.get_sound_effect().play()

        self.model.set_img(direction + str(index))

    def handle_moving(self, keys):
        if self.model.get_state() != EState.FREE:
            return

        x, y = self.model.get_position()

        speed = self.model.get_speed()

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

        if self.model.can_move((x, y)):
            self.model.moving((x, y))
            self.moving_animation(direction)
