import sys
import pygame as pg
import src.gamepart.part as gp
import src.gamemanage.game as gm
import src.gamemanage.effect as ge
import src.mapcontainer.housenormal as mphouse
import src.mapcontainer.town as mptown


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

    def manage_progess(self):
        progess = self.get_progess_index()

        if progess == 0:
            self.__waking_up()
            self.next()

        elif progess == 1:
            self.__get_up()
            self.next()

        elif progess == 2:
            self.__check_tv()

        elif progess == 3:
            self.__going_outside()

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
        path = "../Assets/Sound/VioleVoice/"
        gm.Manager.set_map(mphouse.HouseNormal(self.screen))
        gm.Manager.gamemap.sect.create()
        gm.Manager.gamemap.sect.set_opacity(0)

        ge.Effect.fade_in_screen()
        gm.Manager.wait(2)

        pg.mixer.Sound("../Assets/Sound/Other/tvlost.mp3").play(-1)

        voice1 = pg.mixer.Sound(f"{path}voice5.wav")
        voice2 = pg.mixer.Sound(f"{path}voice6.wav")
        self.create_board_text("What was that ? |Am I just too tired ?", voice1)
        self.create_board_text("Hmm? What wrong with the TV ?", voice2)

    def __check_tv(self):
        sect = gm.Manager.gamemap.sect

        if type(sect) is not mphouse.Room:
            if self.is_occur_start_event:
                pg.mixer.stop()

            self.is_occur_start_event = False
            return

        if not self.is_occur_start_event:
            sound = pg.mixer.Sound("../Assets/Sound/Other/tvlost.mp3")
            sound.play(-1)
            self.is_occur_start_event = True

        area = sect.get_area("TV")
        keys = pg.key.get_pressed()

        if not area.is_overlap(self.player.get_rect()) or not keys[pg.K_f]:
            return

        pg.mixer.stop()
        self.__watching_tv()

    def __watching_tv(self):
        gm.Manager.play_theme("../Assets/Music/vhs1.mp3", 0.1)
        gm.Manager.wait(3)

        voice1 = pg.mixer.Sound("../Assets/Sound/NarratorVoice/voice1.mp3")

        text = ("""We're currently receiving countless report of an unidentified hostile, called the alternate 
|until we have complete understanding of the threat its important to stay home, lock all doors and windows, 
always carry a firearm with you 
|If you encounter an alternate, follow the T.H.I.N.K principle""")
        self.create_board_text(text, voice1)
        self.__the_think_principle()

    def __the_think_principle(self):
        path = "../Assets/Sound/NarratorVoice/"

        tell = "TELL |the authority figure about your encounter"
        t_voice = pg.mixer.Sound(f"{path}tell.mp3")

        hinder = "HINDER |the alternate's movement"
        h_voice = pg.mixer.Sound(f"{path}hinder.mp3")

        identify = "IDENTIFY |the class type"
        i_voice = pg.mixer.Sound(f"{path}identify.mp3")

        neutralize = "NEUTRALIZE |the alternate, if safe to do so"
        n_voice = pg.mixer.Sound(f"{path}neutralize.mp3")

        know = "kill yourself"
        k_voice = pg.mixer.Sound(f"{path}kys.mp3")

        self.create_board_text(tell, t_voice)
        self.create_board_text(hinder, h_voice)
        self.create_board_text(identify, i_voice)
        self.create_board_text(neutralize, n_voice)

        pg.mixer.music.stop()
        self.create_board_text(know, k_voice)

        sound = pg.mixer.Sound("../Assets/Sound/Other/tvlost.mp3")
        sound.play()
        gm.Manager.wait(2)
        sound.stop()

        know = "KNOW |your place and your enemy"
        k_voice = pg.mixer.Sound(f"{path}know.mp3")
        self.create_board_text(know, k_voice)

        self.next()

    def __going_outside(self):
        path = "../Assets/Sound/VioleVoice/"
        self.create_board_text("What... is going on ?",
                               pg.mixer.Sound(f"{path}voice7.wav"))
        self.create_board_text("If the news is right, I need to go outside and get more food ASAP",
                               pg.mixer.Sound(f"{path}voice8.wav"))

        self.can_change_map = True
        self.next()

