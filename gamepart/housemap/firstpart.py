import sys
import pygame as pg
import gamemanage.game as gm
import gamepart.part as gp
import mapcontainer.housenormal as mphouse
import view.player.playerview as pv
import view.enemy.lilyview as lilyv


class FirstPart(gp.Part):
    def __init__(self, screen, gamemap):
        self.screen = screen
        self.gamemap = gamemap
        self.player = pv.PlayerView.get_instance()

    def begin(self):
        pg.mixer.music.load(f"Assets/Music/Lily.mp3")
        pg.mixer.music.play(True)

    def event_action(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN and self.is_open_board:
                    self.__closing_board()

    def __closing_board(self):
        self.is_open_board = False
        gm.Manager.update_UI_ip()

    def pressing_key(self):
        if self.is_open_board:
            return

        keys = pg.key.get_pressed()

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
            if type(self.gamemap.sect) is not mphouse.Kitchen:
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
            start_pos = pg.math.Vector2(370 - offset[0], 550 - offset[1])
            lily = lilyv.LilyView(self.screen, self.gamemap, start_pos)
            self.add_enemy(lily)

            self.next = 4

    def __tutorial(self):
        self.create_board_text("Press AWDS to move, F to interact, Enter to next")
        self.create_board_text("I feel hungry. Maybe i'll go get some food")

    def __checking_fridge(self):
        sect = self.gamemap.sect
        if type(sect) is not mphouse.Kitchen:
            return False

        area = sect.get_area("Fridge")

        keys = pg.key.get_pressed()

        if area.is_overlap(self.player.get_rect()) and keys[pg.K_f]:
            return True

        return False
