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
        botlf = rect.bottomleft
        botrg = rect.bottomright

        walls = mapcontainer.map.Sect.walls

        for wall in walls:
            if (wall.rect.collidepoint(center)
                    or wall.rect.collidepoint(botlf)
                    or wall.rect.collidepoint(botrg)):

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
