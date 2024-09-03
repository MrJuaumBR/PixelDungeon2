from .ingame import *
from .config import *

def modsscreen():
    """
    Mods screen
    """
    run = True
    Back_Button = GameMenu.ModsMenu_BackButton
    
    Warn_LongText = GameMenu.ModsMenu_LongText
    Warn_LongText2 = GameMenu.ModsMenu_LongText2
    
    mods_widgets = [Back_Button, Warn_LongText, Warn_LongText2]
    
    buttons = []
    buttons_ids = []
    
    y_shift = 0
    
    while run:        
        GAME_SCREEN = 3
        GameObject.screen_id = GAME_SCREEN
        if Back_Button.value: run = False
        
        y_shift += pge.mouse.scroll * 10
        
        nx,ny = 5,30 + y_shift *RATIO
        for mod in mods.mods:
            r = pge.draw_rect(((nx)*RATIO,(ny+30)*RATIO), (240*RATIO,128*RATIO), P_DARKGRAY, 3,pge.Colors.DARKBROWN) # Background
            pge.draw_text(((nx+15)*RATIO,(ny+40)*RATIO), mod[0]['Mod_Name'][:18], PPF14, pge.Colors.WHITE) # Mod Name
            pge.draw_text(((nx+25)*RATIO,(ny+55)*RATIO), str(mod[1])[:24], PPF10, pge.Colors.GRAY) # Mod Path
            pge.draw_text(((nx+15)*RATIO,(ny+70)*RATIO),mod[0]['Mod_Author'][:24], PPF12, pge.Colors.WHITE) # Mod Author
            pge.draw_text(((nx+15)*RATIO,(ny+85)*RATIO), mod[0]['Mod_Version'][:24], PPF12, pge.Colors.WHITE) # Mod Version
            pge.draw_text(((nx+120)*RATIO,(ny+70)*RATIO),"Enabled" if mod[0]["Mod_Name"] in CONFIG['enable_mods'] else "Disabled", PPF10, P_PEAR if mod[0]['Mod_Name'] in CONFIG['enable_mods'] else P_LIGHTRED)
            
            button_id_select = f'{mod[0]["Mod_Name"]}select_button'
            button_id_delete = f'{mod[0]["Mod_Name"]}delete_button'
            
            
            if ((button_id_select not in buttons_ids) or (button_id_delete not in buttons_ids)): # Button isn't in buttons id
                if not ((pge.findWidgetById(button_id_select) and pge.findWidgetById(button_id_delete))):
                    select_btn = pyge.Button(pge, ((nx+10)*RATIO, (ny+142)*RATIO), PPF14, 'SELECT', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK],id=button_id_select)
                    delete_btn = pyge.Button(pge, ((nx+135)*RATIO, (ny+142)*RATIO), PPF14, 'DELETE', [pge.Colors.RED, P_DARKGRAY, pge.Colors.BLACK],id=button_id_delete,tip=('Delete Mod will remove from local storage.',PPF10))
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
                
            nx += r.width + 5*RATIO
            if nx > CURRENT_SCREEN_SIZE[0]-60*RATIO:
                nx = 5
                ny += r.height + 5*RATIO
                
        for mods_buttons in buttons:
            select:pyge.Button = mods_buttons[0]
            delete:pyge.Button = mods_buttons[1]
            
            select.rect.top = select.position[1] + y_shift * RATIO
            delete.rect.top = delete.position[1] + y_shift * RATIO
            mod_name = str(select._id).replace('select_button','')
            if select.value:
                if mod_name not in CONFIG['enable_mods']:
                    CONFIG['enable_mods'].append(mod_name)
                    GameObject.mods_enabled = CONFIG['enable_mods']
                elif mod_name in CONFIG['enable_mods']:
                    CONFIG['enable_mods'].remove(mod_name)
                    GameObject.mods_enabled = CONFIG['enable_mods']
            
            if delete.value:
                if mod_name in CONFIG['enable_mods']:
                    CONFIG['enable_mods'].remove(mod_name)
                    GameObject.mods_enabled = CONFIG['enable_mods']
                
                mods.remove_mod(mod_name)
                
                for widget in buttons_ids:
                    widgets = pge.findWidgetById(widget)
                    pge.widgets.remove(widgets)
                    
                buttons = []
                buttons_ids = []
                mods_widgets.remove(select)
                mods_widgets.remove(delete)
                    
                
            nx += r.width + 5
            if nx > CURRENT_SCREEN_SIZE[0]-60:
                nx = 0
                ny += r.height
        if Back_Button.value:
            run = False
        for ev in pge.events:
            if ev.type == pg.QUIT:
                pge.exit()
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    run = False
            elif ev.type == pg.MOUSEBUTTONDOWN:
                if pge.getMousePressed(5)[3]: run = False
        
        ShowFPS()
        pge.draw_widgets(mods_widgets)
        mods.draw_mods(pge,GameObject)
        # Screen Title + Shadow
        pge.draw_text((13*RATIO,15*RATIO),'Mods', GGF32, pge.Colors.DARKGRAY)
        pge.draw_text((15*RATIO,15*RATIO), 'Mods', GGF34, pge.Colors.WHITE)
        pge.update()
        pge.fill(pge.Colors.BLACK)
        pge.fpsw()
    db.update_value('cfg', 'data',0, CONFIG)
    db.save()

