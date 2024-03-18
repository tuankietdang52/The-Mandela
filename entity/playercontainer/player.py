import os

import pygame

import mapcontainer

from pjenum.estate import EState


class Player:
    _instance = None
    __state = EState.FREE
    __speed = 2
    __path = "Assets/Ally/MainChar/"
    animatepth = "left0"

    # Stats
    x = 0
    y = 0
    width, height = (36, 80)

    __health = 0
    __img = None

    def __init__(self, health, centerx, centery, screen):
        """
        :param float health:
        :param float centerx: set x-axis for camera
        :param float centery: set y-axis for camera
        :param pygame.Surface screen: game screen
        """
        self.__health = health
        self.centerx = centerx
        self.centery = centery
        self.screen = screen

        if os.getcwd() == "C:\\Users\\ADMIN\\PycharmProjects\\Nightmare":
            self.set_img(self.animatepth)
            self.set_size(self.get_size())

    # Get Set #
    def set_img(self, img, size=None):
        """
        :param img: string or Surface:
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

    def set_size(self, size):
        """
        :param tuple[float, float] size:
        :return:
        """
        self.width, self.height = size
        self.__img = pygame.transform.scale(self.__img, size)

    def get_size(self) -> tuple[float, float]:
        return self.width, self.height

    # Movement #
    def moving(self, x, y):
        prev = self.get_position()

        # pygame.draw.rect(self.screen, (0, 255, 255), self.__img.get_rect(topleft=(self.centerx, self.centery)))

        pos = tuple((x - prev[0], y - prev[1]))

        if self.__state != EState.FREE:
            return

        if not self.can_move(self.centerx + pos[0], self.centery + pos[1]):
            return

        self.set_position(x, y)

    def can_move(self, x, y):
        walls = mapcontainer.Map.walls

        center = self.__img.get_rect(topleft=(x, y)).center
        botlf = self.__img.get_rect(topleft=(x, y)).bottomleft
        botrg = self.__img.get_rect(topleft=(x, y)).bottomright

        for wall in walls:
            if (wall.rect.collidepoint(center)
                    or wall.rect.collidepoint(botlf)
                    or wall.rect.collidepoint(botrg)):
                return False

        return True
