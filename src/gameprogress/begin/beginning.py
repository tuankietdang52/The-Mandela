import sys

import src.gameprogress.progressmanager as gp
import src.mapcontainer.housenormal as mphouse
import src.movingtype.normalmoving as normv
import src.gameprogress.begin.themandela as mandela
import src.hud.hudcomp as hud
import src.entity.thealternate.lily as ll
import src.entity.thealternate.doppelganger as dp

from src.tilemap import Area
from src.pjenum import *
from src.utils import *


class BeginStory(gp.ProgressManager):
    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen)

        self.can_press_key = True
        self.setup()

    def setup(self):
        super().setup()
        gm.Manager.play_theme("../Assets/Music/Lily.mp3")

    def event_action(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

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

        if not area.is_overlap(player.get_rect()) or not keys[pg.K_f]:
            return False

        gm.Manager.play_theme("../Assets/Sound/Other/rain.mp3")
        news_sound_path = "../Assets/Sound/NarratorVoice/news.mp3"
        SoundUtils.play_sound(news_sound_path, True)

        return True

    def __finding_lily(self):
        gm.Manager.get_instance().wait(1)
        player = gm.Manager.get_instance().player

        voice = player.get_voice("voice3")
        hud.HUDComp.create_board_text("What!? |I remember tv is turned off ?", voice)

        self.next()

    def __spawnlily(self):
        sect = self.manager.gamemap.sect

        if type(sect) is not mphouse.Room:
            return

        size = sect.size
        start_pos = pg.math.Vector2(6.2 * size, 6.5 * size)

        lily = ll.Lily(start_pos)
        lily.is_harmless = True
        self.spawn_manager.add_special_enemy("lily", lily, mphouse.Room)
        self.next()

    def __to_dream(self):
        sect = gm.Manager.get_instance().gamemap.sect
        player = gm.Manager.get_instance().player

        if type(sect) is not mphouse.Room:
            return

        if not self.is_occur_start_event:
            voice = player.get_voice("voice4")
            hud.HUDComp.create_board_text("Who are you ? |How did you get in my house ?", voice)
            self.is_occur_start_event = True

        self.__lily_chasing()

    def __lily_chasing(self):
        player = gm.Manager.get_instance().player
        areas = gm.Manager.get_instance().gamemap.sect.areas

        lily = self.spawn_manager.get_special_enemy("lily")
        lily_position = lily.get_position()

        player_rect = player.get_rect()
        width, height = 36, 80
        active_area = Area("active", lily_position, width, height, EPosition.TOPLEFT, areas)

        if not active_area.is_overlap(player_rect):
            return

        SoundUtils.play_sound("../Assets/Sound/Other/suprise.mp3")

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
        lily.set_speed(4)
        lily.set_movement(normv.NormalMovement(lily))

    def destroying(self):
        manager = gm.Manager.get_instance()
        player = manager.player

        lily = self.spawn_manager.get_special_enemy("lily")
        player_rect = player.get_rect()

        if not Physic.is_collide(player_rect, lily.get_rect()):
            return

        self.next()
        self.can_press_key = False
        Effect.to_black_screen()

        manager.wait(3)
        SoundUtils.clear_all_sound()
        manager.wait(2)

        self.spawn_manager.remove_special_enemy("lily")
        manager.set_game_progress(mandela.TheMandela(self.screen))
