"""
MTD_Mod_Name: Base Mod
MTD_Mod_Author: MrJuaum
MTD_Mod_Version: 0.0.1
MTD_Mod_Description: Just a simple base mod, for examples
MTD_Mod_RCode: 1
"""

import pygameengine

class Mod:
    # Example
    variable_example = 'Example'
    
    # Required
    engine: pygameengine.PyGameEngine
    gameObj:object
    screen_affects = [0]
    kwargs = {}
    def __init__(self, game_engine: pygameengine.PyGameEngine, game_object:object):
        self.engine = game_engine
        self.gameObj = game_object
        self.kwargs = {}
        
    def screen_handler(self, game_engine: pygameengine.PyGameEngine, game_object:object, **kwargs):
        self.engine = game_engine
        if kwargs:
            self.kwargs = kwargs
        
        # Receives Screen Id
        screen_id = game_object.screen_id
        if screen_id in self.screen_affects:
            # Converts it to the name:
            # Screen Ids:
            # Main Menu: 0
            # Save Select: 1
            # Options: 2
            # Mods: 3
            # In Game: 4
            # Confirm Exit: 5
            # Create Save: 6
            if screen_id == 0:
                self.main_menu(game_object)
            
    def main_menu(self,game_object:object):
        screen_size = self.engine.screen.get_size()
        self.engine.draw_text((0,screen_size[1]-50),'Base Mod Loaded!', self.engine._findFont(2), self.engine.Colors.WHITE)