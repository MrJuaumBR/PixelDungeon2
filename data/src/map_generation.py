"""
This file will generate the map.

How it will work?
    For the generation system will be used a system of rooms, wich will be pre-generated, and is a procedural generation of this rooms.
    Will have a list that will receive the "Lines" or the "Y Axis" of the map, and inside of it will have multiples "strings" that will be the id of tile
    
What is the rooms?
    rooms will be stored on the file: {root}/data/map_data.json
    
What is the tiles?
    The tiles will be stored on the file: {root}/data/src/tiles.py, but if you wanna only see ids, you can see "tile_ids" into {root}/data/src/config.py
"""

import json, random, datetime

class Room:
    """Represents a pre-generated room"""
    def __init__(self, room_data:dict={'id':None, 'width':None, 'height':None, 'data':None}):
        """
        Initializes a Room object from a dictionary

        :param room_data: A dictionary containing the room's data
        """
        self.id = room_data["id"] or None
        self.width = room_data["width"] or None
        self.height = room_data["height"] or None
        self.data = room_data["data"] or None
        
    def get_dict(self) -> dict:
        return self.__dict__
    
    def load_dict(self, data:dict):
        self.__dict__ = data

class MapGeneration:
    """Generates a map based on pre-generated rooms"""
    saveable:list[str,] = ['map_grid', 'num_rooms', 'room_theme', 'rooms']
    
    map_grid:list[list[str,]] = []
    num_rooms:int
    room_theme:str
    rooms:list[Room,]
    
    mp_wid:int = 100
    mp_hei:int = 72
    def __init__(self, num_rooms, room_theme):
        """
        Initializes a MapGeneration object

        :param num_rooms: The number of rooms to generate
        :param room_theme: The theme of the rooms (not used in this example)
        """
        self.num_rooms = num_rooms
        self.room_theme = room_theme
        self.rooms = []

    def load_dict(self, data:dict):
        """
        Load the dictionarie of this system
        
        :param data: The dictionarie
        """
        
        for key in data.keys():
            if key in MapGeneration.saveable:
                if key == 'rooms':
                    for room in data[key]:
                        self.rooms.append(Room().load_dict(room))
                else:
                    setattr(self, key, data[key])
         
    def get_dict(self) -> dict:
        """
        Transform this system into a dictionarie
        """
        d:dict = {}
        for key in MapGeneration.saveable:
            if key == 'rooms':
                if key not in d.keys(): d[key] = []
                for room in self.rooms:
                    room: Room
                    if room:
                        try:
                            d[key].append(room.get_dict())
                        except Exception as e:
                            print(f'\t! [Error in MapGeneration - get_dict] {e}\n')
                            print(f'\t- Room Data: {room.__dict__}')
                    
            else:
                d[key] = self.__dict__[key]
                
        return d
    
    def random_room(self,room_data:dict, blacklist:list[str,] = ['Starter']):
        x = random.choice(room_data)
        if x in blacklist:
            return self.random_room(room_data, blacklist)
        else:
            return x
    
    def load_rooms(self, filename):
        """
        Loads pre-generated rooms from a JSON file

        :param filename: The name of the JSON file
        """
        with open(filename, "r") as file:
            room_data = json.load(file)['rooms']
            for _ in range(self.num_rooms):
                self.rooms.append(Room(self.random_room(room_data)))

    def generate_map(self):
        """
        Generates a map by randomly placing the pre-generated rooms

        :return: A 2D list representing the generated map
        """
        # Initialize an empty map
        map_width = self.mp_wid  # arbitrary width
        map_height = self.mp_hei  # arbitrary height
        map_grid = [[" " for _ in range(map_width)] for _ in range(map_height)]

        # Randomly place the rooms
        for room in self.rooms:
            room:Room
            # Choose a random position for the room
            x = random.randint(0, map_width - room.width)
            y = random.randint(0, map_height - room.height)

            # Place the room on the map
            for i in range(room.height):
                for j in range(room.width):
                    # i == Y Axis, j == X Axis
                    map_grid[y + i][x + j] = room.data[i][j]

        self.map_grid = map_grid
        return map_grid
    
    def output_log_file(self):
        with open("./map_log.txt",'w+') as file:
            text_list = ["\n\nMap Log Output\n\n",f"\t\t{datetime.datetime.now()}\n\n"]
            for y,row in enumerate(self.map_grid):
                for x,k in enumerate(row):
                    if str(k) in ['',' ','-1']:
                        text_list.append(f'.')
                    else:
                        text_list.append(f'{str(k)}')
                    if x >= len(row) - 1:
                        text_list.append(f'\n')
            text_list.append("\n\n Exited. \n\n")
            
            file.writelines(text_list)
                        

# Example usage
if __name__ == "__main__":
    map_gen = MapGeneration(5, "dungeon")
    map_gen.load_rooms("./data/map_data.json")
    map_gen.generate_map()
    map_gen.output_log_file()