import os, sys, importlib, threading,shutil
import pygameengine

_ACCEPTABLE_FILES = ['pyplugin','mod','pymod','py']

class Mods:
    mods:list
    paths:list[str,]
    mods_data:dict = {}
    def __init__(self):
        print('Setup Mods Loader...')
        self.mods = []
        self.paths = []
        self.load_mods()
        self.create_paths()

    def number_of_mods(self) -> int:
        return int(len(self.mods_data.keys())/2)

    def import_mods(self, game_engine: pygameengine.PyGameEngine, game_object:object):
        """
        Import Mods
        Will be imported a _import object and the mod itself
        """
        # Try Import Mods
        for mod_metadata, mod_path_os in self.mods:
            try:
                mod_fixed_name = mod_metadata['Mod_Name'].replace(' ','_')
                mod_path = (mod_path_os.replace('/','.').replace('\\','.').replace('.py',''))[2:] # Get Mod_Path and remove all / and \ and .py
                if mod_metadata['Mod_RCode'] != 1:
                    self.mods_data[mod_fixed_name+'_import'] =importlib.import_module(mod_path)
                    self.mods_data[mod_fixed_name] = self.mods_data[mod_fixed_name+'_import'].Mod(game_engine=game_engine,game_object=game_object)
            except Exception as e:
                print(f'Error importing {mod_metadata["Mod_Name"]}: {e}')
        
        print('Mods Imported!')

    def draw_mods(self, game_engine: pygameengine.PyGameEngine, game_object:object, **kwargs):
        """
        Independent Mod Page Handler
        """
        for mod_key in self.mods_data.keys():
            if mod_key.endswith('_import'):
                pass
            else:
                self._indiv_mod_page_handler(game_engine=game_engine, game_object=game_object, mod_key=mod_key, kwargs=kwargs)
    
    def _indiv_mod_page_handler(self, game_engine: pygameengine.PyGameEngine, game_object:object, mod_key, kwargs):
        """
        Individual Mod Page Handler
        
        → it will get all mods and load invidiualy mod page handler if not ends with "_import"
        → Will run with threading for make less impact into Performance of the game
        """
        if mod_key.endswith('_import'):
            pass
        else:
            if str(mod_key).replace("_"," ").replace('/','') in game_object.mods_enabled:
                mod = self.mods_data[mod_key]
                threading.Thread(target=mod.screen_handler,name=f'PixelDungeon2-{str(mod_key).replace(" ","-").replace('/','')}', args=(game_engine, game_object, kwargs)).start()

    def load_mods(self):
        for file in os.listdir('./data/mods/'):
            if os.path.isfile(f'./data/mods/{file}'):
                x = file.split('.')
                if x[-1] in _ACCEPTABLE_FILES and x[0] != __name__.split('.')[-1]:
                    self.paths.append(f'./data/mods/{file}')
                    
        self.check_integrity()
    
    def _check_integrity(self, path:str) -> tuple[bool, dict]:
        integrity = True
        x = path.split('.')
        if x[-1] in _ACCEPTABLE_FILES and x[0] != __name__.split('.')[-1]:
            read1 = open(path, 'rb')
            read_lines:list[bytes,] = []
            for line in read1.readlines():
                if not (line in ['',' ','#',None] or (line.startswith(b'#'))):
                    read_lines.append(line)
            
            Metadata = {
                'Mod_Name':'',
                'Mod_Author':'',
                'Mod_Version':'',
                'Mod_Description':'',
                'Has_Mod_Class':False,
                'Mod_RCode':0
            }
            
            # Get Metadata
            for line in read_lines:
                if line.startswith(b'MTD_Mod_Name:'):
                    Metadata['Mod_Name'] = line.split(b':')[-1].strip().decode('utf-8')
                elif line.startswith(b'MTD_Mod_Author:'):
                    Metadata['Mod_Author'] = line.split(b':')[-1].strip().decode('utf-8')
                elif line.startswith(b'MTD_Mod_Version:'):
                    Metadata['Mod_Version'] = line.split(b':')[-1].strip().decode('utf-8')
                elif line.startswith(b'MTD_Mod_Description:'):
                    Metadata['Mod_Description'] = line.split(b':')[-1].strip().decode('utf-8')
                elif line.startswith(b'MTD_Mod_RCode:'):
                    Metadata['Mod_RCode'] = int(line.split(b':')[-1].strip().decode('utf-8'))
                
            # Get Mod Class
            try:
                p = [b.decode() for b in read_lines]
                Has_Mod_Class = False
                for line in p:
                    if line.startswith('class Mod:') or line.startswith('class Mod():'):
                        Has_Mod_Class = True
                
                Metadata['Has_Mod_Class'] = Has_Mod_Class
            except Exception as e:
                print(f'Error loading Mod: {path}, Error: {e}')
                Metadata['Has_Mod_Class'] = False
            
            for key in Metadata.keys():
                if key in ['Mod_RCode']: # This will be ignored
                    pass
                else:
                    if Metadata[key] in [' ','',None,False]:        
                        integrity = False
            
            if integrity:
                return True, Metadata
            else:
                return False, Metadata
            
        return False, None        
    
    def check_integrity(self):
        for path in self.paths.copy():
            sucess, metadata = self._check_integrity(path)
            if not sucess:
                print(f'Invalid Mod: {path}, Metadata: {metadata}')
            else:
                self.mods.append([metadata, path])
                
    def create_paths(self):
        if not os.path.exists('./data/mods/mods_files'):
            os.mkdir('./data/mods/mods_files')
        for mod in self.mods:
            mod_name:str = mod[0]['Mod_Name']
            mod_name = mod_name.replace(' ','')
            if not os.path.exists('./data/mods/mods_files/' + mod_name):
                if not os.path.isdir('./data/mods/mods_files/' + mod_name):
                    os.mkdir('./data/mods/mods_files/' + mod_name)
                else:
                    print(f'non Folder file exists: ./data/mods/mods_files/{mod_name}')
                    
    def remove_mod(self, mod_name:str):
        mod_path = ''
        for mod in self.mods:
            if mod[0]['Mod_Name'] == mod_name:
                self.mods.remove(mod)
                mod_path = mod[1]
                break
            
        for path in self.paths:
            if path == mod_path:
                self.paths.remove(path)
                break
            
        for data in self.mods_data.keys():
            if data == mod_name:
                self.mods_data.pop(data)
                break
            
        if os.path.exists(mod_path):
            os.remove(mod_path)

        fmod_name = mod_name.replace(' ','')
        if os.path.exists('./data/mods/mods_files/' + fmod_name):
            shutil.rmtree(f'./data/mods/mods_files/{fmod_name}')
        print(f'Removed mod: {mod_path}')