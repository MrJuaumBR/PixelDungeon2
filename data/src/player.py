from .config import *

class Player(pyge.pg.sprite.Sprite):
    saveable = ['element','name','pos','level','xp','points', 'strength', 'intelligence', 'dexterity', 'defence', 'max_health', 'health', 'max_mana', 'mana']
    element = 0
    name =''
    rect:pyge.pg.Rect
    type = 'player'
    pos:tuple = (0,0)
    image:pyge.pg.SurfaceType
    
    is_spawned:bool = False
    world:object = None
    direction:pyge.pg.math.Vector2 = pyge.pg.math.Vector2(0,0)
    # Attributes
    level:int = 1
    xp:float = 0.0
    points:int = 3
    speed:float = 3.0
    
    # Stats
    strength:int = 1
    intelligence:int = 1
    dexterity:int = 1
    defence:int = 1
    max_health:int = 100
    health:int = 100
    max_mana:int = 100
    mana:int = 100
    
    FieldOfView:int = CONFIG['RenderDistance']
    def __init__(self,save,name:str,elment:int,xy:tuple[int,int]=(0,0)):
        super().__init__()
        self.element = elment
        self.name = name
        self.save = save
        self.rect = pyge.pg.Rect(xy[0],xy[1],32,32)
        self.pos = self.rect.topleft
        
        self.LoadSprite()
        
    def LoadSprite(self):
        self.image = pge.createSurface(32,32, pyge.SRCALPHA)
        self.image.fill((190,100,210,255))
    
    def getWorldData(self):
        if not self.world:
            return {}
        else:
            return {
                'gravity': self.world.gravity,
                'zoom': self.world.zoom,
                'timeofday': self.world.time_of_day
            }
    
    def updateAttributes(self):
        self.speed = 3.0
        if self.dexterity > 1: self.speed = 3.0 * (self.dexterity*0.25) if self.dexterity >= 4 else 3.0 * (self.dexterity)
    
    def getInput(self):
        """
        Player Input
        
        Controls:
        AD←→ : Move left/right
        WS↑↓ : Move up/down
        LMB : Attack
        
        """
        
        LEFT = pge.hasKeyPressed(pyge.K_a) or pge.hasKeyPressed(pyge.K_LEFT)
        RIGHT = pge.hasKeyPressed(pyge.K_d) or pge.hasKeyPressed(pyge.K_RIGHT)
        UP = pge.hasKeyPressed(pyge.K_w) or pge.hasKeyPressed(pyge.K_UP)
        DOWN = pge.hasKeyPressed(pyge.K_s) or pge.hasKeyPressed(pyge.K_DOWN)
        
        if LEFT:
            self.direction.x = -1
        elif RIGHT:
            self.direction.x = 1
        else:
            self.direction.x *= 0.5
            if self.direction.x <= 0.01: self.direction.x = 0
        if UP:
            self.direction.y = -1
        elif DOWN:
            self.direction.y = 1
        else:
            self.direction.y *= 0.5
            if self.direction.y <= 0.01: self.direction.y = 0
    
    def getCorrectData(self) -> dict:
        s:dict = {}
        for var in self.__dict__.keys():
            if var in self.saveable:
                s[var] = self.__dict__[var]
        return s
        
    def loadData(self,data:dict):
        for key in data.keys():
            self.__dict__[key] = data[key]
    
    def setPos(self, position:tuple = (0,0)):
        """
        Set player position
        
        Same as: player.rect.topleft = position
        """
        self.pos = position
        self.rect.topleft = position
    
    def draw(self,surface:pyge.pg.surface):
        r:pyge.pg.rect.RectType = pyge.Rect(0, 0, 32, 32)
        r.center = (CURRENT_SCREEN_SIZE[0]/2, CURRENT_SCREEN_SIZE[1]/2)
        surface.blit(self.image, r)
        # pge.screen.blit(self.image, (CURRENT_SCREEN_SIZE[0]/2 - 16, CURRENT_SCREEN_SIZE[1]/2 - 16))
    
    def update(self):
        self.getWorldData()
        self.getInput()
        
        self.rect.topleft = self.pos
        
        return super().update()