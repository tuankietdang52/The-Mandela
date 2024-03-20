import mapcontainer.map
import pygame


class Physic:
    def __init__(self):
        pass

    @staticmethod
    def is_collide_wall(rect):
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
