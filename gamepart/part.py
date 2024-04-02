import abc
import sys
import pygame as pg
import gamemanage.game as gm

from hud import *


class Part(abc.ABC):
    next = 0
    to_next = True

    is_changing_part = False
    is_open_board = False

    gamemap = None
    player = None
    screen = None

    enemies = list()

    @abc.abstractmethod
    def begin(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def event_action(self):
        pass

    @abc.abstractmethod
    def pressing_key(self):
        pass

    @abc.abstractmethod
    def manage_progess(self):
        pass

    def handle_change_sect(self):
        mapname = self.gamemap.sect.in_area(self.player.get_rect())

        current = self.gamemap.sect

        self.gamemap.change_sect(mapname)

        if self.gamemap.sect == current:
            return

        self.update_list_entities()
        self.gamemap.sect.create()
        self.repos_player()

        gm.Manager.update_UI_ip()

    def add_enemy(self, enemy: pg.sprite.Sprite):
        self.enemies.append(enemy)
        self.update_list_entities()

    def remove_enemy(self, enemy: pg.sprite.Sprite):
        self.enemies.remove(enemy)
        self.update_list_entities()

    def update_list_entities(self):
        gm.Manager.appear_entities.empty()
        for enemy in self.enemies:
            if enemy.is_appear():
                gm.Manager.appear_entities.add(enemy)

    def repos_player(self):
        """Place player in map section start point"""
        start_pos = self.gamemap.sect.get_start_point()

        self.player.set_position(start_pos)
        self.player.update()

    def create_board_text(self, text):
        if self.is_open_board:
            return

        self.is_open_board = True
        pos = self.screen.get_width() / 2 + 10, self.screen.get_height() - 100

        size = self.screen.get_width() - 20, self.screen.get_height() - 500

        board = BoardText(self.screen, text, 20, pos, size)

        pg.display.update(board.rect)

        while self.is_open_board:
            self.__check_closing_board()

        gm.Manager.update_UI_ip()

    def __check_closing_board(self):
        for event in pg.event.get():
            """Prevent game to freezing itself"""
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if self.is_open_board and event.key == pg.K_RETURN:
                    self.is_open_board = False
