import pygame as pg
import src.entity.thealternate.enemy as em
import src.gamemanage.game as gm
import src.movingtype.ghostmoving as ghmv
from src.eventhandle.argument.eventargument import EventArgs

from src.utils import *
from src.pjenum import *


class FlawedImpersonators(em.Enemy):
    size = (52, 200)
    __sound_path = "../Assets/Sound/FlawedImpersonators/"

    def __init__(self, pos: pg.math.Vector2):
        super().__init__("../Assets/Enemy/FlawedImpersonators/",
                         "stand",
                         pos,
                         self.size)

        self.set_movement(ghmv.GhostMoving(self))
        self.speed = 2
        self.count = 0

        self.__is_rage = False

        self.__heart_beat_sound: pg.mixer.Channel | None = None

        self.__set_player_position()
        self.__set_spawn()

        self.__yelling_sound: pg.mixer.Channel | None = None

    def __set_spawn(self):
        player_pos = gm.Manager.get_instance().player.get_position()

        position = player_pos[0], player_pos[1] - 500

        self.set_position(position)

        SoundUtils.play_sound(f"{self.__sound_path}warning.mp3")
        gm.Manager.get_instance().wait(2)

        self.__heart_beat_sound = SoundUtils.play_sound(f"{self.__sound_path}heartbeat.mp3", True)

    def __set_player_position(self):
        sect = gm.Manager.get_instance().gamemap.sect
        player = gm.Manager.get_instance().player

        point = sect.get_point("Start")
        position = pg.math.Vector2(point.x, point.y)

        player.set_position(position)

    def __check_player_look(self):
        player = gm.Manager.get_instance().player
        direction = player.direction

        if direction != "up":
            self.count += 0.1
            self.__check_rage()
            return False

        self.count = 0
        return True

    def __check_rage(self):
        if self.count < 10 or self.__is_rage:
            return

        self.set_speed(5)

        self.__yelling_sound = SoundUtils.play_sound(f"{self.__sound_path}yelling.mp3")
        self.__is_rage = True

    def moving(self):
        if not self.__check_player_look() or self.__is_rage:
            self.__heart_beat_sound.unpause()
            self.movement.moving()
            return

        self.__heart_beat_sound.pause()
        player = gm.Manager.get_instance().player
        position = player.get_position().x, self.get_position().y
        self.set_position(position)

    def update(self, *args, **kwargs):
        super().update()
        self.moving()

    def kill_player(self):
        manager = gm.Manager.get_instance()

        self.__jumpscare()
        manager.wait(1)

        super().kill_player()

    def __jumpscare(self):
        screen = gm.Manager.get_instance().screen

        jumpscare = pg.image.load(f"{self.image_path}jumpscare.jpg").convert()
        size = screen.get_size()

        jumpscare = pg.transform.scale(jumpscare, size)
        screen.blit(jumpscare, (0, 0))
        pg.display.update()

    def on_destroy(self, args: EventArgs):
        super().on_destroy(args)
        self.__stop_sound()

    def __stop_sound(self):
        player = gm.Manager.get_instance().player
        if player.get_state() == EState.DEAD:
            return

        if self.__heart_beat_sound is not None:
            self.__heart_beat_sound.stop()

        if self.__yelling_sound is not None:
            self.__yelling_sound.stop()
