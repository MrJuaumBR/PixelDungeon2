from .config import *

class Player(pyge.pg.sprite.Sprite):
    element = 0
    name =''
    def __init__(self,name,elment):
        super().__init__()
        self.element = elment
        self.name = name