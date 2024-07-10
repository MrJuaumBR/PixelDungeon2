import random

tiles_ids = {
    'water': 0.2,
    'sand': 0.3,
    'rock': 0.5,
    'dirt': 0.6,
    'grass': 0.8,
    'snow': 1,
    'barrier': 999
}

class MapGenerator:
    width:int = 256
    height:int = 192
    pixel_size:int = 32
    terrain:list[list[float,],]
    str_terrain:list[list[float,],]
    def __init__(self,width:int=256,height:int=192, pixel_size:int=32) -> None:
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
    
    def data(self) -> dict:
        return self.__dict__
    
    def load_data(self, data:dict):
        for key in data.keys():
            self.__dict__[key] = data[key]
    
    def generate_map(self) -> list:
        self.terrain = []
        self.str_terrain = []
        for y in range(self.height):
            self.terrain.append([])
            self.str_terrain.append([])
            for x in range(self.width):
                n = self.generate_noise(x,y, self.terrain.copy())
                self.terrain[y].insert(x, n)
        return self.terrain
    
    def noise(self, x:int,y:int, terrain:list[list[float]]) -> float:
        noise = 0
        if x == 0 and y == 0: noise = 999 # First of all
        elif y == 0 or y == self.height - 1: noise = 999 # First line or last line
        elif x == 0 or x == self.width - 1: noise = 999 # First column or last column
        else:
            x1:float = 0
            x2:float = 0
            x3:float = 0
            if x > 0: x1 = terrain[y][x-1]
            else: x1 = (terrain[(y if y > 0 else 1)-1][x]+random.uniform(0,1)) / 2
            if y > 0: x2 = terrain[y-1][x]
            else: x2 = (terrain[y][(x if x > 0 else 1)-1]+random.uniform(0,1)) / 2
            if x > 0 and y > 0: x3 = terrain[y-1][x-1]
            else: x3 = (terrain[(y if y > 0 else 1)-1][(x if x > 0 else 1)-1]+random.uniform(0,1)) / 2
            
            x = (x1+x2+x3+random.uniform(0,1)) / 4
            noise = x
        return round(noise,4)
    
    def generate_noise(self, x:int, y:int, terrain:list) -> float:
        tile = ''
        noise = self.noise(x,y, terrain)
        for tile_id in tiles_ids.keys():
            rang = tiles_ids[tile_id]
            if noise <= rang:
                tile = tile_id
                break
        self.str_terrain[y].insert(x, tile)
        return noise
    
    def simplified_version(self):
        s = ''
        for line in self.str_terrain:
            x = ''
            for w in line:
                x += str(w) + ', '
            s += x + '\n'
            
        return s
    
if __name__ == '__main__':
    generator = MapGenerator()
    generator.generate_map()
    print(generator.simplified_version())