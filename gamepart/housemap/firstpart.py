import pygame
import sys
import gamemanage.game
import gamepart.part

from entity.enemycontainer.demon import *
from view.playerview import *
from hud import *


class FirstPart(gamepart.part.Part):
    def __init__(self, screen, gamemap):
        self.screen = screen
        self.gamemap = gamemap
        self.player = PlayerView.get_instance()

    def begin(self):
        pygame.mixer.music.load(f"Assets/Music/Lily.mp3")
        pygame.mixer.music.play(True)

    def event_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.is_open_board:
                    self.__closing_board()

    def __closing_board(self):
        self.is_open_board = False
        gamemanage.game.Manager.update_UI_ip()

    def pressing_key(self):
        if self.is_open_board:
            return

        keys = pygame.key.get_pressed()

        self.player.moving(keys)

    def update(self):
        self.handle_change_sect()

        if self.is_open_board:
            return

        self.manage_progess()

    def manage_progess(self):
        if self.next == 0:
            self.begin()
            self.__tutorial()
            self.next = 1

        elif self.next == 1:
            if type(self.gamemap.sect) is not mapcontainer.housenormal.Kitchen:
                return

            self.create_board_text("Let check the refrigerator")
            self.next = 2

        elif self.next == 2:
            if not self.__checking_fridge():
                return

            self.create_board_text('"Out of food"')
            self.create_board_text("...")
            self.next = 3

        elif self.next == 3:
            offset = self.gamemap.sect.CAM_OFFSETX, self.gamemap.sect.CAM_OFFSETY
            demon = Demon(self.screen, self.gamemap, type(self.gamemap.sect), (370 - offset[0], 550 - offset[1]))
            self.add_enemy(demon)
            self.next = 4

    def __tutorial(self):
        self.create_board_text("Press AWDS to move, F to interact, Enter to next")
        self.create_board_text("I feel hungry. Maybe i'll go get some food")

    def __checking_fridge(self):
        sect = self.gamemap.sect
        if type(sect) is not mapcontainer.housenormal.Kitchen:
            return False

        area = sect.get_area("Fridge")

        keys = pygame.key.get_pressed()

        if area.is_overlap(self.player.get_rect()) and keys[pygame.K_f]:
            return True

        return False
