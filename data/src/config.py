

"""
Config File
"""


# MetaData
GAME_TITLE = 'Pixel Dungeon 2'
GAME_VERSION = '1.0.0'

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
    144,
    240
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
    'enable_mods':[]
}
CONFIG:dict = DEFAULT_CONFIG_JSON

# Configs:

import pygameengine as pyge
from JPyDB import pyDatabase
from ..mods.mods import Mods as ModsClass
import os, random, math, sys, base64, pickle

pg = pyge.pg

pge = pyge.PyGameEngine()

# Database
pdb = pyDatabase('/data/savedata')
db = pdb.database

# Load Config
if 'cfg' in db.tables.keys():
    CONFIG:dict = db.get_value('cfg', 'data', 0)
    for key in DEFAULT_CONFIG_JSON.keys():
        if not (key in CONFIG.keys()): # Fix for old configs
            CONFIG[key] = DEFAULT_CONFIG_JSON[key]
else:
    db.create_table('cfg', [('data',dict)])
    db.add_value('cfg', 'data', 0, DEFAULT_CONFIG_JSON)
    CONFIG:dict = DEFAULT_CONFIG_JSON

if not ('saves' in db.tables.keys()):
    db.create_table('saves', [('data',bytes)])

# Default Screen Size
DEFAULT_SCREEN_SIZE = SCREEN_SIZE_OPTIONS[1]
CURRENT_SCREEN_SIZE = SCREEN_SIZE_OPTIONS[CONFIG['screen_size']]
RATIO = (CURRENT_SCREEN_SIZE[0]/DEFAULT_SCREEN_SIZE[0] + CURRENT_SCREEN_SIZE[1]/DEFAULT_SCREEN_SIZE[1]) / 2

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
GGF56 = pge.createFont(GlitchGoblinFont, int(56*RATIO))
GGF54 = pge.createFont(GlitchGoblinFont, int(54*RATIO))
GGF34 = pge.createFont(GlitchGoblinFont, int(34*RATIO))
GGF32 = pge.createFont(GlitchGoblinFont, int(32*RATIO))

PPF28 = pge.createFont(PublicPixelFont, int(28*RATIO))
PPF26 = pge.createFont(PublicPixelFont, int(26*RATIO))
PPF24 = pge.createFont(PublicPixelFont, int(24*RATIO))
PPF20 = pge.createFont(PublicPixelFont, int(20*RATIO))
PPF18 = pge.createFont(PublicPixelFont, int(18*RATIO))
PPF16 = pge.createFont(PublicPixelFont, int(16*RATIO))
PPF14 = pge.createFont(PublicPixelFont, int(14*RATIO))
PPF12 = pge.createFont(PublicPixelFont, int(12*RATIO))
PPF10 = pge.createFont(PublicPixelFont, int(10*RATIO))
PPF8  = pge.createFont(PublicPixelFont, int(8*RATIO))

# Colors
P_DARKGRAY = pyge.reqColor(30,30,30)
P_PEAR = pyge.reqColor(117, 255, 142)
P_LIGHTBLUE = pyge.reqColor(140, 197, 255)
P_LIGHTRED = pyge.reqColor(255, 140, 140)
P_LIGHTGREEN = pyge.reqColor(140, 255, 140)

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