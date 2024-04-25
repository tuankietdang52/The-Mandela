import sys

import pygame as pg

import src.gamemanage.game as gm
import src.gamemanage.physic as gph
import src.gamemanage.effect as ge
import src.gameprogress.part as gp
import src.mapcontainer.housenormal as mphouse
import src.movingtype.normalmoving as normv
import src.gameprogress.townmap.themandela as mandela
import src.hud.hudcomp as hud
import src.entity.thealternate.lily as ll

from src.tilemap import Area
from src.pjenum import *


class BeginStory(gp.Part):
    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen)

        self.can_press_key = True
        self.setup()

    def setup(self):
        self.update_list_entities()
        gm.Manager.play_theme("../Assets/Music/Lily.mp3")

    def event_action(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

    def pressing_key(self):
        player = self.manager.player

        if not self.can_press_key:
            return

        keys = pg.key.get_pressed()

        player.handle_moving(keys)

    def manage_progress(self):
        sect = gm.Manager.get_instance().gamemap.sect
        player = gm.Manager.get_instance().player
        progress = self.get_progress_index()

        if progress == 0:
            self.__tutorial()
            self.next()

        elif progress == 1:
            if type(sect) is not mphouse.Kitchen:
                return

            voice = player.get_voice("voice2")
            hud.HUDComp.create_board_text("Let check the refrigerator", voice)
            self.next()

        elif progress == 2:
            if not self.__checking_fridge():
                return

            hud.HUDComp.create_board_text('"Out of food"')
            hud.HUDComp.create_board_text("...")
            self.next()

        elif progress == 3:
            self.__finding_lily()

        elif progress == 4:
            self.__spawnlily()

        elif progress == 5:
            self.__to_dream()

        elif progress == 6:
            self.destroying()

    def __tutorial(self):
        player = gm.Manager.get_instance().player

        hud.HUDComp.create_board_text("Press AWDS to move |F to interact |Enter to next")
        voice = player.get_voice("voice1")
        hud.HUDComp.create_board_text("I feel hungry. Maybe i'll go get some food", voice)

    def __checking_fridge(self):
        sect = gm.Manager.get_instance().gamemap.sect
        player = gm.Manager.get_instance().player

        if type(sect) is not mphouse.Kitchen:
            return False

        area = sect.get_area("Fridge")

        keys = pg.key.get_pressed()

        if area.is_overlap(player.get_rect()) and keys[pg.K_f]:
            return True

        return False

    def __finding_lily(self):
        player = gm.Manager.get_instance().player

        gm.Manager.play_theme("../Assets/Sound/Other/rain.mp3")

        voice = pg.mixer.Sound("../Assets/Sound/LilyVoice/voice1.wav")
        hud.HUDComp.create_board_text("Viole...", voice)

        voice = player.get_voice("voice3")
        hud.HUDComp.create_board_text("What!? Is that voice come from my bedroom |Is that... |Lily", voice)

        self.next()

    def __spawnlily(self):
        sect = self.manager.gamemap.sect

        if type(sect) is not mphouse.Room:
            return

        size = sect.size
        start_pos = pg.math.Vector2(6.2 * size, 6.5 * size)

        lily = ll.Lily(start_pos, self.manager.entities)
        lily.is_harmless = True
        self.add_special_enemy("lily", lily, mphouse.Room)
        self.next()

    def __to_dream(self):
        sect = gm.Manager.get_instance().gamemap.sect
        player = gm.Manager.get_instance().player

        if type(sect) is not mphouse.Room:
            return

        if not self.is_occur_start_event:
            voice = player.get_voice("voice4")
            hud.HUDComp.create_board_text("Lily ?", voice)
            self.is_occur_start_event = True

        self.__lily_chasing()

    def __lily_chasing(self):
        player = gm.Manager.get_instance().player
        areas = gm.Manager.get_instance().gamemap.sect.areas

        lily = self.get_special_enemy("lily")
        lily_position = lily.get_position()

        player_rect = player.get_rect()
        width, height = 36, 80
        active_area = Area("active", lily_position, width, height, EPosition.TOPLEFT, areas)

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
        lily.set_movement(normv.NormalMovement(lily))
        lily.set_speed(4)

    def destroying(self):
        manager = gm.Manager.get_instance()
        player = manager.player

        lily = self.get_special_enemy("lily")
        player_rect = player.get_rect()

        if not gph.Physic.is_collide(player_rect, lily.get_rect()):
            return

        self.next()
        self.can_press_key = False
        ge.Effect.to_black_screen()

        manager.wait(5)

        self.remove_special_enemy("lily")
        manager.set_part(mandela.TheMandela(self.screen))
