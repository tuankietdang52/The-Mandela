from src.hud.menu.contract import *


class MenuModel(MenuContract.IModel):
    def __init__(self, max_choice: int):
        self.choice = 1
        self.max_choice = max_choice

    def increase_choice(self):
        self.choice += 1 if self.choice != self.max_choice else 0

    def decrease_choice(self):
        self.choice -= 1 if self.choice != 1 else 0

    def get_choice(self):
        return self.choice
