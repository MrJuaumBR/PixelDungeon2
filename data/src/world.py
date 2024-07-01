from .config import *

from .player import Player
class World(pyge.pg.sprite.Group):
    diffculty = 0
    player:Player
    def __init__(self, player:Player, diffculty = 0):
        super().__init__()
        self.player = player
        self.diffculty = diffculty