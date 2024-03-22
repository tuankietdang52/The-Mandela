import os

import pygame

import gamemanage.physic

from pjenum.estate import EState


class Player:
    _instance = None
    __speed = 1
    __path = "Assets/Ally/MainChar/"
    animatepth = "sitleft"

    sound_effect = None

    def __init__(self, screen: pygame.Surface, health: float):
        self.screen = screen
        self.__health = health
        self.__img = None
        self.__state = EState.BUSY
        self.width, self.height = (36, 80)

        self.x, self.y = (0, 0)

        if os.getcwd() == "C:\\Users\\ADMIN\\PycharmProjects\\Nightmare":
            self.set_img(self.animatepth)
            self.set_size(self.get_size())

    # Get Set #
    def set_img(self, img: str | pygame.Surface, size: tuple[float, float] = None):
        paratype = type(img)

        if paratype is pygame.Surface:
            self.__img = img

        if paratype is str:
            self.__img = pygame.image.load(f"{self.__path + img}.png")

        size = self.get_size() if size is None else size

        self.set_size(size)

    def get_img(self) -> pygame.Surface:
        return self.__img

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

    def set_position(self, pos: tuple[float, float]):
        self.x, self.y = pos

    def get_position(self) -> tuple[float, float]:
        return self.x, self.y

    def set_speed(self, speed):
        """
        :param int speed:
        """
        self.__speed = speed

    def get_speed(self) -> int:
        return self.__speed

    def set_size(self, size):
        """
        :param tuple[float, float] size:
        """
        self.width, self.height = size
        self.__img = pygame.transform.scale(self.__img, size)

    def get_size(self) -> tuple[float, float]:
        return self.width, self.height

    def get_rect(self) -> pygame.rect.Rect:
        return self.get_img().get_rect(topleft=self.get_position())

    def set_sound_effect(self, sound_effect: pygame.mixer.Sound | str):
        if type(sound_effect) is str:
            self.sound_effect = pygame.mixer.Sound(sound_effect)
        else:
            self.sound_effect = sound_effect

    def get_sound_effect(self) -> pygame.mixer.Sound:
        return self.sound_effect

    # Movement #
    def moving(self, pos):
        """
        :param tuple[float, float] pos: next position
        """
        self.set_position(pos)

    def can_move(self, pos) -> bool:
        """
        :param tuple[float, float] pos: next position
        """

        rect = self.__img.get_rect(topleft=pos)

        if gamemanage.physic.Physic.is_collide_wall(rect):
            return False

        return True
