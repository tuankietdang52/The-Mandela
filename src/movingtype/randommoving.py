import random
import pygame as pg
import src.gamemanage.game as gm
import src.movingtype.movement as mv
import src.entity.thealternate.enemy as em


class RandomMovement(mv.Movement):
    def __init__(self, enemy: em.Enemy, moving_range: int):
        self.owner = enemy
        self.manager = gm.Manager.get_instance()
        self.moving_range = moving_range
        self.dest = self.owner.get_position()

        self.chance_to_stand = 100

    def __get_random_dest(self) -> pg.math.Vector2:
        position = self.owner.get_position()

        cannot_move = set()

        left = position.x - self.moving_range
        right = position.x + self.moving_range
        top = position.y - self.moving_range
        bottom = position.y + self.moving_range

        while True:
            x = random.randint(round(left), round(right))
            y = random.randint(round(top), round(bottom))

            dest = pg.math.Vector2(x, y)

            if (dest.x, dest.y) in cannot_move:
                continue

            if self.owner.can_move(dest):
                break
            else:
                cannot_move.add((dest.x, dest.y))

        return dest

    def moving(self):
        position = self.owner.get_position()

        if self.dest == position:
            # standing
            is_standing = random.randint(0, self.chance_to_stand + 1) < self.chance_to_stand
            if is_standing:
                return

            self.dest = self.__get_random_dest()

        direction = self.owner.calculate_direction(self.dest)
        velocity = direction * self.owner.get_speed()

        next_position = self.owner.get_position() + velocity

        if not self.owner.can_move(next_position):
            self.dest = self.__get_random_dest()
            return

        self.owner.set_position(next_position)
