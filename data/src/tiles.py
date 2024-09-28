from .config import *

TILE_SIZE = 32

class BaseTile(pyge.pg.sprite.Sprite):
    type:str = 'base_tile'
    saveable:list[str,] = ['rect','position']
    rect:pg.rect.RectType
    position:pg.math.Vector2 = pg.math.Vector2(0,0)
    
    frames:list[pg.surface.Surface,] = []
    
    animation_frame:int = 0
    animation_frame_increment:float = 0.17
    
    world_offset:pg.math.Vector2 = pg.math.Vector2(0,0)
    offset_rect:pg.rect.RectType = None
    
    RANGE:float = 3.0
    def __init__(self, position:pg.math.Vector2) -> None:
        super().__init__()
        
        self.position.xy = position
        self.rect = pg.Rect(*position.xy, TILE_SIZE, TILE_SIZE)
        
        self.load_surface()
        
    def load_surface(self):
        pass
    
    def frame(self):
        if len(self.frames) <= 0:
            print('No Frames Loaded!')
            surf = pg.Surface((32,32))
            pge.draw_rect((0,0), (32,32), pge.Colors.random(), screen=surf)
            
            self.frames.append(surf)
            
        return self.frames[int(self.animation_frame)]
    
    def update(self, player):
        self.offset_rect = pg.Rect(*(self.position.xy+self.world_offset).xy, TILE_SIZE, TILE_SIZE)
        
        self.animation_frame += self.animation_frame_increment
        if self.animation_frame >= len(self.frames):
            self.animation_frame = 0
# Animated
class Barrier(BaseTile):
    type:str = 'barrier'
    animation_frame_increment:float = 0.075
    def load_surface(self):
        i = TILES_SPRITESHEET.images_at([(0,0,32,32),(0,32,32,32)])
        [self.frames.append(frame) for frame in i]
        
class Water(BaseTile):
    type:str = 'water'
    animation_frame_increment:float = 0.075
    def load_surface(self):
        i = TILES_SPRITESHEET.images_at([pg.Rect(32,0,32,32),pg.Rect(32,32,32,32)])
        [self.frames.append(frame) for frame in i]

class Door(BaseTile):
    type:str = 'door'
    area:pg.rect.RectType
    def load_surface(self):
        self.frames = []
        self.frames.append(TILES_SPRITESHEET.image_at(pg.Rect(384,32,32,32)))
        self.area = pg.Rect(self.position.xy[0], self.position.xy[1],32*self.RANGE,32*self.RANGE)
        
    def update(self, player):
        super().update(player)
        self.area.center = self.offset_rect.center
        if self.area.colliderect(player.rect):
            print("Colliding Player!")

# Static
class Sand(BaseTile):
    type:str = 'sand'
    def load_surface(self):
        self.frames.append(TILES_SPRITESHEET.image_at(pg.Rect(64,0,32,32)))

class Stone(BaseTile):
    type:str = 'stone'
    def load_surface(self):
        self.frames.append(TILES_SPRITESHEET.image_at(pg.Rect(96,0,32,32)))

class Dirt(BaseTile):
    type:str = 'dirt'
    def load_surface(self):
        self.frames.append(TILES_SPRITESHEET.image_at(pg.Rect(128,0,32,32)))
        
class Grass(BaseTile):
    type:str = 'grass'
    def load_surface(self):
        self.frames.append(TILES_SPRITESHEET.image_at(pg.Rect(160,0,32,32)))
        
class Snow(BaseTile):
    type:str = 'snow'
    def load_surface(self):
        self.frames.append(TILES_SPRITESHEET.image_at(pg.Rect(192,0,32,32)))
        
class Red_Brick(BaseTile):
    type:str = 'red_brick'
    def load_surface(self):
        self.frames = []
        self.frames.append(TILES_SPRITESHEET.image_at(pg.Rect(224,0,32,32)))

class Green_Brick(BaseTile):
    type:str = 'green_brick'
    def load_surface(self):
        self.frames = []
        self.frames.append(TILES_SPRITESHEET.image_at(pg.Rect(256,32,32,32)))

class Blue_Brick(BaseTile):
    type:str = 'blue_brick'
    def load_surface(self):
        self.frames = []
        self.frames.append(TILES_SPRITESHEET.image_at(pg.Rect(288,0,32,32)))
        
class Yellow_Brick(BaseTile):
    type:str = 'yellow_brick'
    def load_surface(self):
        self.frames = []
        self.frames.append(TILES_SPRITESHEET.image_at(pg.Rect(320,0,32,32)))

class Purple_Brick(BaseTile):
    type:str = 'purple_brick'
    def load_surface(self):
        self.frames = []
        self.frames.append(TILES_SPRITESHEET.image_at(pg.Rect(352,0,32,32)))

