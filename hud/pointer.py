import pygame.image


class Pointer:
    size = (20, 30)

    def __init__(self, screen):
        self.image = pygame.image.load("Assets/HUD/pointer.png")

        self.image = pygame.transform.scale(self.image, self.size)
        self.screen = screen
        self.is_set = False

    def set_position(self, pos):
        self.play_select_sound()
        rect = self.image.get_rect(topleft=pos)

        self.is_set = True

        self.screen.blit(self.image, rect)
        pygame.display.update(rect)

    def play_select_sound(self):
        pygame.mixer.Sound("Assets/Sound/select.mp3").play()

    def play_choose_sound(self):
        pygame.mixer.Sound("Assets/Sound/choose.mp3").play()



