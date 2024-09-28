

"""
Config File
"""


# MetaData
GAME_TITLE = 'Pixel Dungeon 2'
GAME_VERSION = '1.0.3'

"""
Screen Ids:
Main Menu: 0
Save Select: 1
Options: 2
Mods: 3
In Game: 4
Confirm Exit: 5
Create Save: 6
"""
GAME_SCREEN = 0 # Ids will be used for mods

SCREEN_SIZE_OPTIONS = [
    (640, 480),
    (800, 600),
    (1024, 768),
    (1280, 1024),
    (1600, 1200),
    (1920, 1440),
]
FPS_OPTIONS = [
    30,
    60,
    90,
    120,
    140,
]
RenderDistance_OPTIONS = [
    512,
    1024,    # Px (W x H)
    2048,
    4096,
    8192,
]

DEFAULT_CONFIG_JSON = {
    'volume':0.5,
    'fullscreen':False,
    'screen_size':1,
    'show_fps':False,
    'discord_rpc':False,
    'fullscreen':False,
    'fps':1,
    'dynamic_fps':True,
    'enable_mods':[],
    'smooth_scroll':True,
    'RenderDistance':3
}
CONFIG:dict = DEFAULT_CONFIG_JSON

# Configs:

import pygameengine as pyge
from JPyDB import pyDatabase
from ..mods.mods import Mods as ModsClass
import os, random, math, sys, base64, pickle, shutil


# Game Object
class GameObj:
    screen_id:int
    version = GAME_VERSION
    title = GAME_TITLE
    threading_running:bool = False
    mods_enabled:list[str,] = []
    pid:int = 0
    pyDatabase:pyDatabase
    ratio:float = 1.0
    config:dict

GameObject = GameObj()

pg = pyge.pg

pge = pyge.PyGameEngine()

TILE_SIZE:int = 32

# Database
pdb = pyDatabase('/data/savedata')
db = pdb.database

GameObject.pyDatabase = pdb

# Load Config
if 'cfg' in db.tables.keys():
    CONFIG:dict = db.get_value('cfg', 'data', 0)
    for key in DEFAULT_CONFIG_JSON.keys():
        if not (key in CONFIG.keys()): # Fix for old configs
            CONFIG[key] = DEFAULT_CONFIG_JSON[key]
    GameObject.mods_enabled = CONFIG['enable_mods']
    GameObject.config = CONFIG
else:
    db.create_table('cfg', [('data',dict)])
    db.add_value('cfg', 'data', 0, DEFAULT_CONFIG_JSON)
    CONFIG:dict = DEFAULT_CONFIG_JSON
    GameObject.config = CONFIG

if not ('saves' in db.tables.keys()):
    db.create_table('saves', [('data',bytes)])

# Fix Config
if CONFIG['fps'] > len(FPS_OPTIONS)-1: CONFIG['fps'] = DEFAULT_CONFIG_JSON['fps']
if CONFIG['screen_size'] > len(SCREEN_SIZE_OPTIONS)-1: CONFIG['screen_size'] = DEFAULT_CONFIG_JSON['screen_size']

db.update_value('cfg', 'data', 0, CONFIG)
db.save()

# Default Screen Size
DEFAULT_SCREEN_SIZE = SCREEN_SIZE_OPTIONS[1]
CURRENT_SCREEN_SIZE = SCREEN_SIZE_OPTIONS[CONFIG['screen_size']]
RATIO = (CURRENT_SCREEN_SIZE[0]/DEFAULT_SCREEN_SIZE[0] + CURRENT_SCREEN_SIZE[1]/DEFAULT_SCREEN_SIZE[1]) / 2

GameObject.ratio = RATIO

# Paths
ROOT_PATH = os.path.abspath('.')
DATA_PATH = os.path.join(ROOT_PATH, 'data')
ASSETS_PATH = os.path.join(DATA_PATH, 'assets')
FONTS_PATH = os.path.join(ASSETS_PATH, 'fonts')
SOUNDS_PATH = os.path.join(ASSETS_PATH, 'sounds')
TEXTURES_PATH = os.path.join(ASSETS_PATH, 'textures')

GlitchGoblinFont = os.path.join(FONTS_PATH, 'GlitchGoblin.ttf')
PublicPixelFont = os.path.join(FONTS_PATH, 'PublicPixel.ttf')

# Screen Creation
screen = pge.createScreen(*CURRENT_SCREEN_SIZE, pg.SCALED|pg.FULLSCREEN if CONFIG['fullscreen'] else pg.SCALED)
pge.setScreenTitle(f'{GAME_TITLE}')
pge.setFPS(FPS_OPTIONS[CONFIG['fps']])

