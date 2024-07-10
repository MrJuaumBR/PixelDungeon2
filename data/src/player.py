from .config import *

class Player(pyge.pg.sprite.Sprite):
    saveable = ['element','name','pos']
    element = 0
    name =''
    rect:pyge.pg.Rect
    pos:tuple = (0,0)
    def __init__(self,save,name:str,elment:int):
        super().__init__()
        self.element = elment
        self.name = name
        self.save = save
        self.rect = pyge.pg.Rect(4096,3072,32,32)
        self.pos = self.rect.topleft
        
    def getCorrectData(self) -> dict:
        s:dict = {}
        for var in self.__dict__.keys():
            if var in self.saveable:
                s[var] = self.__dict__[var]
        return s
        
    def loadData(self,data:dict):
        for key in data.keys():
            self.__dict__[key] = data[key]