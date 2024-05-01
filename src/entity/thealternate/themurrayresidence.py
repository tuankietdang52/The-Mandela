import pygame as pg
import src.gamemanage.game as gm
import src.entity.thealternate.enemy as em
import src.movingtype.ghostmoving as ghmv

from src.pjenum import *
from src.eventhandle.argument.eventargument import *
from src.utils import *


class TheMurrayResidence(em.Enemy):
    size = (90, 138)
    __frame = 0

    def __init__(self, pos: pg.math.Vector2, groups: pg.sprite.Group):
        super().__init__("../Assets/Enemy/TheMurrayResidence/",
                         "stand",
                         pos,
                         self.size,
                         groups)
        self.movement = ghmv.GhostMoving(self)

        self.set_speed(5)
        self.__is_chasing = False
        self.__sound: pg.mixer.Channel | None = None

    def __chase_animation(self):
        if self.__frame < 10:
            index = 1
            self.set_size((186, 135))

        else:
            index = 0

        self.__frame += 1
        if self.__frame > 20:
            self.__frame = 0

        path = f"run{index}"
        self.set_image(path)
        self.set_direction_to_player()

    def __spin_head(self):
        murray_sound_path = "../Assets/Sound/TheMurrayResidence/"
        if self.__frame == 0:
            self.set_direction_to_player()
            self.__sound = SoundUtils.play_sound(f"{murray_sound_path}kidvoice.mp3")

        self.__frame += 1

        if 20 <= self.__frame < 150:
            self.set_image("spinhead1")
            self.set_direction_to_player()

        elif 150 <= self.__frame < 330:
            self.set_image("spinhead2")
            self.set_direction_to_player()

        elif self.__frame >= 350:
            self.__frame = 0
            self.__is_chasing = True
            self.__sound = SoundUtils.play_sound(f"{murray_sound_path}shout.mp3", True)

        gm.Manager.get_instance().update_UI_ip()

    def __give_player_debuff(self):
        player = gm.Manager.get_instance().player

        if player.get_state() == EState.DEAD:
            return

        player.set_speed(0.5)
        player.set_state(EState.PANIC)

    def update(self):
        super().update()
        self.__give_player_debuff()

        if not self.__is_chasing:
            self.__spin_head()
        else:
            self.moving()

    def moving(self):
        self.movement.moving()
        self.__chase_animation()

    def on_destroy(self, args: EventArgs):
        super().on_destroy(args)
        player = gm.Manager.get_instance().player

        if player.get_state() == EState.DEAD:
            return

        gm.Manager.get_instance().player.set_speed(1.5)
        player.set_state(EState.FREE)

        if self.__sound is not None and player.get_state() != EState.DEAD:
            self.__sound.stop()
