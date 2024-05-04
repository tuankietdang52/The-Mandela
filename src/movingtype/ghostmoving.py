import pygame as pg
import src.movingtype.movement as mv
import src.entity.thealternate.enemy as enenemy
import src.gamemanage.game as gm


class GhostMoving(mv.Movement):
    def __init__(self, enemy: enenemy.Enemy):
        self.owner = enemy
        self.manager = gm.Manager.get_instance()
        self.player = self.manager.player

    def moving(self):
        player_position = self.player.get_position()

        direction = self.owner.calculate_direction(player_position)
        velocity = direction * self.owner.get_speed()

        self.__chase(velocity)

    def __chase(self, velocity: pg.math.Vector2):
        position = self.owner.get_position() + velocity
        self.owner.set_position(position)
