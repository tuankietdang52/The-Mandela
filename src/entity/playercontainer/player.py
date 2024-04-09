import os
import pygame as pg
import src.gamemanage.physic as gph

from src.pjenum.estate import EState


class Player:
    _instance = None
    __speed = 1.5
    __path = "../Assets/Ally/Viole/"
    animatepth = "left1"

    sound_effect = None

    def __init__(self, screen: pg.surface.Surface, health: float):
        self.screen = screen
        self.__health = health
        self.__image = None
        self.__state = EState.FREE
        self.width, self.height = (36, 80)

        self.position = pg.math.Vector2()

        if os.getcwd() == "C:\\Users\\ADMIN\\PycharmProjects\\Nightmare\\src":
            self.set_image(self.animatepth)
            self.set_size(self.get_size())

    # Get Set #
    def set_image(self, image: str | pg.surface.Surface, size: tuple[float, float] = None):
        paratype = type(image)

        if paratype is pg.surface.Surface:
            self.__image = image

        if paratype is str:
            self.__image = pg.image.load(f"{self.__path + image}.png")

        size = self.get_size() if size is None else size

        self.set_size(size)

    def get_image(self) -> pg.surface.Surface:
        return self.__image

    def set_health(self, health: float):
        self.__health = health

    def get_health(self) -> float:
        return self.__health

    def decrease_health(self, damage: float):
        self.__health -= damage

    def get_state(self) -> EState:
        return self.__state

    def set_state(self, state: EState):
        self.__state = state

    def set_position(self, pos: tuple[float, float] | pg.math.Vector2):
        if type(pos) is pg.math.Vector2:
            self.position = pos
        else:
            self.position = pg.math.Vector2(pos)

    def get_position(self) -> pg.math.Vector2:
        return self.position

    def set_speed(self, speed: int):
        self.__speed = speed

    def get_speed(self) -> int:
        return self.__speed

    def set_size(self, size: tuple[float, float]):
        self.width, self.height = size
        self.__image = pg.transform.scale(self.__image, size)

    def get_size(self) -> tuple[float, float]:
        return self.width, self.height

    def get_rect(self) -> pg.rect.Rect:
        return self.get_image().get_rect(topleft=self.get_position())

    def set_sound_effect(self, sound_effect: pg.mixer.Sound | str):
        if type(sound_effect) is str:
            self.sound_effect = pg.mixer.Sound(sound_effect)
        else:
            self.sound_effect = sound_effect

    def get_sound_effect(self) -> pg.mixer.Sound:
        return self.sound_effect

    def get_voice(self, voice: str) -> pg.mixer.Sound:
        path = f"../Assets/Sound/VioleVoice/{voice}.wav"
        return pg.mixer.Sound(path)

    # Movement #
    def moving(self, velocity: pg.math.Vector2):
        self.position += velocity

    def can_move(self, velocity: pg.math.Vector2) -> bool:
        next_pos = self.position + velocity

        rect = self.__image.get_rect(topleft=next_pos)

        if gph.Physic.is_collide_wall(rect):
            return False

        return True
