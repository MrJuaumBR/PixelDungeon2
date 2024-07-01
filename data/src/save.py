from .player import *
from .world import World

class Save:
    id:str
    Savename:str
    Saveworld:World
    Saveplayer:Player
    def __init__(self, Savename, Savedifficulty, Saveelement) -> None:
        self.Savename = Savename
        self.Saveplayer = Player(Savename, Saveelement)
        self.Saveworld = World(self.Saveplayer, Savedifficulty)
        
    def getData(self) -> bytes:
        return base64.b64encode(pickle.dumps(self))
    
    def loadData(self, data:bytes):
        self.__dict__ = pickle.loads(base64.b64decode(data)).__dict__