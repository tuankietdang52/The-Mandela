import pygame as pg
import src.gamemanage.game as gm
import src.entity.thealternate.enemy as em
import src.movingtype.normalmoving as normv

from src.eventhandle.argument import EventArgs


class Instruder(em.Enemy):
    def __init__(self, pos: pg.math.Vector2):
        super().__init__("../Assets/Enemy/Instruder/",
                         "instruder",
                         pos,
                         (36, 80))

        self.movement = normv.NormalMovement(self)
        self.speed = 7

        player = gm.Manager.get_instance().player
        player.set_speed(0.1)

    def update(self, *args, **kwargs):
        super().update()
        self.moving()

    def moving(self):
        self.movement.moving()
        self.set_direction_to_player()

    def kill_player(self):
        manager = gm.Manager.get_instance()

        self.__jumpscare()
        manager.wait(2)

        super().kill_player()

    def __jumpscare(self):
        screen = gm.Manager.get_instance().screen

        jumpscare = pg.image.load(f"{self.image_path}jumpscare.png").convert()
        size = screen.get_size()

        jumpscare = pg.transform.scale(jumpscare, size)
        screen.blit(jumpscare, (0, 0))
        pg.display.update()
