import pygame as pg
import src.entity.playercontainer as enplayer
import src.gamemanage.game as gm

from src.pjenum import EState


class PlayerPresenter:
    frame = 0

    def __init__(self, view, screen: pg.surface.Surface, health: float):
        self.model = enplayer.Player(screen, health)
        self.view = view

    def set_image(self, image: str | pg.surface.Surface):
        self.model.set_image(image)

    def get_image(self):
        return self.model.get_image()

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

    def set_position(self, pos: tuple[int, int] | pg.math.Vector2):
        self.model.set_position(pos)

    def get_position(self) -> pg.math.Vector2:
        return self.model.get_position()

    def set_size(self, size: tuple[int, int]):
        self.model.set_size(size)

    def get_size(self) -> tuple[int, int]:
        return self.model.get_size()

    def get_rect(self):
        return self.model.get_rect()

    def set_sound_effect(self, sound_effect):
        self.model.set_sound_effect(sound_effect)

    def get_sound_effect(self) -> pg.mixer.Sound:
        return self.model.get_sound_effect()

    def get_voice(self, text: str) -> pg.mixer.Sound:
        return self.model.get_voice(text)

    def moving_animation(self, direction):
        self.set_sound_effect("../Assets/Sound/Other/footstep.mp3")

        if self.frame < 20:
            index = 1

        else:
            index = 0

        self.frame += 1
        if self.frame > 40:
            self.frame = 0
            self.get_sound_effect().play()

        self.model.set_image(direction + str(index))

    def handle_moving(self, keys):
        if self.model.get_state() != EState.FREE:
            return

        velocity = pg.math.Vector2()

        speed = self.model.get_speed()

        if keys[pg.K_w]:
            velocity.y = -speed
            direction = "up"

        elif keys[pg.K_d]:
            velocity.x = speed
            direction = "right"

        elif keys[pg.K_a]:
            velocity.x = -speed
            direction = "left"

        elif keys[pg.K_s]:
            velocity.y = speed
            direction = "down"

        else:
            return

        if self.model.can_move(velocity):
            self.model.moving(velocity)
            self.moving_animation(direction)
            gm.Manager.update_UI_ip()
