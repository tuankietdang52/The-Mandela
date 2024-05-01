import pygame as pg


class SoundUtils:
    @staticmethod
    def play_sound(path: str, is_loop: bool = False) -> pg.mixer.Channel:
        sound = pg.mixer.Sound(path)
        if is_loop:
            return sound.play(-1)
        else:
            return sound.play(0)

    @staticmethod
    def clear_all_sound():
        pg.mixer.stop()