def options():
    """
    Options Screen
    """
    run = True
    Volume_Slider = GameMenu.OptionsMenu_VolumeSlider
    
    Screen_size_dropdown = GameMenu.OptionsMenu_ScreenSizeDropdown
    
    FPS_select = GameMenu.OptionsMenu_FPSSelect
    
    Fullscreen_checkbox = GameMenu.OptionsMenu_FullscreenCheckbox
    Fullscreen_checkbox.value = CONFIG['fullscreen']
    
    ShowFPS_checkbox = GameMenu.OptionsMenu_FPSCheckbox
    ShowFPS_checkbox.value = CONFIG['show_fps']
    
    FPSDynamic_checkbox = GameMenu.OptionsMenu_DynamicFPSCheckbox
    FPSDynamic_checkbox.value = CONFIG['dynamic_fps']
    
    SmoothScroll_checkbox = GameMenu.OptionsMenu_SmoothMouseScrollCheckbox
    
    RenderDistance_dropdown = GameMenu.OptionsMenu_RenderDistanceDropdown
    
    Back_Button = GameMenu.OptionsMenu_BackButton
    
    options_widgets = [
        Back_Button,
        Volume_Slider,
        Screen_size_dropdown,
        FPS_select,
        Fullscreen_checkbox,
        ShowFPS_checkbox,
        FPSDynamic_checkbox,
        SmoothScroll_checkbox,
        RenderDistance_dropdown
    ]
    while run:
        GAME_SCREEN = 2
        GameObject.screen_id = GAME_SCREEN
        if Back_Button.value: run = False
        # Screen Title + Shadow
        pge.draw_text((13*RATIO,15*RATIO),'Options', GGF32, pge.Colors.DARKGRAY)
        pge.draw_text((15*RATIO,15*RATIO), 'Options', GGF34, pge.Colors.WHITE)
        
        # Texts
        pge.draw_text((15*RATIO,70*RATIO), f'Volume: {int(Volume_Slider.value*100)}%', PPF16, pge.Colors.WHITE)
        pge.draw_text((20*RATIO,140*RATIO), f'Screen Size: ', PPF16, pge.Colors.WHITE)
        pge.draw_text((20*RATIO,180*RATIO), f'FPS:', PPF16, pge.Colors.WHITE)
        pge.draw_text((20*RATIO, 380*RATIO), f'Render Distance:', PPF16, pge.Colors.WHITE)
        
        # Update
        CONFIG['volume'] = round(Volume_Slider.value,2)
        CONFIG['screen_size'] = Screen_size_dropdown.current_text
        CONFIG['fps'] = FPS_select.value
        CONFIG['show_fps'] = ShowFPS_checkbox.value
        CONFIG['fullscreen'] = Fullscreen_checkbox.value
        CONFIG['dynamic_fps'] = FPSDynamic_checkbox.value
        CONFIG['RenderDistance'] = RenderDistance_dropdown.current_text
        CONFIG['smooth_scroll'] = SmoothScroll_checkbox.value
        GameObject.config = CONFIG
        
        for ev in pge.events:
            if ev.type == pg.QUIT: pge.exit()
            elif ev.type == pg.KEYUP:
                if ev.key == pg.K_ESCAPE: run = False
                elif ev.key == pg.K_F1:
                    pdb.get_content()
            elif ev.type == pg.MOUSEBUTTONDOWN:
                if pge.getMousePressed(5)[3]: run = False

        ShowFPS()
        pge.draw_widgets(options_widgets)
        mods.draw_mods(pge,GameObject)
        pge.update()
        pge.fill(pge.Colors.BLACK)
        pge.fpsw()
        
    # Update Config
    db.update_value('cfg', 'data', 0, CONFIG)
    db.save()
    
    pge.setFPS(FPS_OPTIONS[CONFIG['fps']])
    pge.mouse.smooth_scroll = CONFIG['smooth_scroll']
    
