import mapcontainer.map
import pygame


class Physic:
    def __init__(self):
        pass

    @staticmethod
    def is_collide_wall(rect: pygame.Rect):
        """
        :param rect: Next rect
        """

        center = rect.center
        bottom_left = rect.bottomleft
        bottom_right = rect.bottomright
        left = rect.midleft
        right = rect.midright

        walls = mapcontainer.map.Sect.walls

        if (center in walls
                or bottom_left in walls
                or bottom_right in walls
                or left in walls
                or right in walls):
            return True

        return False

    @staticmethod
    def is_collide(rect1, rect2):
        center = rect1.center
        botlf = rect1.bottomleft
        botrg = rect1.bottomright

        if (rect2.collidepoint(center)
                or rect2.collidepoint(botlf)
                or rect2.collidepoint(botrg)):

            return True

        return False
