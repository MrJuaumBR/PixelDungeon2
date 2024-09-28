from .player import *
from .world import World
from ast import literal_eval

class Save:
    id:str
    Savename:str
    Saveworld:World
    Saveplayer:Player
    opened_times:int = 0
    def __init__(self, Savename, Savedifficulty, Saveelement) -> None:
        self.Savename = Savename
        self.Saveplayer = Player(self,Savename, Saveelement)
        self.Saveworld = World(self,self.Saveplayer, Savedifficulty)
        self.opened_times = 0
        
    def fix_dict(self, data:object) -> dict:
        x:dict = {}
        if type(data) == Player:
            data:Player
            x = data.getCorrectData()
        elif type(data) == World:
            data:World
            x = data.getCorrectData()
            
        return x
    
    def getData(self) -> bytes:
        correct_dict:dict = {}
        for key in self.__dict__.keys():
            if key in ['Saveplayer', 'Saveworld']:
                correct_dict[key] = self.fix_dict(self.__dict__[key])
            else:
                correct_dict[key] = self.__dict__[key]
        return base64.b64encode(str(correct_dict).encode('utf-8'))
    
    def loadData(self, data:bytes):
        # Decode
        data:bytes = base64.b64decode(data)
        data:str = bytes(data).decode('utf-8')
        data:dict = literal_eval(data)
        
        
        # Load
        self.opened_times = data['opened_times']
        self.id = data['id']
        self.Savename = data['Savename']
        
        # Load Objects
        self.Saveplayer = Player(self, '', 0)
        self.Saveplayer.loadData(data['Saveplayer'])
        
        self.Saveworld = World(self, self.Saveplayer, 0)
        self.Saveworld.loadData(data['Saveworld'])