def create_save():
    name_list1 = ['Robert','Carl','Michael','Stew','John','David','Sonic','Shapened','Robloxian','Ex','Neymar','Usually','Mr']
    name_list2 = ['Hooke','Jonson','Stewart','Jones','Wright','Green','Pythonic','Gunner','Slicer','Ninja','Programmer','Jr','Potato','Juan']
    preset_name = random.choice(name_list1) + f'{"_" if random.randint(0,1)==1 else ""}' + random.choice(name_list2)
    
    run = True
    
    difficulties_select = GameMenu.CreateSaveMenu_DifficultiesSelect
    
    elements_dropdown = GameMenu.CreateSaveMenu_ElementsDropdown
    
    name_textbox = GameMenu.CreateSaveMenu_NameTextbox
    name_textbox.text = preset_name
    
    save_button = GameMenu.CreateSaveMenu_SaveButton
    cancel_button = GameMenu.CreateSaveMenu_CancelButton
    
    create_save_widgets = [difficulties_select, elements_dropdown,name_textbox,save_button, cancel_button]
    while run:
        GAME_SCREEN = 6
        GameObject.screen_id = GAME_SCREEN
        # Game Title + Shadow
        pge.draw_text((13*RATIO,15*RATIO),'Create Save', GGF32, pge.Colors.DARKGRAY)
        pge.draw_text((15*RATIO,15*RATIO), 'Create Save', GGF34, pge.Colors.WHITE)
        
        # Form
        pge.draw_text((10*RATIO, 100*RATIO), 'Name: ', PPF20, pge.Colors.WHITE)
        pge.draw_text((10*RATIO, 180*RATIO), 'Difficulty: ', PPF20, pge.Colors.WHITE)
        difficulties_select.colors[0] = colors['difficulty'][str(difficulties_select.value)]
        
        pge.draw_text((10*RATIO, 260*RATIO), 'Element: ', PPF20, pge.Colors.WHITE)
        elements_dropdown.colors[0] = colors['element'][str(elements_dropdown.current_text)]
        
        if cancel_button.value:
            run = False
        elif save_button.value:
            # Create Save
            SS = Save(name_textbox.value, difficulties_select.value, elements_dropdown.current_text)
            SS.id = SS.Savename+str(random.randint(0,10000))
            
            if 'saves' in db.tables.keys():
                db.add_value('saves', 'data',id=SS.id, value=SS.getData())
                db.save()
            run = False
        
        for ev in pge.events:
            if ev.type == pg.QUIT: pge.exit()
            elif ev.type == pg.KEYUP:
                if ev.key == pg.K_ESCAPE: run = False
            elif ev.type == pg.MOUSEBUTTONDOWN:
                if pge.getMousePressed(5)[3]: run = False
        
        ShowFPS()
        pge.draw_widgets(create_save_widgets)
        mods.draw_mods(pge,GameObject)
        pge.update()
        pge.fill(pge.Colors.BLACK)
        pge.fpsw()

