import pygame as pg
import src.entity.thealternate.enemy as em
import src.gamemanage.game as gm
import src.movingtype.ghostmoving as ghm


class FlawedImpersonators(em.Enemy):
    size = (52, 200)
    __sound_path = "../Assets/Sound/FlawedImpersonators/"

    def __init__(self,
                 pos: pg.math.Vector2,
                 groups: pg.sprite.Group):
        super().__init__("../Assets/Enemy/FlawedImpersonators/",
                         "stand",
                         pos,
                         self.size,
                         groups)

        self.set_movement(ghm.GhostMoving(self))
        self.speed = 2
        self.count = 0

        self.__is_rage = False

        self.__set_player_position()
        self.__set_spawn()

    def __set_spawn(self):
        player_pos = gm.Manager.get_instance().player.get_position()

        position = player_pos[0], player_pos[1] - 500

        self.set_position(position)

        pg.mixer.Sound(f"{self.__sound_path}warning.mp3").play()
        gm.Manager.get_instance().wait(2)

        self.__heart_beat_sound = pg.mixer.Sound(f"{self.__sound_path}heartbeat.mp3").play(-1)

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
        pg.mixer.Sound(f"{self.__sound_path}yelling.mp3").play()

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
