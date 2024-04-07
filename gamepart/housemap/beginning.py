import sys
import pygame as pg

import entity.enemycontainer.lily
import gamemanage.game as gm
import gamemanage.physic as gph
import gamepart.part as gp
import mapcontainer.housenormal as mphouse
import view.enemy.lilyview
import view.player.playerview as pv
import view.enemy.lilyview as lilyv
import movingtype.normalmoving as normv

from tilemap import Area


class BeginStory(gp.Part):
    def __init__(self, screen: pg.surface.Surface, gamemap: mphouse.HouseNormal):
        self.screen = screen
        self.gamemap = gamemap
        self.player = pv.PlayerView.get_instance()

        self.offset = self.gamemap.sect.CAM_OFFSETX, self.gamemap.sect.CAM_OFFSETY

        self.can_press_key = True
        self.begin()

    def begin(self):
        gm.Manager.play_theme("Assets/Music/Lily.mp3")

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
        progess = self.get_progess_index()

        if progess == 0:
            self.__tutorial()
            self.next()

        elif progess == 1:
            if type(self.gamemap.sect) is not mphouse.Kitchen:
                return

            voice = self.player.get_voice("voice2")
            self.create_board_text("Let check the refrigerator", voice)
            self.next()

        elif progess == 2:
            if not self.__checking_fridge():
                return

            self.create_board_text('"Out of food"')
            self.create_board_text("...")
            self.next()

        elif progess == 3:
            self.__finding_lily()

        elif progess == 4:
            self.__to_dream()

        elif progess == 5:
            self.destroying()


    def __tutorial(self):
        self.create_board_text("Press AWDS to move|F to interact|Enter to next")
        voice = self.player.get_voice("voice1")
        self.create_board_text("I feel hungry. Maybe i'll go get some food", voice)

    def __checking_fridge(self):
        sect = self.gamemap.sect
        if type(sect) is not mphouse.Kitchen:
            return False

        area = sect.get_area("Fridge")

        keys = pg.key.get_pressed()

        if area.is_overlap(self.player.get_rect()) and keys[pg.K_f]:
            return True

        return False

    def __finding_lily(self):
        gm.Manager.play_theme("Assets/Sound/rain.mp3")

        voice = pg.mixer.Sound("Assets/Sound/LilyVoice/voice1.wav")
        self.create_board_text("Viole...", voice)

        voice = self.player.get_voice("voice3")
        self.create_board_text("What!? Is that voice come from my bedroom|Is that...|Lily", voice)
        self.__spawnlily()

        self.next()

    def __spawnlily(self):
        start_pos = pg.math.Vector2(570 - self.offset[0], 550 - self.offset[1])

        lily = lilyv.LilyView(self.screen, self.gamemap, mphouse.Room, start_pos)
        self.add_enemy(lily)
        self.add_special_enemy("lily", lily)

    def __to_dream(self):
        if type(self.gamemap.sect) is not mphouse.Room:
            return

        if not self.is_occur_start_event:
            voice = self.player.get_voice("voice4")
            self.create_board_text("Lily ?", voice)
            self.is_occur_start_event = True

        self.__lily_chasing()

    def __lily_chasing(self):
        lily = self.get_special_enemy("lily")
        lily_position = lily.get_position()

        player_rect = self.player.get_rect()
        width, height = 36, 80
        active_area = Area("active",lily_position, width, height)

        if not active_area.is_overlap(player_rect):
            return

        lily.set_position(pg.math.Vector2(lily_position.x, lily_position.y + 185))
        lily.presenter.set_movement(normv.NormalMovement(lily.presenter.model))
        lily.presenter.set_speed(3)

        self.next()

    def destroying(self):
        lily = self.get_special_enemy("lily")
        player_rect = pv.PlayerView.get_instance().get_rect()

        if not gph.Physic.is_collide(player_rect, lily.get_rect()):
            return

        gm.Manager.unload_map()
        # self.is_changing_part = True
        self.next()
