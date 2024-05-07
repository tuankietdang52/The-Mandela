import pygame as pg
import src.gamemanage.game as gm
import src.hud.playerhud as plhud


from src.pjenum.estate import EState
from src.utils import *
from src.eventhandle import *


class Player(pg.sprite.Sprite):
    _instance = None
    __path = "../Assets/Ally/Viole/"
    animatepth = "walk0"
    __frame = 0

    def __init__(self, screen: pg.surface.Surface, groups: pg.sprite.Group):
        super().__init__(groups)
        self.screen = screen
        self.__state = EState.FREE

        self.size = 36, 80
        self.__speed = 1.5
        self.position = pg.math.Vector2()

        self.image = pg.image.load(f"{self.__path + self.animatepth}.png").convert_alpha()
        self.set_size(self.size)
        self.rect = self.image.get_rect()

        self.direction = "left"

        self.interact = EventHandle()

        self.hungry_bar: plhud.Bar | None = None
        self.sanity_bar: plhud.Bar | None = None
        self.full_time = 0

        self.busy_time = 0

    def init_hud(self, hud_groups: pg.sprite.Group):
        self.hungry_bar = plhud.Bar("hungry", pg.math.Vector2(10, 0), (255, 126, 1), self, hud_groups)
        self.sanity_bar = plhud.Bar("sanity", pg.math.Vector2(10, 50), (201, 0, 255), self, hud_groups)

    def update(self, *args, **kwargs):
        if self.__state == EState.DEAD:
            return

        self.countdown_full_buff()
        self.countdown_busy_time()
        self.decrease_hungry_amount(0.003)
        self.__check_hungry()

    def __check_hungry(self):
        if self.hungry_bar is None:
            return

        if self.get_hungry_amount() <= 0:
            self.set_state(EState.DEAD)

    # Get Set #
    def set_image(self, image: str | pg.surface.Surface, size: tuple[float, float] = None):
        size = self.get_size() if size is None else size

        if type(image) is str:
            self.image = pg.image.load(f"{self.__path + image}.png").convert_alpha()
        else:
            self.image = image

        self.set_size(size)

    def get_image(self) -> pg.surface.Surface:
        return self.image

    def flip_horizontal(self):
        self.image = pg.transform.flip(self.image, True, False)

    def get_state(self) -> EState:
        return self.__state

    def set_state(self, state: EState):
        self.__state = state
        if self.__state == EState.DEAD:
            self.dying()

    def set_position(self, pos: tuple[float, float] | pg.math.Vector2):
        if type(pos) is pg.math.Vector2:
            self.position = pos
        else:
            self.position = pg.math.Vector2(pos)

        self.rect = self.image.get_rect(center=self.position)

    def get_position(self) -> pg.math.Vector2:
        return self.position

    def set_speed(self, speed: float):
        self.__speed = speed

    def get_speed(self) -> float:
        return self.__speed

    def set_size(self, size: tuple[int, int]):
        self.image = pg.transform.scale(self.image, size)

    def get_size(self) -> tuple[int, int]:
        return self.image.get_size()

    def get_rect(self) -> pg.rect.Rect:
        return self.get_image().get_rect(center=self.get_position())

    def get_voice(self, voice: str) -> pg.mixer.Sound:
        path = f"../Assets/Sound/VioleVoice/{voice}.wav"
        return pg.mixer.Sound(path)

    # FOOD

    def increase_hungry_amount(self, amount: float):
        if self.hungry_bar is None:
            return

        self.hungry_bar.increase_amount(amount)

    def increase_sanity_amount(self, amount: float):
        if self.sanity_bar is None:
            return

        self.sanity_bar.increase_amount(amount)

    def decrease_hungry_amount(self, amount: float):
        if self.hungry_bar is None:
            return

        if self.full_time > 0:
            return

        self.hungry_bar.decrease_amount(amount)

    def decrease_sanity_amount(self, amount: float):
        if self.sanity_bar is None:
            return

        self.sanity_bar.decrease_amount(amount)

    def set_hungry_amount(self, amount: float):
        if self.hungry_bar is None:
            return

        self.hungry_bar.set_amount(amount)

    def set_sanity_amount(self, amount: float):
        if self.sanity_bar is None:
            return

        self.sanity_bar.set_amount(amount)

    def get_hungry_amount(self) -> float:
        if self.hungry_bar is None:
            return 0

        return self.hungry_bar.get_amount()

    def get_sanity_amount(self) -> float:
        if self.sanity_bar is None:
            return 0

        return self.sanity_bar.get_amount()

    def set_full_time(self, time: float):
        self.full_time += time

    def set_busy_time(self, time: float):
        self.busy_time += time

    def countdown_full_buff(self):
        if self.full_time > 0:
            time = gm.Game.get_time()
            self.full_time -= time

        if self.full_time == 0:
            self.full_time = 0

    def countdown_busy_time(self):
        if self.busy_time > 0:
            time = gm.Game.get_time()
            self.busy_time -= time

        if self.busy_time == 0:
            self.busy_time = 0

    # Movement #
    def __get_reverse_animate(self) -> str:
        direction_tuple = [
            ["down", "up"],
            ["left", "right"]
        ]

        for di in direction_tuple:
            if self.direction == di[0]:
                return di[1]

            elif self.direction == di[1]:
                return di[0]

        return ""

    def action_key(self, keys: pg.key.ScancodeWrapper):
        self.__handle_moving(keys)

        if keys[pg.K_f]:
            self.interact.invoke()

    def __is_moving(self, keys: pg.key.ScancodeWrapper):
        if keys[pg.K_w] or keys[pg.K_s] or keys[pg.K_a] or keys[pg.K_d]:
            return True

        return False

    def __handle_moving(self, keys: pg.key.ScancodeWrapper):
        if self.__state != EState.FREE and self.__state != EState.PANIC:
            return

        speed = self.get_speed()
        velocity = pg.math.Vector2()

        if keys[pg.K_w]:
            velocity.y = -speed
            self.direction = "up"

        elif keys[pg.K_d]:
            velocity.x = speed
            self.direction = "right"

        elif keys[pg.K_a]:
            velocity.x = -speed
            self.direction = "left"

        elif keys[pg.K_s]:
            velocity.y = speed
            self.direction = "down"

        else:
            return

        if not self.can_move(velocity):
            return

        if self.__state == EState.PANIC:
            self.direction = self.__get_reverse_animate()
            velocity = velocity[0] * -1, velocity[1] * -1

        self.__moving(velocity)
        self.__moving_animation(self.direction)

    def can_move(self, velocity: pg.math.Vector2) -> bool:
        next_pos = self.position + velocity

        rect = self.image.get_rect(center=next_pos)

        if Physic.is_collide_wall(rect):
            return False

        if Physic.is_collide_object(rect):
            return False

        return True

    def __moving(self, velocity: pg.math.Vector2):
        position = self.get_position() + velocity
        self.set_position(position)

        self.decrease_hungry_amount(0.001)

    def __moving_animation(self, direction: str):
        if self.__frame < 20:
            index = 1

        else:
            index = 0

        self.__frame += 1
        if self.__frame > 40:
            self.__frame = 0
            SoundUtils.play_sound("../Assets/Sound/Other/footstep.mp3")

        if direction == "left" or direction == "right":
            name_animate = "walk"
        else:
            name_animate = direction

        self.set_image(name_animate + str(index))
        if direction == "left":
            self.flip_horizontal()

    def dying(self):
        pos = self.get_position()
        self.set_image("dead", (203, 51))
        self.set_position(pos)

    def reset(self):
        self.set_image("walk0", (36, 80))
        self.set_state(EState.FREE)
        self.direction = "left"
        self.set_speed(1.5)

        self.set_full_time(0)
        self.increase_hungry_amount(100)
        self.increase_sanity_amount(100)
        self.hungry_bar.set_visible(True)
        self.sanity_bar.set_visible(True)