def save_select():
    """
    Save Select Screen
    """
    current_save:Save = None
    saves:dict[Save,] = {}
    for save in db.get_all('saves'):
        x = Save('',0,0)
        x.loadData(save['data'])
        saves[str(save['id'])] = x
    
    # for id in saves.keys():
    #     save:Save = saves[id]
    #     print(id,save.Savename)
    
    Back_Button = GameMenu.GameSelectMenu_BackButton
    Create_Save_Button = GameMenu.GameSelectMenu_CreateSaveButton
    Load_Save_Button = GameMenu.GameSelectMenu_LoadSaveButton
    
    save_select_widgets = [Back_Button,Create_Save_Button,Load_Save_Button]
    buttons_save:list[list[pyge.Button, pyge.Button, Save]] = []
    
    to_confirm_delete = False
    to_delete_id:str = ''
    
    confirm_delete_button = GameMenu.GameSelectMenu_ConfirmDeleteButton
    cancel_delete_button = GameMenu.GameSelectMenu_CancelDeleteButton
    
    buttons_save_ids = []
    
    run = True
    while run:
        GAME_SCREEN = 1
        GameObject.screen_id = GAME_SCREEN
        pge.draw_text((240*RATIO, 551*RATIO),f'Current: {current_save.Savename[:10] if current_save else "None"}', PPF18, pge.Colors.WHITE, bgColor=pge.Colors.DARKGRAY, border_width=3, border_color=pge.Colors.BLACK)
        pge.draw_text((10*RATIO, 575*RATIO), f'Used Save Slots: {len(db.get_all("saves"))}/9', PPF12, pge.Colors.WHITE if len(db.get_all("saves")) < 9 else pge.Colors.DARKGRAY)
        if len(saves) <= 0: pge.draw_text((60*RATIO, 240*RATIO),'A little bit empty here...', PPF18, pge.Colors.DARKGRAY, alpha=200)
        if Back_Button.value: run = False
        if Load_Save_Button.value and current_save is not None:
            game(current_save)
        if Create_Save_Button.value and len(db.get_all('saves')) < 9:
            create_save()
            saves:dict[Save,] = {}
            for save in db.get_all('saves'):
                x = Save('',0,0)
                x.loadData(save['data'])
                saves[str(save['id'])] = x
        pos = [50,65]
        for save_id in saves.keys():
            if pos[0] >= 800-230:
                pos[0] = 50
                pos[1] += 125
            save:Save = saves[save_id]
            pge.draw_rect((pos[0]*RATIO, pos[1]*RATIO),(230*RATIO, 120*RATIO), pge.Colors.DARKGRAY,alpha=120)
            pge.draw_text(((pos[0]+5)*RATIO,(pos[1]+10)*RATIO), str(save.Savename)[:12], PPF18, pge.Colors.WHITE)
            pge.draw_text(((pos[0]+5)*RATIO,(pos[1]+30)*RATIO), f'Difficulty: {difficulties[save.Saveworld.difficulty]}', PPF8, colors['difficulty'][str(save.Saveworld.difficulty)])
            pge.draw_text(((pos[0]+5)*RATIO,(pos[1]+40)*RATIO), f'Element: {elements[save.Saveplayer.element]}', PPF8, colors['element'][str(save.Saveplayer.element)])
            
            id1 = f'{save_id}button_select'
            id2 = f'{save_id}button_delete'
            if (not pge.findWidgetById(id1)) and (not pge.findWidgetById(id2)):
                select_btn = pyge.Button(pge, ((pos[0]+5)*RATIO, (pos[1]+100)*RATIO), PPF14, 'SELECT', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK],id=id1)
                delete_btn = pyge.Button(pge, ((pos[0]+95)*RATIO, (pos[1]+100)*RATIO), PPF14, 'DELETE', [pge.Colors.RED, P_DARKGRAY, pge.Colors.BLACK],id=id2)
                
                save_select_widgets.append(select_btn)
                save_select_widgets.append(delete_btn)
                buttons_save_ids.append(id1)
                buttons_save_ids.append(id2)
                buttons_save.append([select_btn,delete_btn, save])
            else:
                try:
                    select_btn = pge.findWidgetById(id1)
                    delete_btn = pge.findWidgetById(id2)
                    
                    if select_btn not in save_select_widgets:
                        save_select_widgets.append(select_btn)
                    if delete_btn not in save_select_widgets:
                        save_select_widgets.append(delete_btn)
                    if [select_btn,delete_btn, save] not in buttons_save:
                        buttons_save.append([select_btn,delete_btn, save])
                    if id1 not in buttons_save_ids:
                        buttons_save_ids.append(id1)
                    if id2 not in buttons_save_ids:
                        buttons_save_ids.append(id2)
                except: pass
            
            pos[0] += 235
        
        for buttons in buttons_save:
            if current_save is not None:
                if buttons[0].value:
                    current_save = buttons[2]
                    to_confirm_delete = False
                elif buttons[1].value and not to_confirm_delete:
                    to_confirm_delete = True
                    to_delete_id = buttons[2].id
            else:
                current_save = buttons[2]
                to_confirm_delete = False
            
        for ev in pge.events:
            if ev.type == pg.QUIT: pge.exit()
            elif ev.type == pg.KEYUP:
                if ev.key == pg.K_ESCAPE: run = False
            elif ev.type == pg.MOUSEBUTTONDOWN:
                if pge.getMousePressed(5)[3]: run = False
                
        ShowFPS()
        pge.draw_widgets(save_select_widgets)
        mods.draw_mods(pge,GameObject, current_save=current_save)
        if to_confirm_delete and not (to_delete_id in ['',' ',None,'None']):
            pge.draw_rect((30*RATIO, 290*RATIO), (740*RATIO, 150*RATIO), pge.Colors.DARKGRAY, alpha=190, border_color=pge.Colors.LIGHTGRAY, border_width=3)
            pge.draw_text((40*RATIO, 300*RATIO), 'Are you sure you want to delete this save?', PPF16, pge.Colors.WHITE)
            pge.draw_text((40*RATIO, 330*RATIO), f'Savename: {to_delete_id}', PPF12, pge.Colors.WHITE)
            confirm_delete_button.draw()
            cancel_delete_button.draw()
            keys = pge.getKeys()
            id1 = f'{to_delete_id}button_select'
            id2 = f'{to_delete_id}button_delete'
            if keys[pg.K_y]: # Delete
                db.delete_values('saves',to_delete_id)
                db.save()
                # Remove all wdigets for this from engine
                for widget in pge.widgets.copy():
                    if widget._id in buttons_save_ids:
                        pge.widgets.remove(widget)
                        save_select_widgets.remove(widget) # Remove from save_select_widgets too
                buttons_save = []
                buttons_save_ids = []
                
                # Reload Saves
                saves:dict[Save,] = {}
                for save in db.get_all('saves'):
                    x = Save('',0,0)
                    x.loadData(save['data'])
                    saves[str(save['id'])] = x
                
                to_confirm_delete = False
                to_delete_id = ''
            elif keys[pg.K_n]: # Cancel
                to_confirm_delete = False
                to_delete_id = ''
            else:
                if confirm_delete_button.value: # Delete
                    db.delete_values('saves',to_delete_id)
                    db.save()
                    # Remove all wdigets for this from engine
                    for widget in pge.widgets.copy():
                        if widget._id in buttons_save_ids:
                            pge.widgets.remove(widget)
                            save_select_widgets.remove(widget) # Remove from save_select_widgets too
                    buttons_save = []
                    buttons_save_ids = []
                    
                    # Reload Saves
                    saves:dict[Save,] = {}
                    for save in db.get_all('saves'):
                        x = Save('',0,0)
                        x.loadData(save['data'])
                        saves[str(save['id'])] = x
                    
                    to_confirm_delete = False
                    to_delete_id = ''
                elif cancel_delete_button.value: # Cancel
                    to_confirm_delete = False
                    to_delete_id = ''
        # Screen Title + Shadow
        pge.draw_text((13*RATIO,15*RATIO),'Save Select', GGF32, pge.Colors.DARKGRAY)
        pge.draw_text((15*RATIO,15*RATIO), 'Save Select', GGF34, pge.Colors.WHITE)
        
        pge.update()
        pge.fill(pge.Colors.BLACK)
        pge.fpsw()