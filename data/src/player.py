import pickle, base64
from .config import *

class Player(pyge.pg.sprite.Sprite):
    type:str = 'player'
    saveable:list[str, ] = ['name', 'element', 'difficulty', 'level','experience', 'health', 'status', 'maxhealth', 'position']
    
    save:object
    
    movement:pg.math.Vector2 = pg.math.Vector2(0,0)
    name:str
    element:int
    difficulty:int
    
    level:int
    experience:float
    
    health:float = 100
    maxhealth:float = 100
    heal_delay_time:float = 0.0 # Seconds to be passed on TimeSys
    heal_delay_time_count:int = 0 # Frames that we will need to wait
    
    status:dict = {
        'atk':1,
        'def':1,
        'spd':1,
        'int':1,
        'lck':1,
        'points':0
    }
    
    damage:int = 5
    resistance:int = 3
    speed:int = 1
    
    frames:list[pg.SurfaceType,] = []
    frame_count:float = 0
    
    rect:pg.rect.RectType = pg.rect.Rect(0,0,32,32)
    def __init__(self, save, Savename:str, Saveelement:int) -> None:
        super().__init__()
        self.save = save
        self.name = Savename
        self.element = Saveelement
        rect:pg.rect.RectType = pg.rect.Rect(0,0,32,32)
        
    def update_attributtes(self):
        self.damage = 5 + self.status['atk'] * 0.5
        self.resistance = 3 + self.status['def'] * 0.5
        self.speed = 1 + self.status['spd'] * 0.15
        
        percentage_health = self.health/self.maxhealth
        self.maxhealth = 100 + self.resistance * 0.6
        self.health = self.maxhealth * percentage_health
        
    def input(self):
        UP_INPUT:bool = pge.hasKeyPressed(pg.K_w) or pge.hasKeyPressed(pg.K_UP)
        DOWN_INPUT:bool = pge.hasKeyPressed(pg.K_s) or pge.hasKeyPressed(pg.K_DOWN)
        LEFT_INPUT:bool = pge.hasKeyPressed(pg.K_a) or pge.hasKeyPressed(pg.K_LEFT)
        RIGHT_INPUT:bool = pge.hasKeyPressed(pg.K_d) or pge.hasKeyPressed(pg.K_RIGHT)
        
        if UP_INPUT:
            self.movement.y = self.speed
        elif DOWN_INPUT:
            self.movement.y = -self.speed
        else:
            self.movement.y *= 0.75
            if abs(self.movement.y) < 0.05: self.movement.y = 0
            
        if LEFT_INPUT:
            self.movement.x = self.speed
        elif RIGHT_INPUT:
            self.movement.x = -self.speed
        else:
            self.movement.x *= 0.75
            if abs(self.movement.x) < 0.05: self.movement.x = 0
    
    def frame(self) -> pg.SurfaceType:
        if len(self.frames) <= 0:
            surf = pg.Surface((32,32))
            surf.fill(pge.Colors.random().rgb)
            
            self.frames.append(surf)
            
        return self.frames[int(self.frame_count)]
    
    def loadData(self, data:dict):
        for key in data.keys():
            if key in Player.saveable:
                setattr(self, key, data[key])
        
    def update(self):
        self.update_attributtes()
        self.input()
        
        self.rect.center = pge.screen.get_rect().center
        
    def getCorrectData(self) -> dict:
        return {key:value for key,value in self.__dict__.items() if key in Player.saveable}