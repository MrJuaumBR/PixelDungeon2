import io,os,random
import time

tiles_ids = {
    0: 'water',
    1: 'sand',
    2: 'rock',
    3: 'dirt',
    4: 'grass',
    5: 'snow',
    'p': 'player',
    -1: 'air',
    -2: 'barrier'
}
 
class MapGenerator:
    width:int = 256
    height:int = 192
    pixel_size:int = 32
    terrain:list[list[int,],] = []
    str_terrain:list[list[str,],] = []
    map:str = 'default-map'
    maps_json:dict = None
    maps_file:io.BufferedReader = None
    
    last_modification:float = None
    def __init__(self,width:int=256,height:int=192, pixel_size:int=32,map:str='default-map') -> None:
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        
        self.map = map
        self.maps_json:dict = self.load_maps_json()
    
    def load_maps_json(self) -> dict:
        self.last_modification = os.path.getmtime('data/maps.json')
        with open('data/maps.json', 'rb') as f:
            self.maps_file = f
            import json
            j = json.loads(f.read())
            return j
    
    def data(self) -> dict:
        x = {}
        for key in self.__dict__.keys():
            if key not in ['maps_file','last_modification','maps_json','terrain','str_terrain']:
                x[key] = self.__dict__[key]
        return x
    
    def load_data(self, data:dict):
        for key in data.keys():
            self.__dict__[key] = data[key]
    
    def generate_map(self) -> list:
        self.terrain = []
        self.str_terrain = []
        
        self.terrain = self.maps_json['maps'][self.map]['terrain']
        self.simplified_version()
        
        return self.terrain
    
    def hotreload_map(self) -> bool:
        if self.last_modification < os.path.getmtime('data/maps.json'):
            self.maps_json:dict = self.load_maps_json()
            self.generate_map()
            self.last_modification = os.path.getmtime('data/maps.json')
            return True
        return False        

    def simplified_version(self) -> list:
        for line in self.terrain:
            l = []
            for id in line:
                l.append(tiles_ids[id])
            self.str_terrain.append(l)
        
        return self.str_terrain
    
if __name__ == '__main__':
    generator = MapGenerator()
    generator.generate_map()
    generator.hotreload_map()