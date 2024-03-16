import pygame
from presenter import PlayerPresenter


class PlayerView(pygame.sprite.Sprite):
    __path = "Assets/Ally/MainChar/"
    __size = (24, 68)

    def __init__(self, screen, health):
        self.screen = screen
        self.presenter = PlayerPresenter(health, self)
        self.img = pygame.image.load(self.__path + "down1.png").convert_alpha()
        pygame.sprite.Sprite.__init__(self)

    def set_img(self, img):
        self.img = img

    def get_img(self):
        return self.img

    def set_scale(self, size):
        """
        :param tuple[float, float] size:
        :return:
        """
        self.__size = size

    def get_scale(self) -> tuple[float, float]:
        return self.__size

    def moving(self, keys):
        self.presenter.handle_moving(keys)

    def update_player(self):
        rect = self.presenter.get_position()
        self.draw(rect, self.__size)

    def draw(self, rect, size=None):
        if size is None:
            self.img = pygame.transform.scale(self.img, self.__size)

        else:
            self.img = pygame.transform.scale(self.img, size)

        self.screen.blit(self.img, rect)
        print(f"{self.presenter.get_position()}")

