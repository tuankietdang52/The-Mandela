import sys

import pygame as pg

import src.gamemanage.game as gm
import src.gamemanage.physic as gph
import src.gamepart.part as gp
import src.mapcontainer.housenormal as hsmp
import src.movingtype.normalmoving as normv
import src.view.enemy.lilyview as lilyv
import src.view.player.playerview as pv
import src.gamepart.townmap.themandela as mandela

from src.tilemap import Area


class BeginStory(gp.Part):
    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen)

        self.offset = gm.Manager.gamemap.sect.CAM_OFFSETX, gm.Manager.gamemap.sect.CAM_OFFSETY

        self.can_press_key = True
        self.setup()

    def setup(self):
        gm.Manager.play_theme("../Assets/Music/Lily.mp3")

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

    def manage_progess(self):
        progess = self.get_progess_index()

        if progess == 0:
            self.__tutorial()
            self.next()

        elif progess == 1:
            if type(gm.Manager.gamemap.sect) is not hsmp.Kitchen:
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
        self.create_board_text("Press AWDS to move |F to interact |Enter to next")
        voice = self.player.get_voice("voice1")
        self.create_board_text("I feel hungry. Maybe i'll go get some food", voice)

    def __checking_fridge(self):
        sect = gm.Manager.gamemap.sect
        if type(sect) is not hsmp.Kitchen:
            return False

        area = sect.get_area("Fridge")

        keys = pg.key.get_pressed()

        if area.is_overlap(self.player.get_rect()) and keys[pg.K_f]:
            return True

        return False

    def __finding_lily(self):
        gm.Manager.play_theme("../Assets/Sound/Other/rain.mp3")

        voice = pg.mixer.Sound("../Assets/Sound/LilyVoice/voice1.wav")
        self.create_board_text("Viole...", voice)

        voice = self.player.get_voice("voice3")
        self.create_board_text("What!? Is that voice come from my bedroom |Is that... |Lily", voice)
        self.__spawnlily()

        self.next()

    def __spawnlily(self):
        start_pos = pg.math.Vector2(424 - self.offset[0], 448 - self.offset[1])

        lily = lilyv.LilyView(self.screen, gm.Manager.gamemap, hsmp.Room, start_pos)
        self.add_enemy(lily)
        self.add_special_enemy("lily", lily)

    def __to_dream(self):
        if type(gm.Manager.gamemap.sect) is not hsmp.Room:
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
        active_area = Area("active", lily_position, width, height, gm.Manager.gamemap.sect.areas)

        if not active_area.is_overlap(player_rect):
            return

        pg.mixer.Sound("../Assets/Sound/Other/suprise.mp3").play()

        self.__lily_to_demon(lily)

        self.next()

    def __lily_to_demon(self, lily):
        """
        :param Any lily:
        """

        lily_position = lily.get_position()

        img = pg.image.load("../Assets/Enemy/Demon/bigmouth.png").convert_alpha()
        lily.set_image(img)
        lily.set_size((45, 83))

        lily.set_position(pg.math.Vector2(lily_position.x, lily_position.y + 185))
        lily.presenter.set_movement(normv.NormalMovement(lily.presenter.model))
        lily.presenter.set_speed(4)

    def destroying(self):
        lily = self.get_special_enemy("lily")
        player_rect = pv.PlayerView.get_instance().get_rect()

        if not gph.Physic.is_collide(player_rect, lily.get_rect()):
            return

        self.next()
        self.can_press_key = False
        gm.Manager.unload_map()

        gm.Manager.wait(5)

        gm.Manager.set_part(mandela.TheMandela(self.screen))
