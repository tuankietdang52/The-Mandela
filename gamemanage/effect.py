import pygame as pg


class Effect:
    @staticmethod
    def set_opacity(screen: pg.Surface, lssurf, alpha: int):
        """
        Set opacity for list of surface

        Must redraw map if opacity is lower than before
        """

        for surf in lssurf:
            surf[0].set_alpha(alpha)
            screen.blit(surf[0], surf[1])
            pg.display.update(surf[1])

    """
        Outline text
        Source code from pgzero
    """
    @classmethod
    def _circlepoints(cls, r):
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

    @classmethod
    def create_text_outline(cls,
                            font: pg.font.Font,
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

        for dx, dy in cls._circlepoints(outline_size):
            surf.blit(osurf, (dx + outline_size, dy + outline_size))

        surf.blit(textsurface, (outline_size, outline_size))
        return surf
