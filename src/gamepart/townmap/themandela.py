import sys
import pygame as pg
import src.gamepart.part as gp
import src.gamemanage.game as gm
import src.gamemanage.effect as ge
import src.mapcontainer.housenormal as mphouse


class TheMandela(gp.Part):
    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen)

        self.can_press_key = True
        self.setup()

    def setup(self):
        pg.mixer.music.stop()

    def event_action(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if not self.can_press_key:
                    return

                if event.key == pg.K_RETURN and self.is_open_board:
                    self.closing_board()

    def pressing_key(self):
        if self.is_open_board:
            return

        if not self.can_press_key:
            return

        keys = pg.key.get_pressed()

        self.player.moving(keys)

    def update(self):
        if self.is_open_board:
            return

        self.handle_change_sect()
        self.manage_progess()

    def manage_progess(self):
        progess = self.get_progess_index()

        if progess == 0:
            self.__waking_up()
            self.next()

        elif progess == 1:
            self.__get_up()
            self.next()

    def __waking_up(self):
        path = "../Assets/Sound/GrabielVoice/"
        voice1 = pg.mixer.Sound(f"{path}voice1.mp3")
        voice2 = pg.mixer.Sound(f"{path}voice2.mp3")

        self.create_board_text("Viole", voice1)
        self.create_board_text("Viole", voice1)
        self.create_board_text("Wake up", voice2)
        self.create_board_text("Viole", voice1)
        self.create_board_text("Wake up", voice2)

    def __get_up(self):
        gm.Manager.set_map(mphouse.HouseNormal(self.screen))
        gm.Manager.gamemap.sect.create()
        gm.Manager.gamemap.sect.set_opacity(0)

        ge.Effect.fade_in_screen()
