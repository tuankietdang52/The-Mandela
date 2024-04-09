import abc
import sys

import src.gamemanage.game as gm
import src.view.baseview as vw
import src.mapcontainer.map as mp
import src.view.player.playerview as pv

from src.hud import *


class Part(abc.ABC):
    __progess = 0
    to_next = True

    is_open_board = False
    can_press_key = False
    is_occur_start_event = False

    nextpart = None

    enemies = list()
    special_enemies = set()

    def __init__(self, screen: pg.surface.Surface):
        self.__clean_previous_part()

        self.screen = screen
        self.player = pv.PlayerView.get_instance()

    def __clean_previous_part(self):
        self.enemies.clear()
        self.special_enemies.clear()
        gm.Manager.clear_entities()

    @abc.abstractmethod
    def setup(self):
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

    def set_progess_index(self, progess_index: int):
        self.__progess = progess_index
        self.is_occur_start_event = False

    def next(self):
        self.__progess += 1
        self.is_occur_start_event = False

    def previous(self):
        self.__progess -= 1

    def get_progess_index(self) -> int:
        return self.__progess

    def handle_change_sect(self):
        gamemap = gm.Manager.gamemap

        if gamemap is None:
            return

        mapname = gamemap.sect.in_area(self.player.get_rect())

        current = gamemap.sect

        gamemap.change_sect(mapname)

        if gamemap.sect == current:
            return

        self.update_list_entities()
        gamemap.sect.create()
        self.repos_player()

        gm.Manager.update_UI_ip()

    def add_enemy(self, enemy: vw.BaseView):
        self.enemies.append(enemy)
        self.update_list_entities()

    def remove_enemy(self, enemy: vw.BaseView):
        self.enemies.remove(enemy)
        self.update_list_entities()

    def add_special_enemy(self, name: str, enemy: vw.BaseView):
        self.special_enemies.add((name, enemy))

    def get_special_enemy(self, name: str) -> vw.BaseView | None:
        for enemy in self.special_enemies:
            if enemy[0] == name:
                return enemy[1]

        return None

    def remove_special_enemy(self, name: str | vw.BaseView):
        if type(name) is vw.BaseView:
            self.special_enemies.remove(name)
            return

        for enemy in self.special_enemies:
            if enemy.name == name:
                self.special_enemies.remove(enemy)
                break

    def update_list_entities(self):
        gm.Manager.appear_entities.empty()
        for enemy in self.enemies:
            if enemy.is_appear():
                gm.Manager.appear_entities.add(enemy)

    def repos_player(self):
        """Place player in map section start point"""
        start_pos = gm.Manager.gamemap.sect.get_start_point()

        self.player.set_position(start_pos)
        self.player.update()

    def create_board_text(self, text: str, sound: pg.mixer.Sound = None):
        if self.is_open_board:
            return

        if sound is not None:
            sound.play()

        self.is_open_board = True
        pos = self.screen.get_width() / 2 + 10, self.screen.get_height() - 100

        size = self.screen.get_width() - 20, self.screen.get_height() - 500

        board = BoardText(self.screen, text, 20, pos, size)

        pg.display.update(board.rect)

        while self.is_open_board:
            self.__check_closing_board()

        if sound is not None:
            sound.stop()

        gm.Manager.update_UI_ip()

    def closing_board(self):
        self.is_open_board = False
        gm.Manager.update_UI_ip()

    def __check_closing_board(self):
        for event in pg.event.get():
            """Prevent game to freezing itself"""
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if self.is_open_board and event.key == pg.K_RETURN:
                    self.is_open_board = False
