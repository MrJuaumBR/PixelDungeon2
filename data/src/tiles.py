from typing import Any
from .config import *

class Tile(pyge.pg.sprite.Sprite):
    id:str
    type:str='base_tile'
    position:pyge.pg.math.Vector2
    start_pos:pyge.pg.math.Vector2
    size:pyge.pg.math.Vector2
    image:pyge.pg.SurfaceType
    
    canCollide:bool = True
    canDamage:bool = False
    
    spritesheet:dict
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__()
        self.rect = pyge.pg.Rect(*position.xy, *size.xy)
        self.rect.x = position.x
        self.rect.y = position.y
        self.position = position
        self.start_pos = position.copy()
        self.size = size
        self.id = self.generate_id()
        
        self.load_spritesheet()
        
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = TILES_SPRITESHEET.image_at(pyge.pg.Rect(0,0,32,32), 0)
        
        self.image = self.spritesheet['idle']
        
    def generate_id(self) -> str:
        return f'{self.type}_{os.urandom(8).hex()}'
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        # self.rect.topleft = self.position
        return super().update(*args, **kwargs)
    
    def draw(self, surface:pyge.pg.SurfaceType, zoom):
        
        self.rect.width = self.size.x * zoom
        self.rect.height = self.size.y * zoom
        
        self.rect.left = self.start_pos[0] * zoom
        self.rect.top = self.start_pos[1] * zoom
        
        surface.blit(self.image, self.rect.topleft)
        
class Tile_barrier(Tile):
    type = 'barrier'
    
    animate_clock:float = 1
    animate_frame:int = 0
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__(position, size)
    
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = [TILES_SPRITESHEET.image_at(pyge.pg.Rect(0,0,32,32), 0), TILES_SPRITESHEET.image_at(pyge.pg.Rect(0,33,32,32), 0)]
        
        self.image = self.spritesheet['idle'][0]
        
    def animate(self) -> None:
        add = self.animate_clock / FPS_OPTIONS[CONFIG['fps']]
        
        self.animate_frame += add
        if int(self.animate_frame) > len(self.spritesheet['idle'])-1:
            self.animate_frame = 0
            
        self.image = self.spritesheet['idle'][int(self.animate_frame)]
        
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.animate()
        return super().update(*args, **kwargs)
        
class Tile_water(Tile):
    type = 'water'
    
    animate_clock:float = 2 # Frames per second
    animate_frame:int = 0
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__(position, size)
    
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = [TILES_SPRITESHEET.image_at(pyge.pg.Rect(33,0,32,32), 0), TILES_SPRITESHEET.image_at(pyge.pg.Rect(33,33,32,32), 0)]
        
        self.image = self.spritesheet['idle'][self.animate_frame]
        
    def animate(self):
        # Adds 0.03 when Frames is running at 60
        # Adjust Animation Speed for the current running FPS
        # 0.03 = 60FPS
        # f(fps) = 2 / fps
        add = self.animate_clock / FPS_OPTIONS[CONFIG['fps']]
        
        self.animate_frame += add
        if int(self.animate_frame) > len(self.spritesheet['idle'])-1:
            self.animate_frame = 0
        
        self.image = self.spritesheet['idle'][int(self.animate_frame)]
        
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.animate()
        return super().update(*args, **kwargs)
        
        
class Tile_sand(Tile):
    type = 'sand'
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__(position, size)
    
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = TILES_SPRITESHEET.image_at(pyge.pg.Rect(65,0,32,32), 0)
        
        self.image = self.spritesheet['idle']
        
class Tile_rock(Tile):
    type = 'rock'
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__(position, size)
    
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = TILES_SPRITESHEET.image_at(pyge.pg.Rect(97,0,32,32), 0)
        
        self.image = self.spritesheet['idle']
        
class Tile_dirt(Tile):
    type = 'dirt'
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__(position, size)
    
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = TILES_SPRITESHEET.image_at(pyge.pg.Rect(129,0,32,32), 0)
        
        self.image = self.spritesheet['idle']
        
class Tile_grass(Tile):
    type = 'grass'
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__(position, size)
    
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = TILES_SPRITESHEET.image_at(pyge.pg.Rect(161,0,32,32), 0)
        
        self.image = self.spritesheet['idle']
        
class Tile_snow(Tile):
    type = 'snow'
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__(position, size)
    
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = TILES_SPRITESHEET.image_at(pyge.pg.Rect(193,0,32,32), 0)
        
        self.image = self.spritesheet['idle']