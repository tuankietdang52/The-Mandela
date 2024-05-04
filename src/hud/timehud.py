import pygame as pg
import src.gamemanage.game as gm


class TimeHUD(pg.sprite.Sprite):
    FONTPATH = "../Assets/Font/Crang.ttf"

    def __init__(self, groups: pg.sprite.Group):
        super().__init__(groups)
        self.manager = gm.Manager.get_instance()

        width, height = self.manager.screen.get_size()

        self.image = pg.surface.Surface((0.15 * width, 0.2 * height), pg.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect(topright=(width, 20))

    def update(self, *args, **kwargs):
        self.image.fill((0, 0, 0, 0))
        time = self.manager.game_time
        day = self.manager.game_night

        hour, minute = str(time[0]), str(time[1])
        hour_format = f"0{time[0]}" if len(hour) == 1 else hour
        minute_format = f"0{time[1]}" if len(minute) == 1 else minute

        night_str = f"Night {str(day)}"

        time_str = f"{hour_format}:{minute_format}"

        font = pg.font.Font(self.FONTPATH, 20)
        time_surf = font.render(time_str, 1, (255, 255, 255))
        time_rect = time_surf.get_rect(topleft=(0, 0))

        night_surf = font.render(night_str, 1, (255, 255, 255))
        night_rect = night_surf.get_rect(topleft=(0, 50))

        self.image.blit(time_surf, time_rect)
        self.image.blit(night_surf, night_rect)

    def set_visible(self, is_visible: bool):
        if not is_visible:
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(254)
