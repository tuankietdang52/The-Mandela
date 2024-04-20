import abc

import pygame as pg
import src.gamemanage.physic as gph
import src.movingtype.movement as mv
import src.gamemanage.game as gm


class Enemy(abc.ABC, pg.sprite.Sprite):
    img_path = ""

    def __init__(self,
                 image: str,
                 pos: pg.math.Vector2,
                 size: tuple[int, int],
                 groups: pg.sprite.Group):
        super().__init__(groups)
        
        self.image = pg.image.load(image).convert_alpha()
        self.set_size(size)

        self.start_pos = pg.math.Vector2(pos)
        self.position = pg.math.Vector2(pos)
        self.rect = self.image.get_rect(topleft=self.position)

        self.direction = pg.math.Vector2()

        self.speed = 1
        self.movement = None

        gm.Manager.get_instance().on_destroy += self.on_destroy

    def set_position(self, pos: tuple[float, float] | pg.math.Vector2):
        if type(pos) is pg.math.Vector2:
            self.position = pos
        else:
            self.position = pg.math.Vector2(pos)

        self.rect = self.image.get_rect(topleft=self.position)

    def get_position(self) -> pg.math.Vector2:
        return self.position

    def set_image(self, image: pg.surface.Surface | str, size: tuple[int, int] = None):
        """
        :param image: string: name of image
        :param size:
        """
        size = self.get_size() if size is None else size

        if type(image) is str:
            image = pg.image.load(f"{self.img_path + image}.png").convert_alpha()

        self.image = image
        self.set_size(size)

    def get_image(self) -> pg.surface.Surface:
        return self.image

    def set_size(self, size: tuple[int, int]):
        self.image = pg.transform.scale(self.image, size)

    def get_size(self) -> tuple[int, int]:
        return self.image.get_size()

    def get_rect(self) -> pg.rect.Rect:
        return self.image.get_rect(topleft=self.get_position())

    def set_speed(self, speed: float):
        self.speed = speed

    def get_speed(self) -> float:
        return self.speed

    def set_movement(self, movement: mv.Movement):
        self.movement = movement

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        pass

    def set_direction_to_player(self):
        """for UI"""
        position = self.get_position()
        player_pos = gm.Manager.get_instance().player.get_position()

        if position.x > player_pos.x:
            self.__flip_horizontal()

    def __flip_horizontal(self):
        self.image = pg.transform.flip(self.image, True, False)

    def calculate_direction(self, dest: pg.math.Vector2) -> pg.math.Vector2:
        position = self.get_position()

        distance = (dest - position).magnitude()

        if distance > 0:
            self.direction = (dest - position).normalize()

        else:
            self.direction = pg.math.Vector2()

        self.direction = pg.math.Vector2(round(self.direction.x), round(self.direction.y))

        return self.direction

    def moving(self):
        if self.movement is not None:
            self.movement.moving()

    def can_move(self, pos: pg.math.Vector2):
        rect = self.image.get_rect(topleft=pos)

        if gph.Physic.is_collide_wall(rect):
            return False

        return True

    def is_hit_player(self) -> bool:
        player = gm.Manager.get_instance().player

        rect = self.rect
        player_rect = player.get_rect()

        if gph.Physic.is_collide(player_rect, rect):
            return True

        return False

    def on_destroy(self):
        manager = gm.Manager.get_instance()
        manager.appear_enemy.remove(self)
        manager.entities.remove(self)
