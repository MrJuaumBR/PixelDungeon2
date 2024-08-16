from .config import *

RECOVER_TIME:float = 3.0
GRAVITY:float = 1



class Player(pyge.pg.sprite.Sprite):
    saveable = ['element','name','pos','level','xp','points', 'strength', 'intelligence', 'dexterity', 'defence', 'max_health', 'health', 'max_mana', 'mana', 'is_dead', 'damage_taken_clock', 'locked']
    element = 0
    name =''
    rect:pyge.pg.Rect
    irect:pyge.pg.Rect
    type = 'player'
    pos:tuple = (0,0)
    image:pyge.pg.SurfaceType
    
    is_spawned:bool = False
    world:object = None
    direction:pyge.pg.math.Vector2 = pyge.pg.math.Vector2(0,0)
    dirr:str = 'right'
    locked:bool = False
    
    # Attributes
    level:int = 1
    xp:float = 0.0
    points:int = 3
    speed:float = 3.0
    jump_speed:float = 16.0
    is_dead:bool = False
    on_floor:bool = False
    
    # Stats
    strength:int = 1
    intelligence:int = 1
    dexterity:int = 1
    defence:int = 1
    max_health:int = 100
    health:int = 100
    max_mana:int = 100
    mana:int = 100
    
    # Cooldowns
    damage_taken_clock:float = 0.0
    
    FieldOfView:int = RenderDistance_OPTIONS[CONFIG['RenderDistance']]
    def __init__(self,save,name:str,elment:int,xy:tuple[int,int]=(0,0)):
        super().__init__()
        self.element = elment
        self.name = name
        self.save = save
        self.rect = pyge.pg.Rect(xy[0],xy[1],32,32)
        self.irect = self.rect.copy()
        self.pos = self.rect.topleft
        
        self.FieldOfView = RenderDistance_OPTIONS[CONFIG['RenderDistance']]
        self.FOV_Rect = pyge.pg.Rect(0,0,self.FieldOfView, self.FieldOfView)
        
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
            if abs(self.direction.x) <= 0.01: self.direction.x = 0
            
        if UP and self.on_floor and not self.is_dead:
            self.direction.y = -self.jump_speed
        # elif DOWN:
        #     pass
        else:
            self.direction.y *= 0.5
            if abs(self.direction.y) <= 0.01: self.direction.y = 0
    
    def getCorrectData(self) -> dict:
        s:dict = {}
        for var in self.__dict__.keys():
            if var in self.saveable:
                s[var] = self.__dict__[var]
        return s
        
    def loadData(self,data:dict):
        for key in data.keys():
            self.__dict__[key] = data[key]
    
    def setPos(self, position:tuple = (0,0), part_linked:str='topleft'):
        """
        Set player position
        
        Same as: player.rect.topleft = position
        """
        if part_linked == 'topleft':
            self.rect.topleft = position
        elif part_linked == 'topright':
            self.rect.topright = position
        elif part_linked == 'bottomleft':
            self.rect.bottomleft = position
        elif part_linked == 'bottomright':
            self.rect.bottomright = position
        elif part_linked == 'center':
            self.rect.center = position
            
        self.pos = self.rect.topleft
        
        
    # Player Logic
    def take_damage(self, damage:int):
        if not self.is_dead:
            self.health -= damage
            self.damage_taken_clock = pge.TimeSys.s2f(RECOVER_TIME)
            if self.health <= 0:
                self.health = 0
                self.is_dead = True
                
    def heal(self, heal:int):
        if not self.is_dead:
            self.health += heal
            if self.health > self.max_health:
                self.health = self.max_health
    
    def auto_heal(self):
        if self.damage_taken_clock <= 0 and not self.is_dead:
            self.heal(self.health*0.01)
            self.damage_taken_clock = pge.TimeSys.s2f(RECOVER_TIME/10)
            
    def cooldowns_refresh(self):
        if self.damage_taken_clock > 0:
            self.damage_taken_clock -= 0
            if self.damage_taken_clock <= 0:
                self.damage_taken_clock = 0
        
    def getGravity(self) -> float:
        return GRAVITY
    def apply_gravity(self):
        
        self.direction.y += GRAVITY
        self.rect.y += self.direction.y * self.speed
        self.on_floor = False
                
    # Game
    
    def draw(self,surface:pyge.pg.surface,zoom:float):
        r:pyge.pg.rect.RectType = pyge.Rect(0, 0, 32, 32)
        r.center = (CURRENT_SCREEN_SIZE[0]/2, CURRENT_SCREEN_SIZE[1]/2)
        self.FOV_Rect.center = r.center
        
        size = self.rect.width * zoom, self.rect.height * zoom
        
        surface.blit(pg.transform.scale(self.image, size), r)
        # pge.screen.blit(self.image, (CURRENT_SCREEN_SIZE[0]/2 - 16, CURRENT_SCREEN_SIZE[1]/2 - 16))
    
    def update(self):
        self.cooldowns_refresh()
        self.auto_heal()
        self.getWorldData()
        self.getInput()
        
        return super().update()