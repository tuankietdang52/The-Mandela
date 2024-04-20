import pygame as pg
import src.entity.thealternate.enemy as enenemy
import src.movingtype.normalmoving as normv
import src.gamemanage.game as gm


class Doppelganger(enenemy.Enemy):
    size = (36, 80)
    __frame = 0

    def __init__(self,
                 pos: pg.math.Vector2,
                 groups: pg.sprite.Group):
        self.img_path = "../Assets/Ally/Viole/"
        super().__init__(f"{self.img_path}walk1.png", pos, self.size, groups)
        self.set_movement(normv.NormalMovement(self))

    def update(self, *args, **kwargs):
        self.moving()

    def __set_animation_moving(self, index: int):
        player_pos = gm.Manager.get_instance().player.get_position()
        direction = self.direction

        if direction.y != 0:
            if direction.y > player_pos.y:
                path = "up"

            else:
                path = "down"
        else:
            path = "walk"

        animate = f"{path + str(index)}"
        self.set_image(animate)

        if direction.y == 0:
            self.set_direction_to_player()

    def __play_animation_moving(self):
        if self.__frame < 20:
            index = 1

        else:
            index = 0

        self.__frame += 1
        if self.__frame > 40:
            self.__frame = 0

        self.__set_animation_moving(index)

    def moving(self):
        super().moving()
        self.__play_animation_moving()
