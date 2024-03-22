from enum import Enum


class EState(Enum):
    FREE = 0
    ISATTACK = 1
    BUSY = 2
    DEAD = 3
