from data.src import constant
from .ingame import *
from .config import *

def modsscreen(game_state):
    """
    Mods screen
    """
    run = True
    Back_Button = pyge.Button(pge, (5*RATIO, 5*RATIO), PPF12, '< BACK', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    
    Warn_LongText = pyge.Longtext(pge, (0, (DEFAULT_SCREEN_SIZE[1]-100)*RATIO), PPF14, f'A Total of: {mods.number_of_mods()} mods loaded!\nPlease be careful about the mods you use, mods can be used for scam peoples, and then, steal information.', [pge.Colors.WHITE, P_DARKGRAY, pge.Colors.BROWN])
    Warn_LongText2 = pyge.Longtext(pge, (20*RATIO, 550*RATIO), PPF14,  '! Be careful about the mods you use, mods can be used for scam peoples, and then, steal information. More Mods = Minus Perfomance.', [pge.Colors.WHITE, pge.Colors.BLACK, pge.Colors.BLACK])
    
    mods_widgets = [Back_Button, Warn_LongText, Warn_LongText2]
    
    buttons = []
    buttons_ids = []        

    GAME_SCREEN = constant.Menu.MODS_SCREEN
    GameObject.screen_id = GAME_SCREEN

    pge.fill(pge.Colors.BLACK)                        
    # Screen Title + Shadow
    pge.draw_text((13*RATIO,15*RATIO),'Mods', GGF32, pge.Colors.DARKGRAY)
    pge.draw_text((15*RATIO,15*RATIO), 'Mods', GGF34, pge.Colors.WHITE)

    nx,ny = 0,30
    for mod in mods.mods:
        r = pge.draw_rect(((nx+30)*RATIO,(ny+30)*RATIO), (256*RATIO,128*RATIO), P_DARKGRAY, 3,pge.Colors.DARKBROWN) # Background
        pge.draw_text(((nx+40)*RATIO,(ny+40)*RATIO), mod[0]['Mod_Name'][:18], PPF14, pge.Colors.WHITE) # Mod Name
        pge.draw_text(((nx+35)*RATIO,(ny+55)*RATIO), str(mod[1])[:24], PPF10, pge.Colors.GRAY) # Mod Path
        pge.draw_text(((nx+35)*RATIO,(ny+70)*RATIO),mod[0]['Mod_Author'][:24], PPF12, pge.Colors.WHITE) # Mod Author
        pge.draw_text(((nx+35)*RATIO,(ny+85)*RATIO), mod[0]['Mod_Version'][:24], PPF12, pge.Colors.WHITE) # Mod Version
        pge.draw_text(((nx+190)*RATIO,(ny+70)*RATIO),"Enabled" if mod[0]["Mod_Name"] in CONFIG['enable_mods'] else "Disabled", PPF10, P_PEAR if mod[0]['Mod_Name'] in CONFIG['enable_mods'] else P_LIGHTRED)
        
        button_id_select = f'{mod[0]["Mod_Name"]}select_button'
        button_id_delete = f'{mod[0]["Mod_Name"]}delete_button'
        
        
        if ((button_id_select not in buttons_ids) or (button_id_delete not in buttons_ids)):
            if not ((pge.findWidgetById(button_id_select) and pge.findWidgetById(button_id_delete))):
                select_btn = pyge.Button(pge, ((nx+40)*RATIO, (ny+142)*RATIO), PPF14, 'SELECT', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK],id=button_id_select)
                delete_btn = pyge.Button(pge, ((nx+190)*RATIO, (ny+142)*RATIO), PPF14, 'DELETE', [pge.Colors.RED, P_DARKGRAY, pge.Colors.BLACK],id=button_id_delete,tip=('Delete Mod will remove from local storage.',PPF10))
                select_btn.click_time = 0.3
                delete_btn.click_time = 0.3
                buttons.append([select_btn, delete_btn])
                buttons_ids.append(button_id_select)
                buttons_ids.append(button_id_delete)
                mods_widgets.append(select_btn)
                mods_widgets.append(delete_btn)
            else:
                select_btn = pge.findWidgetById(button_id_select)
                delete_btn = pge.findWidgetById(button_id_delete)
                buttons.append([select_btn, delete_btn])
                buttons_ids.append(button_id_select)
                buttons_ids.append(button_id_delete)
                mods_widgets.append(select_btn)
                mods_widgets.append(delete_btn)
        
        # Description
        texts = split_lines(mod[0]['Mod_Description'][:64], PPF12, 128*RATIO)
        pos = [nx+30, (ny+105)*RATIO]
        for line in texts:
            pge.draw_text(pos, line, PPF10, pge.Colors.WHITE)
            pos[1] += PPF10.size(line)[1]
            
    for mods_buttons in buttons:
        select:pyge.Button = mods_buttons[0]
        delete:pyge.Button = mods_buttons[1]
        mod_name = str(select._id).replace('select_button','')
        if select.value:
            if mod_name not in CONFIG['enable_mods']:
                CONFIG['enable_mods'].append(mod_name)
                GameObject.mods_enabled = CONFIG['enable_mods']
            elif mod_name in CONFIG['enable_mods']:
                CONFIG['enable_mods'].remove(mod_name)
                GameObject.mods_enabled = CONFIG['enable_mods']
        
        nx += r.width + 5
        if nx > CURRENT_SCREEN_SIZE[0]-60:
            nx = 0
            ny += r.height   
                   
    #@TODO: HACK
    for widget in mods_widgets:
        widget.build_widget_display() 
    pge.draw_widgets(mods_widgets)    
    mods.draw_mods(pge, GameObject)

    ShowFPS()    

    if Back_Button.value:  
        db.update_value('cfg', 'data',0, CONFIG)
        game_state.Mods_Button.value = False
        game_state.mode = constant.Menu.MAIN

