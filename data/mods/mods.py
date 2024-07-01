import os, sys, importlib

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
        print(f'{len(self.mods)} Mods Loaded!')

    def import_mods(self):
        # Try Import Mods
        print('Importing Mods...')
        for mod_metadata, mod_path_os in self.mods:
            try:
                mod_fixed_name = mod_metadata['Mod_Name'].replace(' ','_')
                mod_path = (mod_path_os.replace('/','.').replace('\\','.').replace('.py',''))[2:] # Get Mod_Path and remove all / and \ and .py
                self.mods_data[mod_fixed_name+'_import'] =importlib.import_module(mod_path)
                self.mods_data[mod_fixed_name] = self.mods_data[mod_fixed_name+'_import'].Mod()
            except Exception as e:
                print(f'Error importing {mod_metadata["Mod_Name"]}: {e}')
        
        print('Mods Imported!')

    def load_mods(self):
        print('Loading Mods...')
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
                'Has_Mod_Class':False
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
                if Metadata[key] in [' ','',None,False]:        
                    integrity = False
            
            if integrity:
                return True, Metadata
            else:
                return False, Metadata
            
        return False, None        
    
    def check_integrity(self):
        print('Checking Mod Integrity...')
        for path in self.paths.copy():
            sucess, metadata = self._check_integrity(path)
            if not sucess:
                print(f'Invalid Mod: {path}, Metadata: {metadata}')
            else:
                self.mods.append([metadata, path])