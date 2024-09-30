"""
MTD_Mod_Name: Debug Mod
MTD_Mod_Author: MrJuaum
MTD_Mod_Version: 0.0.1
MTD_Mod_Description: just a mod for debugging
"""

import pygameengine, JPyDB,os, signal, time

class Mod:
    engine: pygameengine.PyGameEngine
    gameObj:object

    screen_affects = [2,1,4]
    screens_widgets = {}
    kwargs = {}
    def __init__(self, game_engine: pygameengine.PyGameEngine, game_object:object):
        self.engine = game_engine
        self.gameObj = game_object
        self.kwargs = {}
        
        self.create_widgets()
    
    def create_widgets(self):
        RATIO = self.gameObj.ratio
        self.screens_widgets['options'] = {}
        self.screens_widgets['options']['ClearSavesBtn'] = pygameengine.Button(self.engine, (20*RATIO, 440*RATIO), self.engine._findFont(6),'Clear Saves', [self.engine.Colors.WHITE, self.engine.Colors.DARKGRAY, self.engine.Colors.GRAY])
        self.screens_widgets['options']['DeleteDatabaseBtn'] = pygameengine.Button(self.engine, (20*RATIO, 480*RATIO), self.engine._findFont(6),'Delete Database', [self.engine.Colors.WHITE, self.engine.Colors.DARKGRAY, self.engine.Colors.GRAY])
        self.screens_widgets['options']['OutputDatabaseBtn'] = pygameengine.Button(self.engine, (20*RATIO, 520*RATIO), self.engine._findFont(6),'Output Database', [self.engine.Colors.WHITE, self.engine.Colors.DARKGRAY, self.engine.Colors.GRAY])
        
        
        self.screens_widgets['save_select'] = {}
        self.screens_widgets['save_select']['NewWorldForSelectedBtn'] = pygameengine.Button(self.engine, (240*RATIO, 525*RATIO), self.engine._findFont(10),'Regenerate World(Selected)', [self.engine.Colors.WHITE, self.engine.Colors.DARKGRAY, self.engine.Colors.GRAY])
        
        self.screens_widgets['in_game'] = {}
        self.screens_widgets['in_game']['ShowMenuBtn'] = pygameengine.Button(self.engine, (1*RATIO, 28*RATIO), self.engine._findFont(13),'Show Menu', [self.engine.Colors.WHITE, self.engine.Colors.DARKGRAY, self.engine.Colors.GRAY])
        

    def screen_handler(self, game_engine: pygameengine.PyGameEngine, game_object:object, kwargs:dict={}):
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
            if screen_id == 2:
                self.options()
            elif screen_id == 1:
                self.save_select()
            elif screen_id == 4:
                self.in_game()
    
    def in_game(self):
        RATIO = self.gameObj.ratio
        self.engine.draw_widgets(self.screens_widgets['in_game'].values())
        world = self.kwargs['world']
        player = self.kwargs['player']
        
        self.engine.draw_rect(player.rect_offset.topleft, (32,32), self.engine.Colors.LIGHTBLUE, screen=self.engine.screen)
        
        self.engine.draw_text((1*RATIO, 1*RATIO), f'World Offset(X,Y): {round(world.offset.x,1)},{round(world.offset.y,1)}, Player Offset(X,Y): {round(player.rect_offset.left,1)},{round(player.rect_offset.top,1)}', self.engine._findFont(12), self.engine.Colors.WHITE)
        self.engine.draw_text((1*RATIO, 14*RATIO), f'World Offset(Player, [X,Y]): {round(player.world_offset.x,1)},{round(player.world_offset.y,1)}, Save ID: {player.save.id}', self.engine._findFont(12), self.engine.Colors.WHITE)

            
    
    def save_select(self):
        self.engine.draw_widgets(self.screens_widgets['save_select'].values())
        if 'current_save' in self.kwargs.keys():
            ratio = self.gameObj.ratio
                
            self.engine.draw_text((240*ratio, 500*ratio), 'Save id: '+str(self.kwargs["current_save"].id if self.kwargs["current_save"] else 'None'), self.engine._findFont(10), self.engine.Colors.WHITE)
            if self.kwargs['current_save']:
                
                if self.screens_widgets['save_select']['NewWorldForSelectedBtn'].value:
                    save = self.kwargs["current_save"]
                    pyd:JPyDB.pyDatabase = self.gameObj.pyDatabase
                    
                    print(f'Regenerating World({save.Savename})...')
                    save.Saveworld.mapgen.generate_map()
                    pyd.database.update_value('saves', 'data', save.id, save.getData())
                    pyd.save()
    
    def options(self):
        self.engine.draw_widgets(self.screens_widgets['options'].values())
        pyd:JPyDB.pyDatabase = self.gameObj.pyDatabase
        if self.screens_widgets['options']['ClearSavesBtn'].value:
            save_table:JPyDB.Tables = pyd.database.tables['saves']
            for save in save_table.get_all():
                pyd.database.delete_values('saves', save['id'])
            pyd.save()
            print('Saves Cleared')
        if self.screens_widgets['options']['DeleteDatabaseBtn'].value:
            pyd.deleteDatabase()
            print('Database Deleted\nExiting...')
            os.kill(self.gameObj.pid, signal.SIGTERM)
            self.engine.exit()
            
        if self.screens_widgets['options']['OutputDatabaseBtn'].value:
            print('\n\nDatabase Output:\n')
            pyd.get_content()
            print('\n\n')
            time.sleep(1)