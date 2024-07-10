from .config import *

from .map_generation import MapGenerator
from .player import Player
from .tiles import *
import threading

class World(pyge.pg.sprite.Group):
    saveable = ['difficulty', 'zoom']
    difficulty = 0
    player:Player
    surface:pyge.pg.SurfaceType
    mapgen:MapGenerator
    save = None
    zoom = 1
    def __init__(self, save,player:Player, diffculty = 0):
        super().__init__()
        self.save = save
        self.player = player
        self.difficulty = diffculty
        self.mapgen = MapGenerator(256,192,32)
        self.surface = pge.createSurface(self.mapgen.width*self.mapgen.pixel_size,self.mapgen.height*self.mapgen.pixel_size)
    
    
    def gen_world(self):
        if self.save.opened_times <= 0:
            print("World Generating...")
            self.mapgen.generate_map()
            
        terr = self.mapgen.str_terrain
        # getattr(sys.modules[__name__], f'{}_{terr.lower()}')
        for y in range(len(terr)):
            for x in range(len(terr[y])):
                try:
                    t = getattr(sys.modules[__name__], f'Tile_{terr[y][x]}')
                except Exception as e:
                    print(e)
                else:
                    self.add(t(pyge.pg.math.Vector2(x*self.mapgen.pixel_size,y*self.mapgen.pixel_size),pyge.pg.math.Vector2(self.mapgen.pixel_size,self.mapgen.pixel_size)))
    
    def draw(self):
        for sprite in self.sprites():
            # Check if sprite is in Field Of View
            # Player Field Of View
            try:
                P_FOV:pyge.pg.Rect = pyge.pg.Rect(0,0,800, 600)
                P_FOV.center = self.player.rect.center
                sprite:Tile
                if sprite.rect.colliderect(P_FOV):
                    sprite.draw(self.surface)
                else: 
                    pass
            except Exception as e:
                print(f'{e}')
            
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