import sys

import pygame
from Presenter.Player.PlayerPresenter import  PlayerPresenter
FPS = 60
Width = 700
Height = 700
clock = pygame.time.Clock()


def running_game():
    pygame.init()

    gameover = False
    pygame.display.set_mode((Width, Height))

    while not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
                sys.exit()

        clock.tick(FPS)


if __name__ == "__main__":
    a = PlayerPresenter.init(1000)

    print(a.get_health())

    a.decrease_health(200)

    print(a.get_health())
