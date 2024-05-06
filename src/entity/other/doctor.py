import pygame as pg
import src.gamemanage.game as gm
import src.gameobj.gameobject as go
import src.mapcontainer.map as mp

from src.eventhandle.argument import *
from src.hud.hudcomp import *


class Doctor(go.GameObject):
    def __init__(self, position: pg.math.Vector2, appear_sect: type[mp.Sect]):
        super().__init__(position, "../Assets/Ally/Doctor/die.png", (100, 40), appear_sect)
        self.rect = self.image.get_rect(center=position)

        self.manager = gm.Manager.get_instance()

        self.set_area_size((100, 80))

    def player_interact(self, args: EventArgs):
        player = self.manager.player

        if not self.area.is_overlap(player.get_rect()):
            return

        HUDComp.create_board_text("A corpse?? Look like the doctor in the news earlier",
                                  player.get_voice("voice15"))
        HUDComp.create_board_text("Huh? There is a piece of paper near him",
                                  player.get_voice("voice16"))

        note = """Dear stranger, 
                |I think I cant avoid the death so I wrote this if someone pick up, 
                they can know the position of the anti-sleep potion I left 
                |The potion I hide in the garbage behind the apartment
                """

        HUDComp.show_note(note, 20)
        player.interact -= self.callback