def options(game_state):
    """
    Options Screen
    """          
    options_widgets = [
        game_state.Back_Button,
        game_state.Volume_Slider,
        game_state.Screen_size_select,
        game_state.FPS_select,
        game_state.Fullscreen_checkbox,
        game_state.ShowFPS_checkbox,
        game_state.FPSDynamic_checkbox,
        game_state.RenderDistance_select,
    ]
    
    key = game_state.input_state.key        
    if key[constant.Key.F1].is_down:
        pdb.get_content()
    
    GameObject.config = CONFIG            

    GAME_SCREEN = constant.Menu.OPTIONS
    GameObject.screen_id = GAME_SCREEN
    if game_state.Back_Button.value: 
        game_state.Options_Button.value = False
        game_state.mode = constant.Menu.MAIN
        # Update Config
        CONFIG['volume'] = round(game_state.Volume_Slider.value,2)
        CONFIG['screen_size'] = game_state.Screen_size_select.value
        CONFIG['fps'] = game_state.FPS_select.value
        CONFIG['show_fps'] = game_state.ShowFPS_checkbox.value
        CONFIG['fullscreen'] = game_state.Fullscreen_checkbox.value
        CONFIG['dynamic_fps'] = game_state.FPSDynamic_checkbox.value
        CONFIG['RenderDistance'] = game_state.RenderDistance_select.value
        pge.setFPS(FPS_OPTIONS[CONFIG['fps']])
        db.update_value('cfg', 'data', 0, CONFIG)
        db.save()   

    pge.fill(pge.Colors.BLACK)
        
    # Screen Title + Shadow
    pge.draw_text((13*RATIO,15*RATIO),'Options', GGF32, pge.Colors.DARKGRAY)
    pge.draw_text((15*RATIO,15*RATIO), 'Options', GGF34, pge.Colors.WHITE)
    
    # Texts
    pge.draw_text((15*RATIO,70*RATIO), f'Volume: {int(game_state.Volume_Slider.value*100)}%', PPF16, pge.Colors.WHITE)
    pge.draw_text((20*RATIO,140*RATIO), f'Screen Size: ', PPF16, pge.Colors.WHITE)
    pge.draw_text((20*RATIO,180*RATIO), f'FPS:', PPF16, pge.Colors.WHITE)
    pge.draw_text((20*RATIO, 340*RATIO), f'Render Distance:', PPF16, pge.Colors.WHITE)    
    
    #@TODO: HACK
    for widget in options_widgets:
        if widget == None:
            widget.build_widget_display() 
    pge.draw_widgets(options_widgets)
    mods.draw_mods(pge,GameObject)                 
    
    if CONFIG['show_fps']:
        ShowFPS()
        