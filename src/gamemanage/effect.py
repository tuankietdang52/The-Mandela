import pygame as pg
import src.gamemanage.game as gm


class Effect:
    @staticmethod
    def to_black_screen():
        manager = gm.Manager.get_instance()
        mp = manager.gamemap.sect
        player = manager.player

        mp.set_opacity(0)
        player.get_image().set_alpha(0)
        manager.set_appear_entity_opacity(0)

        manager.screen.fill((0, 0, 0))

        pg.display.update()

    @staticmethod
    def fade_in_screen(fade_in_entities: bool = True):
        """fade in entire screen"""
        manager = gm.Manager.get_instance()
        mp = manager.gamemap.sect
        player = manager.player

        max_alpha = 255

        for alpha in range(max_alpha):
            manager.screen.fill((0, 0, 0))

            mp.set_opacity(alpha)

            if fade_in_entities:
                manager.set_appear_entity_opacity(alpha)
                player.get_image().set_alpha(alpha)

            manager.update_UI_ip()

    @staticmethod
    def fade_out_screen(fade_out_entities: bool = True):
        """fade out entire screen"""
        manager = gm.Manager.get_instance()
        mp = manager.gamemap.sect
        player = manager.player

        max_alpha = 255

        for alpha in reversed(range(max_alpha)):
            manager.screen.fill((0, 0, 0))

            mp.set_opacity(alpha)

            if fade_out_entities:
                manager.set_appear_entity_opacity(alpha)
                player.get_image().set_alpha(alpha)

            manager.update_UI_ip()

    @staticmethod
    def fade_in_list(screen: pg.surface.Surface, ls: list[tuple[pg.surface.Surface, pg.rect.Rect]]):
        manager = gm.Manager.get_instance()
        max_alpha = 255
        alpha = 0
        delay = float(0)

        while alpha <= max_alpha:
            delay += 0.01
            if delay < 100:
                continue

            delay = 0
            manager.update_UI()

            for item in ls:
                item[0].set_alpha(alpha)
                screen.blit(item[0], item[1])

            pg.display.update()
            alpha += 1

    @staticmethod
    def fade_out_list(screen: pg.surface.Surface, ls: list[tuple[pg.surface.Surface, pg.rect.Rect]]):
        manager = gm.Manager.get_instance()
        alpha = 255
        delay = float(0)

        while alpha >= 0:
            delay += 0.01
            if delay < 100:
                continue

            delay = 0
            manager.update_UI()

            for item in ls:
                item[0].set_alpha(alpha)
                screen.blit(item[0], item[1])

            pg.display.update()
            alpha -= 1

    """
        Outline text
        Source code from pgzero
    """
    @staticmethod
    def __circlepoints(r):
        _circle_cache = {}
        r = int(round(r))
        if r in _circle_cache:
            return _circle_cache[r]
        x, y, e = r, 0, 1 - r
        _circle_cache[r] = points = []
        while x >= y:
            points.append((x, y))
            y += 1
            if e < 0:
                e += 2 * y - 1
            else:
                x -= 1
                e += 2 * (y - x) - 1
        points += [(y, x) for x, y in points if x > y]
        points += [(-x, y) for x, y in points if x]
        points += [(x, -y) for x, y in points if y]
        points.sort()
        return points

    @staticmethod
    def create_text_outline(font: pg.font.Font,
                            text: str,
                            color: tuple[int, int, int],
                            outline_size: int,
                            outline_color: tuple[int, int, int]) -> pg.surface.Surface:
        _circle_cache = {}

        textsurface = font.render(text, True, color).convert_alpha()
        w = textsurface.get_width() + 2 * outline_size
        h = font.get_height()

        osurf = pg.Surface((w, h + 6 * outline_size)).convert_alpha()
        osurf.fill((0, 0, 0, 0))

        surf = osurf.copy()

        osurf.blit(font.render(text, True, outline_color).convert_alpha(), (0, 0))

        for dx, dy in Effect.__circlepoints(outline_size):
            surf.blit(osurf, (dx + outline_size, dy + outline_size))

        surf.blit(textsurface, (outline_size, outline_size))
        return surf