# Mod Loading
mods = ModsClass()

# Fonts
# GGF = GlitchGoblin Font
# PPF = Public Pixel Font
GGF56 = pge.createFont(GlitchGoblinFont, int(56*RATIO)) # 0
GGF54 = pge.createFont(GlitchGoblinFont, int(54*RATIO)) # 1
GGF34 = pge.createFont(GlitchGoblinFont, int(34*RATIO)) # 2
GGF32 = pge.createFont(GlitchGoblinFont, int(32*RATIO)) # 3

PPF28 = pge.createFont(PublicPixelFont, int(28*RATIO)) # 4
PPF26 = pge.createFont(PublicPixelFont, int(26*RATIO)) # 5
PPF24 = pge.createFont(PublicPixelFont, int(24*RATIO)) # 6
PPF20 = pge.createFont(PublicPixelFont, int(20*RATIO)) # 7
PPF18 = pge.createFont(PublicPixelFont, int(18*RATIO)) # 8
PPF16 = pge.createFont(PublicPixelFont, int(16*RATIO)) # 9
PPF14 = pge.createFont(PublicPixelFont, int(14*RATIO)) # 10
PPF12 = pge.createFont(PublicPixelFont, int(12*RATIO)) # 11
PPF10 = pge.createFont(PublicPixelFont, int(10*RATIO)) # 12
PPF8  = pge.createFont(PublicPixelFont, int(8*RATIO))  # 13

GGF30 = pge.createFont(GlitchGoblinFont, int(30*RATIO)) # 14
GGF28 = pge.createFont(GlitchGoblinFont, int(28*RATIO)) # 15
GGF26 = pge.createFont(GlitchGoblinFont, int(26*RATIO)) # 16
GGF24 = pge.createFont(GlitchGoblinFont, int(24*RATIO)) # 17
GGF22 = pge.createFont(GlitchGoblinFont, int(22*RATIO)) # 18
GGF20 = pge.createFont(GlitchGoblinFont, int(20*RATIO)) # 19
GGF18 = pge.createFont(GlitchGoblinFont, int(18*RATIO)) # 20
GGF16 = pge.createFont(GlitchGoblinFont, int(16*RATIO)) # 21
GGF14 = pge.createFont(GlitchGoblinFont, int(14*RATIO)) # 22
GGF12 = pge.createFont(GlitchGoblinFont, int(12*RATIO)) # 23
GGF10 = pge.createFont(GlitchGoblinFont, int(10*RATIO)) # 24
GGF8 = pge.createFont(GlitchGoblinFont, int(8*RATIO)) # 25

# Sprites
TILES_SPRITESHEET = pge.createSpritesheet(TEXTURES_PATH+'/tiles.png')

# Colors
P_DARKGRAY = pyge.reqColor(30,30,30)
P_PEAR = pyge.reqColor(117, 255, 142)
P_LIGHTBLUE = pyge.reqColor(140, 197, 255)
P_LIGHTRED = pyge.reqColor(255, 140, 140)
P_LIGHTGREEN = pyge.reqColor(140, 255, 140)
P_YELLOW = pyge.reqColor(254, 226, 2)

# Misc
def ShowFPS():
    if CONFIG['show_fps']: # Draw on TopRight of screen
        f = int(pge.getFPS())
        c = pge.Colors.WHITE
        mfps = FPS_OPTIONS[CONFIG['fps']]
        if f >= mfps*0.8:
            c = pge.Colors.GREEN
        elif f >= mfps*0.55:
            c = P_LIGHTGREEN
        elif f >= mfps*0.4:
            c = pge.Colors.YELLOW
        elif f >= mfps*0.25:
            c = pge.Colors.ORANGE
        elif f >= mfps*0.1:
            c = pge.Colors.RED
        text = f'FPS: {f}'
        pge.draw_text((CURRENT_SCREEN_SIZE[0]-PPF10.size(text)[0], 5), text, PPF10, c)
        
def split_lines(text, font, max_width) -> list[str,]:
    """
    Split lines when it haves more than max_width
    
    Uses font size to calculate.
    """
    lines = []
    cur_width = 0
    line = ''
    for x,word in enumerate(text.split(' ')):
        if cur_width + font.size(word)[0] > max_width:
            lines.append(line)
            line = word + ' '
            cur_width = 0
        else:
            if x == len(text.split(' '))-1:
                line += word + ' '
                lines.append(line)
            else:
                line += word + ' '
                cur_width += font.size(word)[0]
    
    return lines

