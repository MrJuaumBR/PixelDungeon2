from typing import Any
from .config import *

class Tile(pyge.pg.sprite.Sprite):
    id:str
    type:str='base_tile'
    position:pyge.pg.math.Vector2
    start_pos:pyge.pg.math.Vector2
    size:pyge.pg.math.Vector2
    image:pyge.pg.SurfaceType
    
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
        self.spritesheet['idle'] = TILES_SPRITESHEET.image_at(pyge.pg.Rect(1,1,32,32))
        
        self.image = self.spritesheet['idle']
        
    def generate_id(self) -> str:
        return f'{self.type}_{os.urandom(8).hex()}'
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.topleft = self.position
        return super().update(*args, **kwargs)
    
    def draw(self, surface:pyge.pg.SurfaceType):
        surface.blit(self.image, self.rect)
        
class Tile_barrier(Tile):
    type = 'barrier'
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__(position, size)
    
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = TILES_SPRITESHEET.image_at(pyge.pg.Rect(1,1,32,32))
        
        self.image = self.spritesheet['idle']
        
class Tile_water(Tile):
    type = 'water'
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__(position, size)
    
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = TILES_SPRITESHEET.image_at(pyge.pg.Rect(34,1,32,32))
        
        self.image = self.spritesheet['idle']
        
class Tile_sand(Tile):
    type = 'sand'
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__(position, size)
    
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = TILES_SPRITESHEET.image_at(pyge.pg.Rect(67,1,32,32))
        
        self.image = self.spritesheet['idle']
        
class Tile_rock(Tile):
    type = 'rock'
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__(position, size)
    
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = TILES_SPRITESHEET.image_at(pyge.pg.Rect(100,1,32,32))
        
        self.image = self.spritesheet['idle']
        
class Tile_dirt(Tile):
    type = 'dirt'
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__(position, size)
    
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = TILES_SPRITESHEET.image_at(pyge.pg.Rect(133,1,32,32))
        
        self.image = self.spritesheet['idle']
        
class Tile_grass(Tile):
    type = 'grass'
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__(position, size)
    
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = TILES_SPRITESHEET.image_at(pyge.pg.Rect(166,1,32,32))
        
        self.image = self.spritesheet['idle']
        
class Tile_snow(Tile):
    type = 'snow'
    def __init__(self, position:pyge.pg.math.Vector2, size:pyge.pg.math.Vector2) -> None:
        super().__init__(position, size)
    
    def load_spritesheet(self) -> None:
        self.spritesheet = {}
        self.spritesheet['idle'] = TILES_SPRITESHEET.image_at(pyge.pg.Rect(199,1,32,32))
        
        self.image = self.spritesheet['idle']