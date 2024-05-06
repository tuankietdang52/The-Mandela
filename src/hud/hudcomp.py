import sys
import pygame as pg
import src.gamemanage.game as gm

from src.utils import *


class Pointer(pg.sprite.Sprite):
    """Position by topleft"""
    size = (20, 30)

    def __init__(self, screen: pg.surface.Surface):
        super().__init__(gm.Manager.get_instance().hud_groups)

        self.image = pg.image.load("../Assets/HUD/pointer.png").convert_alpha()

        self.image = pg.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()

        self.screen = screen
        self.is_set = False

    def set_visible(self, is_visible: bool):
        if not is_visible:
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(254)

    def set_position(self, pos: tuple[float, float]):
        self.play_select_sound()
        self.rect = self.image.get_rect(topleft=pos)

        self.is_set = True

    def get_position(self) -> tuple[float, float]:
        return self.rect.topleft

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def flip_horizontal(self):
        self.image = pg.transform.flip(self.image, True, False)

    def play_select_sound(self):
        SoundUtils.play_sound("../Assets/Sound/Other/select.mp3")

    def play_choose_sound(self):
        SoundUtils.play_sound("../Assets/Sound/Other/choose.mp3")

    def destroy(self):
        self.kill()


class Board:
    """Position by center"""

    def __init__(self, screen: pg.surface.Surface, pos: tuple[float, float], size: tuple[float, float]):
        self.screen = screen

        self.surf = pg.Surface(size)

        self.surf.fill((0, 0, 0))
        self.surf.set_alpha(100)

        self.rect = self.surf.get_rect(center=pos)

        self.content: list[tuple[pg.surface.Surface, pg.rect.Rect]] = list()

    def draw(self):
        self.screen.blit(self.surf, self.rect)

        points = [
            self.rect.topleft,
            self.rect.topright,
            self.rect.bottomright,
            self.rect.bottomleft
        ]

        pg.draw.lines(self.screen, (255, 0, 0), True, points, 7)

        self.__draw_content()

    def __draw_content(self):
        for item in self.content:
            # keep a rect inside another
            inside_rect = item[1].clamp(self.rect)
            rect = inside_rect.move(10, 20)

            # pg.draw.circle(self.screen, (255, 0, 0), rect.topleft, 5)
            # pg.display.update()
            self.screen.blit(item[0], rect)

    def insert_content(self, content: pg.surface.Surface, rect: pg.rect.Rect):
        self.content.append((content, rect))


class StoryText:
    """Position by topleft"""
    FONTPATH = "../Assets/Font/Crang.ttf"

    def __init__(self, screen: pg.surface.Surface, text: str, size: int, board: Board):
        """
        Write text to board
        New line: ' |sometext'
        """
        self.screen = screen

        self.text = text
        self.size = size

        self.space_distance = self.size / 4

        self.board = board

        self.write()

    def write(self):
        words = self.text.split()

        font = pg.font.Font(self.FONTPATH, self.size)

        start = self.board.rect.topleft

        pos = start
        end = self.board.rect.topright[0] - 10

        for word in words:
            pos = self.__get_position_word(word, pos, start[0], end)

            for char in word:
                if char == '|':
                    continue

                surf = font.render(char, 1, (255, 255, 255))
                rect = surf.get_rect(topleft=pos)

                self.board.insert_content(surf, rect)
                pos = self.__spacing_character(rect, self.space_distance)

    def __get_position_word(self,
                            word: str,
                            cur: tuple[float, float],
                            start_x: float,
                            end_x: float) -> tuple[float, float]:
        if cur[0] != start_x:
            cur = cur[0] + self.space_distance * 2, cur[1]

        pos = cur
        i = 0
        font = pg.font.Font(self.FONTPATH, self.size)

        while i < len(word):
            surf = font.render(word[i], 1, (255, 255, 255))
            end_rect = surf.get_rect(topleft=cur)

            if word[i] == '|':
                cur = start_x, cur[1] + self.space_distance * 6
                return cur

            elif end_rect.topright[0] >= end_x:
                cur = start_x, cur[1] + self.space_distance * 6
                return cur

            cur = self.__spacing_character(end_rect, self.space_distance)

            i += 1

        return pos

    def __spacing_character(self, rect: pg.rect.Rect, space: float) -> tuple[float, float]:
        pos = rect.topright
        pos = pos[0] + space / 2, pos[1]

        return pos


