import abc
import sys

import pygame

import gamemanage.effect
from view.playerview import *

from hud import *


class Part(abc.ABC):
    next = 0
    is_changing_part = False

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def event_action(self):
        pass

    @abc.abstractmethod
    def pressing_key(self):
        pass


class Start(Part):
    def __init__(self, screen, gamemap):
        self.screen = screen
        self.gamemap = gamemap

        self.player = PlayerView.get_instance()

        pygame.mixer.music.load("Assets/Sound/rain.mp3")

        self.startmenu = StartMenu(screen)
        self.title_start = self.startmenu.get_start_title()
        self.elements = self.startmenu.get_elements()

        self.alpha = 0
        self.next = 0
        self.choice = 1

    def __fade_in(self, ls):
        if self.alpha == 255:
            return

        self.alpha += 1
        gamemanage.effect.Effect.set_opacity(self.screen, ls, self.alpha)

    def __redraw_other(self):
        self.gamemap.sect.redraw()
        self.player.update_player()

    def __fade_out(self, ls):
        if self.alpha <= 0:
            return

        if self.gamemap.sect.is_created:
            self.__redraw_other()

        self.alpha -= 1
        gamemanage.effect.Effect.set_opacity(self.screen, ls, self.alpha)

    def pressing_key(self):
        if self.next != 3 or self.alpha != 255:
            return

    def __check_choice(self):
        if self.choice == 1:
            self.next = 4

        elif self.choice == 3:
            sys.exit()

    def event_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.next != 3 or self.alpha != 255:
                    return

                key = event.key
                self.__move_cur(key)

    def __move_cur(self, key):
        if key == pygame.K_RETURN:
            self.startmenu.pointer.play_choose_sound()
            self.__check_choice()
            return

        elif key == pygame.K_w:
            if self.choice == 1:
                return
            self.choice -= 1

        elif key == pygame.K_s:
            if self.choice == 3:
                return
            self.choice += 1

        else:
            return

        print(self.choice)

        self.__redraw_other()
        self.startmenu.draw_elements()
        self.startmenu.change_choice(self.choice)

    def __setup(self):
        gamemap = self.gamemap
        player = self.player

        gamemap.sect.create()

        try:
            start_point = gamemap.sect.get_spawn_point()
        except AttributeError:
            start_point = gamemap.sect.get_start_point()

        player.set_position(start_point)

        player.update_player()

        pygame.display.update()
        pygame.time.wait(1000)

    def destroying(self):
        self.is_changing_part = True

        x, y = self.player.get_position()
        self.player.set_position((x - 50, y))
        self.player.presenter.set_img("left1")

    def update(self):
        if self.next == 0:
            self.__fade_in([self.title_start])
            if self.alpha == 255:
                self.next = 1

        if self.next == 1:
            self.screen.fill((0, 0, 0))
            self.__fade_out([self.title_start])
            if self.alpha <= 0:
                self.alpha = 0
                self.next = 2

        if self.next == 2:
            self.__setup()
            self.next = 3

        if self.next == 3:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(1)
            self.__fade_in(self.elements.values())
            if self.alpha == 255 and not self.startmenu.pointer.is_set:
                self.startmenu.change_choice(1)

        if self.next == 4:
            self.__fade_out(self.elements.values())
            if self.alpha <= 0:
                self.destroying()


class FirstPart(Part):
    def __init__(self, screen, gamemap):
        pygame.mixer.music.load(f"Assets/Music/Lily.mp3")
        pygame.mixer.music.play(1)

        self.screen = screen
        self.gamemap = gamemap
        self.player = PlayerView.get_instance()

    def event_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def pressing_key(self):
        keys = pygame.key.get_pressed()

        self.player.moving(keys)

    def handle_change_sect(self):
        mapname = self.gamemap.sect.in_area(self.player.get_rect())

        current = self.gamemap.sect

        self.gamemap.change_sect(mapname)

        if self.gamemap.sect == current:
            return

        self.gamemap.sect.create()
        self.repos_player()

    def repos_player(self):
        """Place player in map section start point"""
        start_pos = self.gamemap.sect.get_start_point()

        self.player.set_position(start_pos)
        self.player.update_player()

    def update(self):
        self.handle_change_sect()
