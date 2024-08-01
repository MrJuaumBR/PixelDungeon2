from typing import Any
from .config import *

from .map_generation import MapGenerator
from .player import Player
from .tiles import *

class World(pyge.pg.sprite.Group):
    saveable = ['difficulty', 'zoom']
    difficulty = 0
    player:Player
    surface:pyge.pg.SurfaceType
    mapgen:MapGenerator
    save = None
    zoom = 1
    gravity:float = 7.8
    time_of_day:int = 0
    
    x_shift:int = 0
    y_shift:int = 0
    
    bg_color:tuple[int,int,int] = (0,0,0)
    
    can_draw:bool = False
    def __init__(self, save,player:Player, diffculty = 0):
        super().__init__()
        self.save = save
        self.player = player
        self.difficulty = diffculty
        self.mapgen = MapGenerator(32,32,32)
        self.surface = pge.createSurface(self.mapgen.width*self.mapgen.pixel_size,self.mapgen.height*self.mapgen.pixel_size)
    def gen_world(self):
        if self.save.opened_times <= 0:
            print("World Generating...")
            self.mapgen.generate_map()
            
        terr = self.mapgen.str_terrain
        
        for y in range(len(terr)):
            for x in range(len(terr[y])):
                if terr[y][x] != 'air' and terr[y][x] != 'player':
                    sprite = getattr(sys.modules[__name__], f'Tile_{terr[y][x]}')(pyge.pg.math.Vector2(x*self.mapgen.pixel_size,y*self.mapgen.pixel_size),pyge.pg.math.Vector2(self.mapgen.pixel_size,self.mapgen.pixel_size))
                    try:
                        self.add(sprite)
                    except Exception as e:
                        print(e)
                elif terr[y][x] == 'player' and self.player.is_spawned == False:
                    self.player.setPos((CURRENT_SCREEN_SIZE[0]/2 - 16, CURRENT_SCREEN_SIZE[1]/2 - 16))
                    self.player.is_spawned = True
                    
                    self.add(Tile_dirt(pyge.pg.math.Vector2(CURRENT_SCREEN_SIZE[0]/2, CURRENT_SCREEN_SIZE[1]/2),pyge.pg.math.Vector2(32,32)))
                    
                    # Update X and Y Shift
                    self.x_shift = self.player.rect.left + self.mapgen.width*2
                    self.y_shift = self.player.rect.top + self.mapgen.width*2
    
    def delete_tiles(self):
        for sprite in self.sprites():
            if sprite.type != 'player':
                self.remove(sprite)
    
    def scroll_x(self):
        player = self.player
        if player:
            direction_x = player.direction.x
            
            speed = (self.player.speed * 1.1) * self.zoom
            
            self.x_shift += speed * direction_x
            
    
    def scroll_y(self):
        player = self.player
        if player:
            direction_y = player.direction.y
            
            speed = (self.player.speed * 1.1) * self.zoom
            
            self.y_shift += speed * direction_y
            
    
    def ScrollHandler(self):
        self.scroll_x()
        self.scroll_y()
            
    
    def draw(self):
        changed:bool = self.mapgen.hotreload_map()
        self.surface.fill(self.bg_color)
        if changed:
            print('Map Reload')
            # Clear sprites
            self.delete_tiles()
            
            self.gen_world()
        for sprite in self.sprites():
            # Check if sprite is in Field Of View
            # Player Field Of View
            sprite.position = pyge.pg.math.Vector2(sprite.start_pos.x - self.x_shift,sprite.start_pos.y - self.y_shift)
            sprite.draw(self.surface)
        
        # Draw Player
        self.player.draw(self.surface)
        
        pge.screen.blit(self.surface, (0,0))
    def update(self, *args: Any, **kwargs: Any) -> None:
        for sprite in self.sprites():
            if sprite.type != 'player':
                sprite.update(self.player)
            else:
                sprite.update()
                
        if not self.player.world:
            self.player.world = self
        self.player.update()
        self.ScrollHandler()
        return super().update(*args, **kwargs)
    
    def getCorrectData(self) -> dict:
        s:dict = {}
        for var in self.__dict__.keys():
            if var in self.saveable:
                s[var] = self.__dict__[var]
                
        s['mapgen'] = self.mapgen.data()
        return s
            
    def loadData(self,data:dict):
        for key in data.keys():
            if key in self.saveable:
                self.__dict__[key] = data[key]
            elif key == 'mapgen':
                self.mapgen = MapGenerator(0,0,0)
                self.mapgen.load_data(data[key])