class BoardText:
    def __init__(self,
                 screen: pg.surface.Surface,
                 text: str,
                 fontsize: int,
                 pos: tuple[float, float],
                 size: tuple[float, float]):
        """
        :param pos: position of board
        :param size: size of board
        """
        self.board = Board(screen, pos, size)
        self.txt = StoryText(screen, text, fontsize, self.board)

        self.rect = self.board.rect

    def draw(self):
        self.board.draw()


class AcceptBoard:
    def __init__(self,
                 screen: pg.surface.Surface,
                 pos: tuple[float, float],
                 size: tuple[float, float]):
        self.board_txt = BoardText(screen, "yes | |no", 25, pos, size)
        self.board = self.board_txt.board

        self.pointer = Pointer(screen)
        self.pointer.flip_horizontal()

        self.screen = screen
        self.rect = self.board.rect

        self.yes_choice = True

    def __setup_pointer(self):
        pos = self.board.rect.topleft
        pointer_pos = pos[0] + 100, pos[1] + 20

        self.pointer.set_position(pointer_pos)
        self.pointer.draw()

    def draw(self):
        self.board.draw()
        self.__setup_pointer()

    def __move_cur(self, y):
        pointer_pos = self.pointer.rect.x, self.pointer.rect.y
        self.pointer.set_position((pointer_pos[0], pointer_pos[1] + y))

        gm.Manager.get_instance().update_UI()
        self.board.draw()
        self.pointer.draw()
        pg.display.flip()

    def changing_choice(self):
        keys = pg.key.get_pressed()

        new_y = self.board_txt.txt.space_distance * 12

        if keys[pg.K_w]:
            if self.yes_choice:
                return

            self.yes_choice = True
            self.__move_cur(-new_y)

        elif keys[pg.K_s]:
            if not self.yes_choice:
                return

            self.yes_choice = False
            self.__move_cur(new_y)


class HUDComp:
    @staticmethod
    def create_board_text(text: str, sound: pg.mixer.Sound = None):
        """
        Create a board contain text inside
        If you want to go to new line in the text, using ' |sometext' to do it
        """

        manager = gm.Manager.get_instance()
        screen = manager.screen

        if sound is not None:
            sound.play()

        pos = screen.get_width() / 2, screen.get_height() - 100

        size = screen.get_width(), screen.get_height() - 500

        board = BoardText(screen, text, 20, pos, size)
        board.draw()

        pg.display.update(board.rect)

        while True:
            gm.Game.ticking_time()
            if HUDComp.is_closing_board():
                break

        if sound is not None:
            sound.stop()

        screen.fill((0, 0, 0))
        manager.update_UI_ip()

    @staticmethod
    def create_accept_board() -> AcceptBoard:
        manager = gm.Manager.get_instance()
        screen = manager.screen

        pos = screen.get_width() / 2, screen.get_height() - 100

        size = screen.get_width(), screen.get_height() - 500

        board = AcceptBoard(screen, pos, size)
        board.draw()

        pg.display.update(board.rect)

        while True:
            board.changing_choice()
            gm.Game.ticking_time()
            if HUDComp.is_closing_board():
                board.pointer.play_choose_sound()
                break

        board.pointer.destroy()
        screen.fill((0, 0, 0))
        manager.update_UI_ip()
        return board

    @staticmethod
    def show_note(note: str, fontsize: int):
        manager = gm.Manager.get_instance()
        screen = manager.screen

        width, height = screen.get_size()
        board = BoardText(screen, note, fontsize, (width / 2, height / 2), (width * 0.7, height - 20))

        board.draw()
        pg.display.update()

        while True:
            gm.Game.ticking_time()
            if HUDComp.is_closing_board():
                break

        manager.update_UI_ip()

    @staticmethod
    def is_closing_board() -> bool:
        for event in pg.event.get():
            """Prevent game to freezing itself"""
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return True

        return False
