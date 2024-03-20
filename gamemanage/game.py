import sys
import pygame

from view import PlayerView
from mapcontainer import *


class Game:
    music_path = "Assets/Music/"

    FPS = 120
    WIDTH = 800
    HEIGHT = 800

    clock = pygame.time.Clock()

    pygame.init()

    # screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    # Music Background init #
    pygame.mixer.init()
    pygame.mixer.music.load(f"{music_path}Lily.mp3")
    # pygame.mixer.music.play(1)

    # Object init #
    gamemap = HouseNormal(screen)

    player = PlayerView.init(screen, gamemap, 1000)

    def __init__(self):
        pass

    def change_map(self, gamemap):
        """:param Map gamemap: """
        self.gamemap = gamemap

    def setup(self):
        gamemap = self.gamemap
        player = self.player

        gamemap.sect.create_sect()

        try:
            start_point = gamemap.sect.get_spawn_point()
        except AttributeError:
            start_point = gamemap.sect.get_start_point()

        player.set_position(start_point)

        player.update_player()

    def running_game(self):
        gameover = False
        clock = self.clock

        self.setup()

        while not gameover:
            self.__event_action()
            self.__pressing_key()

            self.handle_change_sect()

            pygame.display.update()

            clock.tick(self.FPS)

    def __event_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def __pressing_key(self):
        keys = pygame.key.get_pressed()

        self.player.moving(keys)

    def repos_player(self):
        start_pos = self.gamemap.sect.get_start_point()

        self.player.set_position(start_pos)
        self.player.update_player()

    def handle_change_sect(self):
        mapname = self.gamemap.sect.in_area(self.player.get_rect())

        current = self.gamemap.sect

        self.gamemap.change_sect(mapname)

        if self.gamemap.sect == current:
            return

        self.restart_screen()

        self.gamemap.sect.create_sect()
        self.repos_player()

    def restart_screen(self):
        black_screen = pygame.Surface((self.WIDTH, self.HEIGHT))
        black_screen.fill((0, 0, 0))
        black_screen.set_alpha(250)

        self.screen.blit(black_screen, (0, 0))
