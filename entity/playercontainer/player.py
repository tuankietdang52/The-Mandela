import os

import pygame

import gamemanage.physic

from pjenum.estate import EState


class Player:
    _instance = None
    __state = EState.FREE
    __speed = 1
    __path = "Assets/Ally/MainChar/"
    animatepth = "left0"

    # Stats
    width, height = (36, 80)

    __health = 0
    __img = None

    x, y = 0, 0

    sound_effect = None

    def __init__(self, screen, health):
        """
        :param pygame.Surface screen: game screen
        :param float health:
        """
        self.screen = screen
        self.__health = health

        if os.getcwd() == "C:\\Users\\ADMIN\\PycharmProjects\\Nightmare":
            self.set_img(self.animatepth)
            self.set_size(self.get_size())

    # Get Set #
    def set_img(self, img, size=None):
        """
        :param str | pygame.Surface img:
        :param tuple[float, float] size:
        """
        paratype = type(img)

        if paratype is pygame.Surface:
            self.__img = img

        if paratype is str:
            self.__img = pygame.image.load(f"{self.__path + img}.png")

        size = self.get_size() if size is None else size

        self.set_size(size)

    def get_img(self) -> pygame.Surface:
        return self.__img

    def set_health(self, health):
        """:param float health:"""
        self.__health = health

    def get_health(self) -> float:
        return self.__health

    def decrease_health(self, damage):
        """:param float damage:"""
        self.__health -= damage

    def get_state(self) -> EState:
        return self.__state

    def set_state(self, state):
        """:param EState state:"""
        self.__state = state

    def set_position(self, pos):
        """
        :param tuple[float, float] pos:
        """
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

    def set_sound_effect(self, sound_effect):
        """:param pygame.mixer.Sound | str sound_effect:"""
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

        if self.__state != EState.FREE:
            return

        self.set_position(pos)

    def can_move(self, pos) -> bool:
        """
        :param tuple[float, float] pos: next position
        """

        rect = self.__img.get_rect(topleft=pos)

        if gamemanage.physic.Physic.is_collide_wall(rect):
            return False

        return True
