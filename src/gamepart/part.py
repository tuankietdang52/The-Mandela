import abc
import sys

import src.gamemanage.game as gm
import src.gamemanage.effect as ge
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
    can_change_map = False

    nextpart = None

    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen
        self.player = pv.PlayerView.get_instance()
        self.enemies = list()
        self.special_enemies = set()

        self.update_list_entities()

    @abc.abstractmethod
    def setup(self):
        pass

    def update(self):
        if self.is_open_board:
            return

        self.handle_change_map()
        self.handle_change_sect()
        self.manage_progess()

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

    def handle_change_map(self):
        if not self.can_change_map:
            return

        sect = gm.Manager.gamemap.sect

        area = sect.in_area(self.player.get_rect())
        keys = pg.key.get_pressed()

        if not keys[pg.K_f]:
            return

        map_comp = gm.Manager.gamemap.get_next_map(area)
        if map_comp is None:
            return

        next_map, text = map_comp

        self.create_board_text(text)
        choice = self.create_accept_board().yes_choice

        if choice:
            self.changing_map(next_map)

    def changing_map(self, next_map: mp.Map):
        gm.Manager.set_map(next_map)
        ge.Effect.fade_out_screen()

        gm.Manager.gamemap.sect.create()
        gm.Manager.gamemap.sect.set_opacity(0)

        pos = gm.Manager.gamemap.sect.get_start_point()
        self.player.set_position(pos)

        gm.Manager.wait(1)
        ge.Effect.fade_in_screen()

    def handle_change_sect(self):
        gamemap = gm.Manager.gamemap

        if gamemap is None:
            return

        sect_name = gamemap.sect.in_area(self.player.get_rect())

        current = gamemap.sect

        gamemap.change_sect(sect_name)

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

        if len(self.enemies) == 0:
            gm.Manager.clear_entities()
            return

        for enemy in self.enemies:
            if enemy.is_appear():
                gm.Manager.appear_entities.add(enemy)

    def repos_player(self):
        """Place player in map section start point"""
        start_pos = gm.Manager.gamemap.sect.get_start_point()

        self.player.set_position(start_pos)
        self.player.update()

    def create_board_text(self, text: str, sound: pg.mixer.Sound = None):
        """
        Create a board contain text inside
        If you want to go to new line in the text, using ' |sometext' to do it
        """

        if self.is_open_board:
            return

        if sound is not None:
            sound.play()

        self.is_open_board = True
        pos = self.screen.get_width() / 2 + 10, self.screen.get_height() - 100

        size = self.screen.get_width() - 20, self.screen.get_height() - 500

        board = BoardText(self.screen, text, 20, pos, size)
        board.draw()

        pg.display.update(board.rect)

        while self.is_open_board:
            self.__check_closing_board()

        if sound is not None:
            sound.stop()

        self.screen.fill((0, 0, 0))
        gm.Manager.update_UI_ip()

    def create_accept_board(self) -> AcceptBoard:
        self.is_open_board = True

        pos = self.screen.get_width() / 2 + 10, self.screen.get_height() - 100

        size = self.screen.get_width() - 20, self.screen.get_height() - 500

        board = AcceptBoard(self.screen, pos, size)
        board.draw()

        pg.display.update(board.rect)

        while self.is_open_board:
            board.changing_choice()
            self.__check_closing_board()

            if not self.is_open_board:
                board.pointer.play_choose_sound()

        self.screen.fill((0, 0, 0))
        gm.Manager.update_UI_ip()
        return board

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
