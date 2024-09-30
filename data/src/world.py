import pickle, base64, threading
from .player import Player
from pygame.sprite import AbstractGroup
from .map_generation import MapGeneration, Room
from .config import *
import data.src.tiles as tiles

class World(pyge.pg.sprite.Group):
    saveable:list[str,] = ['diffculty','mpgen','offset']
    
    save:object
    
    difficulty:int = 0
    player:Player
    
    offset:pg.math.Vector2 = pg.math.Vector2(0,0)
    
    NUMBER_OF_ROOMS_RNG:tuple[int, int] = (8,14)
    
    mpgen:MapGeneration
    
    zoom:float = 1.0
    
    draw_fov:pg.rect.RectType = None
    
    internal_surface:pg.SurfaceType
    def __init__(self, save, SavePlayer, Savediff) -> None:
        super().__init__()
        
        self.difficulty = Savediff
        self.player = SavePlayer
        self.save = save
        self.mpgen = MapGeneration(random.randint(*World.NUMBER_OF_ROOMS_RNG), 'dungeon')
        self.internal_surface:pg.SurfaceType = pg.Surface((4000,4000),pg.SRCALPHA)
        if self.save.opened_times <= 0:
            self.mpgen.load_rooms("./data/map_data.json")
            self.mpgen.generate_map()
        
        self.save.opened_times += 1
        
        self.draw_fov =pg.Rect(0,0,RenderDistance_OPTIONS[CONFIG['RenderDistance']],RenderDistance_OPTIONS[CONFIG['RenderDistance']])
            
    
    def update(self):
        for sprite in self.sprites():
            if sprite.type != 'player':
                sprite.update(self.player)
            else:
                sprite.update()
    
    def get_sprites(self):
        for y,line in enumerate(self.mpgen.map_grid):
            for x,sprite_id in enumerate(line):
                # Get what sprite it is by its id
                if str(sprite_id) in tiles_ids.keys():
                    Tile_Name:str = tiles_ids[str(sprite_id)]
                    
                    # Load the sprite
                    try:
                        if not ( Tile_Name in ['air']):
                            Tile = getattr(tiles, Tile_Name)
                            
                            self.add(Tile(pg.math.Vector2(x*TILE_SIZE,y*TILE_SIZE)))
                    except Exception as e:
                        print(f'[Error in World - get_sprites] {e}')
                
    
    def draw(self):
        self.internal_surface.fill(self.save.background_color)
        for sprite in self.sprites():
            if sprite.type != 'player':
                sprite:tiles.BaseTile
                
                sprite_pos = sprite.rect.topleft + self.offset
                sprite_pos:pg.rect.RectType = pg.Rect(*sprite_pos.xy, TILE_SIZE*self.zoom, TILE_SIZE*self.zoom)
                if sprite_pos.colliderect(self.draw_fov):    
                
                    sprite.world_offset = self.offset
                    f = pg.transform.scale(sprite.frame(),(TILE_SIZE*self.zoom,TILE_SIZE*self.zoom))
                    if sprite.type == 'door':
                        r = sprite.area.copy()
                        r.center = sprite_pos.center
                        x = pg.Surface((r.width,r.height),pg.SRCALPHA)
                        x.fill((100,100,100))
                        if sprite.player_in_range:
                            x.fill(pge.Colors.YELLOW.rgb)
                        pge.draw_text((r.left,r.top), f'{r.top}, {r.bottom}, {r.left}, {r.right}' ,PPF12, pge.Colors.WHITE, x)
                        self.internal_surface.blit(x, r)
                    
                    self.internal_surface.blit(f, sprite_pos)
            elif sprite.type == 'player':
                pass
                
        rect = pg.Rect(0,0,*self.internal_surface.get_size())
        rect.topleft = (0,0)
        pge.screen.blit(self.internal_surface, rect)
        self.draw_player()
        
    def draw_player(self):
        F1 = pge.hasKeyPressed(pg.K_F1)
        sprite:Player = self.player
                
        sprite_pos = pg.Rect(0,0,*sprite.frame().get_size())
        sprite_pos.center = pge.screen.get_rect().center
        
        self.draw_fov.center = sprite_pos.center
        
        self.offset.x += sprite.movement.x * sprite.speed
        self.offset.y += sprite.movement.y * sprite.speed
        
        sprite.world_offset = self.offset
        if not F1:
            pge.screen.blit(sprite.frame(), sprite_pos)
    
    def loadData(self, data:dict):
        for key in data.keys():
            if key in World.saveable:
                if key == 'mpgen':
                    self.mpgen.load_dict(data[key])
                    self.get_sprites() # Load sprites
                elif key == 'offset':
                    self.offset = pg.math.Vector2(data[key][0], data[key][1])
                else:
                    setattr(self, key, data[key])
                    
        
    def getCorrectData(self) -> dict:
        d:dict = {}
        for key, value in self.__dict__.items():
            if key in World.saveable:
                if key == 'mpgen':
                    d[key] = self.mpgen.get_dict()
                elif key == 'offset':
                    d[key] = [value.x, value.y]
                else:
                    d[key] = value
                    
        return d