# Some Configs for the in Game
elements = [
        'fire',
        'air',
        'water',
        'earth',
        'light',
        'dark',
        'thunder',
        'ice',
]
difficulties = [
    'easy',
    'medium',
    'hard',
    'extreme'
]
colors = {
    'difficulty':{
        '0':P_PEAR,
        '1':pge.Colors.GREEN,
        '2':pge.Colors.YELLOW,
        '3':pge.Colors.RED
    },
    'element':{
        '0':pge.Colors.RED,
        '1':pge.Colors.LIGHTGRAY,
        '2':pge.Colors.BLUE,
        '3':pge.Colors.BROWN,
        '4':pge.Colors.YELLOW,
        '5':pge.Colors.DARKPURPLE,
        '6':pge.Colors.LIGHTBLUE,
        '7':pge.Colors.GAINSBORO
    }
}

# Widgets for the Screen
class Menu:
    def __init__(self):
        pge.limit_error_active = False # Disable limit error
        self.run_built()
        
    def run_built(self):
        # Exit Screen Buttons
        self.ExitMenu_ConfirmButton = pyge.Button(pge, (50*RATIO, 130*RATIO), PPF16, 'Confirm (Y)', [P_LIGHTRED, P_DARKGRAY, pge.Colors.BLACK])
        self.ExitMenu_CancelButton = pyge.Button(pge, (400*RATIO, 130*RATIO), PPF16, 'Cancel (N)', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
        
        # Main Menu Buttons
        self.MainMenu_PlayButton = pyge.Button(pge, (25*RATIO, 100*RATIO), PPF26, 'PLAY', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
        self.MainMenu_OptionsButton = pyge.Button(pge, (25*RATIO, 138*RATIO), PPF26, 'OPTIONS', [P_LIGHTBLUE, P_DARKGRAY, pge.Colors.BLACK])
        self.MainMenu_ModsButton = pyge.Button(pge, (25*RATIO, 176*RATIO), PPF26, 'MODS', [P_YELLOW, P_DARKGRAY, pge.Colors.BLACK])
        self.MainMenu_ExitButton = pyge.Button(pge, (25*RATIO, 214*RATIO), PPF26, 'EXIT', [P_LIGHTRED, P_DARKGRAY, pge.Colors.BLACK])
        
        # Options Menu Buttons
        self.OptionsMenu_VolumeSlider = pyge.Slider(pge, (20*RATIO, 100*RATIO), (740*RATIO,30*RATIO), [P_PEAR, P_DARKGRAY, P_DARKGRAY],value=CONFIG['volume'], fill_passed=True)
        self.OptionsMenu_ScreenSizeDropdown = pyge.Dropdown(pge, (250*RATIO, 140*RATIO), [pge.Colors.WHITE, pge.Colors.BLACK, P_DARKGRAY], [f'{c[0]}x{c[1]}' for c in SCREEN_SIZE_OPTIONS], PPF14, current_text=CONFIG['screen_size'], tip=('Screen Size, using the size of your monitor with Fullscreen ON will make it gives a quality gain.',PPF10))
        self.OptionsMenu_FPSSelect =pyge.Select(pge, (130*RATIO, 180*RATIO),PPF14, [pge.Colors.WHITE, pge.Colors.BLACK, P_DARKGRAY], [f'{c}' for c in FPS_OPTIONS], CONFIG['fps'], False, tip=('Sets the limit that the game will run of FPS.',PPF10))
        self.OptionsMenu_FullscreenCheckbox = pyge.Checkbox(pge, (20*RATIO, 220*RATIO), PPF14, 'Fullscreen', [pge.Colors.WHITE, P_LIGHTRED, P_LIGHTGREEN, P_DARKGRAY],tip=('Enables fullscreen mode.',PPF10))
        self.OptionsMenu_FPSCheckbox = pyge.Checkbox(pge, (20*RATIO, 260*RATIO), PPF14, 'Show FPS', [pge.Colors.WHITE, P_LIGHTRED, P_LIGHTGREEN, P_DARKGRAY],tip=('Shows FPS counter.',PPF10))
        self.OptionsMenu_DynamicFPSCheckbox = pyge.Checkbox(pge, (20*RATIO, 300*RATIO), PPF14, 'Dynamic FPS', [pge.Colors.WHITE, P_LIGHTRED, P_LIGHTGREEN, P_DARKGRAY],tip=('Will make the Time system work better with FPS floating.',PPF10))
        self.OptionsMenu_RenderDistanceDropdown = pyge.Dropdown(pge, (300*RATIO, 380*RATIO), [pge.Colors.WHITE, pge.Colors.BLACK, P_DARKGRAY], [f'{c}' for c in RenderDistance_OPTIONS], PPF14, current_text=CONFIG['RenderDistance'], tip=('Render Distance in pixels.',PPF10))
        self.OptionsMenu_BackButton = pyge.Button(pge, (5*RATIO, 5*RATIO), PPF12, '< BACK', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
        self.OptionsMenu_SmoothMouseScrollCheckbox = pyge.Checkbox(pge, (20*RATIO, 340*RATIO), PPF14, 'Smooth Mouse Scroll', [pge.Colors.WHITE, P_LIGHTRED, P_LIGHTGREEN, P_DARKGRAY],tip=('Enables smooth mouse scrolling.',PPF10))
        
        # Game Select Menu Buttons
        self.GameSelectMenu_BackButton = pyge.Button(pge, (5*RATIO, 5*RATIO), PPF12, '< BACK', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
        self.GameSelectMenu_CreateSaveButton = pyge.Button(pge, (10*RATIO, 550*RATIO), PPF20, 'CREATE SAVE', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
        self.GameSelectMenu_LoadSaveButton = pyge.Button(pge, (600*RATIO, 550*RATIO), PPF20, 'LOAD SAVE', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
        self.GameSelectMenu_ConfirmDeleteButton = pyge.Button(pge, (40*RATIO, 350*RATIO), PPF20, 'CONFIRM(y)', [P_LIGHTRED, P_DARKGRAY, pge.Colors.BLACK])
        self.GameSelectMenu_CancelDeleteButton = pyge.Button(pge, (250*RATIO, 350*RATIO), PPF20, 'CANCEL(n)', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
        
        # Create Save Menu Buttons
        self.CreateSaveMenu_DifficultiesSelect = pyge.Select(pge, (40*RATIO, 210*RATIO), PPF16, [P_PEAR, P_DARKGRAY, pge.Colors.BLACK], difficulties, 1, True)
        self.CreateSaveMenu_ElementsDropdown = pyge.Dropdown(pge, (40*RATIO,290*RATIO), [P_PEAR, P_DARKGRAY, pge.Colors.BLACK], elements, PPF16, current_text=random.randint(0, len(elements)-1), tip=('The starting element set for the game.',PPF10))
        self.CreateSaveMenu_NameTextbox = pyge.Textbox(pge, (40*RATIO, 130*RATIO), 20, [pge.Colors.DARKGRAY, pge.Colors.DARKGREEN, pge.Colors.WHITE, pge.Colors.WHITE], PPF16, '')
        self.CreateSaveMenu_SaveButton = pyge.Button(pge, (40*RATIO, 370*RATIO), PPF20, 'SAVE', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
        self.CreateSaveMenu_CancelButton = pyge.Button(pge, (300*RATIO, 370*RATIO), PPF20, 'CANCEL', [P_LIGHTRED, P_DARKGRAY, pge.Colors.BLACK])
        
        # In Game Menu Buttons
        self.InGame_ResumeButton = pyge.Button(pge, (15*RATIO, 55*RATIO), PPF12, 'RESUME', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
        self.InGame_SaveButton = pyge.Button(pge, (15*RATIO, 95*RATIO), PPF12, 'SAVE', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
        self.InGame_QuitButton = pyge.Button(pge, (15*RATIO, 135*RATIO), PPF12, 'QUIT', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
        self.InGame_QuitToDesktopButton = pyge.Button(pge, (15*RATIO, 175*RATIO), PPF12, 'QUIT TO DESKTOP', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
        
        # Mods
        self.ModsMenu_BackButton = pyge.Button(pge, (5*RATIO, 5*RATIO), PPF12, '< BACK', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
        self.ModsMenu_LongText = pyge.Longtext(pge, (0, (DEFAULT_SCREEN_SIZE[1]-100)*RATIO), PPF14, f'A Total of: {mods.number_of_mods()} mods loaded!\nPlease be careful about the mods you use, mods can be used for scam peoples, and then, steal information.', [pge.Colors.WHITE, P_DARKGRAY, pge.Colors.BROWN])
        self.ModsMenu_LongText2 = pyge.Longtext(pge, (20*RATIO, 550*RATIO), PPF14,  '! Be careful about the mods you use, mods can be used for scam peoples, and then, steal information. More Mods = Minus Perfomance.', [pge.Colors.WHITE, pge.Colors.BLACK, pge.Colors.BLACK])
        
# Tiles
tiles_ids:dict = {
    '0':'Sand',
    '1':'Rock',
    '2':'Dirt',
    '3':'Grass',
    '4':'Snow',
    '5':'Water',
    '6':'Red_Brick',
    '7':'Green_Brick',
    '8':'Blue_Brick',
    '9':'Yellow_Brick',
    '10':'Purple_Brick',
    '11':'Door',
    '':'air',
    '-1':'Barrier'
}
        
GameMenu = Menu()