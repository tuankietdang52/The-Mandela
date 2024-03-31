import pygame.image


class Pointer:
    """Position by topleft"""
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


class Board:
    """Position by center"""
    def __init__(self, screen: pygame.Surface, pos: tuple[float, float], size: tuple[float, float]):
        self.screen = screen

        self.surf = pygame.Surface(size)

        self.surf.fill((0, 0, 0))
        self.surf.set_alpha(100)

        self.rect = self.surf.get_rect(center=pos)

    def draw(self):
        self.screen.blit(self.surf, self.rect)

        points = [
            self.rect.topleft,
            self.rect.topright,
            self.rect.bottomright,
            self.rect.bottomleft
        ]

        pygame.draw.lines(self.screen, (0, 0, 0), True, points, 7)

    def insert_content(self, content: pygame.Surface, rect):
        inside_rect = rect.clamp(self.rect)
        rect = inside_rect.move(inside_rect.x, 20)

        self.screen.blit(content, rect)


class StoryText:
    """Position by topleft"""
    fontpath = "Assets/Font/Crang.ttf"

    def __init__(self, screen: pygame.Surface, text: str, size: int, board: Board):
        """Write text to board"""
        self.screen = screen

        self.text = text
        self.size = size

        self.board = board

        self.write()

    def write(self):
        font = pygame.font.Font(self.fontpath, self.size)

        start = self.board.rect.topleft
        width = self.board.rect.width

        pos = start

        end = (start[0] + width) / 2.2

        space = self.size / 3

        for word in self.text:
            if pos[0] >= end:
                pos = start[0], pos[1] + space * 2

            surf = font.render(word, 1, (255, 255, 255))
            rect = surf.get_rect(topleft=pos)

            self.board.insert_content(surf, rect)

            if word != "i" and word != "I":
                pos = pos[0] + space, pos[1]
            else:
                pos = pos[0] + space / 2, pos[1]


class BoardText:
    def __init__(self,
                 screen: pygame.Surface,
                 text: str,
                 fontsize: int,
                 pos: tuple[float, float],
                 size: tuple[float, float]):
        """
        :param pos: position of board
        :param size: size of board
        """
        self.board = Board(screen, pos, size)
        self.board.draw()
        self.txt = StoryText(screen, text, fontsize, self.board)

        self.rect = self.board.rect
