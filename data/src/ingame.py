from .config import *

from .save import Save,Player, World
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

def game():
    """
    Game Loop
    """
    
    run = True
    while run:
        GAME_SCREEN = 4
        for ev in pge.events:
            if ev.type == pg.QUIT: pge.exit()
        
        ShowFPS()
        pge.update()
        pge.fill(pge.Colors.BLACK)
        pge.fpsw()

def create_save():
    name_list1 = ['Robert','Carl','Michael','Stew','John','David','Sonic','Shapened','Robloxian','Ex','Neymar','Usually','Mr']
    name_list2 = ['Hooke','Jonson','Stewart','Jones','Wright','Green','Pythonic','Gunner','Slicer','Ninja','Programmer','Jr','Potato','Juan']
    preset_name = random.choice(name_list1) + f'{"_" if random.randint(0,1)==1 else ""}' + random.choice(name_list2)
    
    run = True
    
    difficulties_select = pyge.Select(pge, (40*RATIO, 210*RATIO), PPF16, [P_PEAR, P_DARKGRAY, pge.Colors.BLACK], difficulties, 1, True)
    
    elements_select = pyge.Select(pge, (40*RATIO, 290*RATIO), PPF16, [P_PEAR, P_DARKGRAY, pge.Colors.BLACK], elements, random.randint(0, len(elements)-1), True)
    
    name_textbox = pyge.Textbox(pge, (40*RATIO, 130*RATIO), 20, [pge.Colors.DARKGRAY, pge.Colors.DARKGREEN, pge.Colors.WHITE, pge.Colors.WHITE], PPF16, preset_name)
    
    save_button = pyge.Button(pge, (40*RATIO, 370*RATIO), PPF20, 'SAVE', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    cancel_button = pyge.Button(pge, (300*RATIO, 370*RATIO), PPF20, 'CANCEL', [P_LIGHTRED, P_DARKGRAY, pge.Colors.BLACK])
    
    create_save_widgets = [difficulties_select, elements_select,name_textbox,save_button, cancel_button]
    while run:
        GAME_SCREEN = 6
        # Game Title + Shadow
        pge.draw_text((13*RATIO,15*RATIO),'Create Save', GGF32, pge.Colors.DARKGRAY)
        pge.draw_text((15*RATIO,15*RATIO), 'Create Save', GGF34, pge.Colors.WHITE)
        
        # Form
        pge.draw_text((10*RATIO, 100*RATIO), 'Name: ', PPF20, pge.Colors.WHITE)
        pge.draw_text((10*RATIO, 180*RATIO), 'Difficulty: ', PPF20, pge.Colors.WHITE)
        difficulties_select.colors[0] = colors['difficulty'][str(difficulties_select.value)]
        
        pge.draw_text((10*RATIO, 260*RATIO), 'Element: ', PPF20, pge.Colors.WHITE)
        elements_select.colors[0] = colors['element'][str(elements_select.value)]
        
        if cancel_button.value:
            run = False
        elif save_button.value:
            # Create Save
            SS = Save(name_textbox.value, difficulties_select.value, elements_select.value)
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
    
    Back_Button = pyge.Button(pge, (5*RATIO, 5*RATIO), PPF12, '< BACK', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    Create_Save_Button = pyge.Button(pge, (10*RATIO, 550*RATIO), PPF20, 'CREATE SAVE', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    Load_Save_Button = pyge.Button(pge, (600*RATIO, 550*RATIO), PPF20, 'LOAD SAVE', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    
    save_select_widgets = [Back_Button,Create_Save_Button,Load_Save_Button]
    buttons_save:list[list[pyge.Button, pyge.Button, Save]] = []
    
    to_confirm_delete = False
    to_delete_id:str = ''
    
    confirm_delete_button = pyge.Button(pge, (40*RATIO, 350*RATIO), PPF20, 'CONFIRM(y)', [P_LIGHTRED, P_DARKGRAY, pge.Colors.BLACK])
    cancel_delete_button = pyge.Button(pge, (250*RATIO, 350*RATIO), PPF20, 'CANCEL(n)', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    
    buttons_save_ids = []
    
    run = True
    while run:
        GAME_SCREEN = 1
        pge.draw_text((240*RATIO, 551*RATIO),f'Current: {current_save.Savename[:10] if current_save else "None"}', PPF18, pge.Colors.WHITE, bgColor=pge.Colors.DARKGRAY, border_width=3, border_color=pge.Colors.BLACK)
        pge.draw_text((10*RATIO, 575*RATIO), f'Used Save Slots: {len(db.get_all("saves"))}/9', PPF12, pge.Colors.WHITE if len(db.get_all("saves")) < 9 else pge.Colors.DARKGRAY)
        if len(saves) <= 0: pge.draw_text((60*RATIO, 240*RATIO),'A little bit empty here...', PPF18, pge.Colors.DARKGRAY, alpha=200)
        if Back_Button.value: run = False
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
            pge.draw_text(((pos[0]+5)*RATIO,(pos[1]+30)*RATIO), f'Difficulty: {difficulties[save.Saveworld.diffculty]}', PPF8, colors['difficulty'][str(save.Saveworld.diffculty)])
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
                    select_btn = pge.widgets[pge.findWidgetById(id1)]
                    delete_btn = pge.widgets[pge.findWidgetById(id2)]
                    
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
            if buttons[0].value:
                current_save = buttons[2]
                to_confirm_delete = False
            elif buttons[1].value and not to_confirm_delete:
                to_confirm_delete = True
                to_delete_id = buttons[2].id
            
        for ev in pge.events:
            if ev.type == pg.QUIT: pge.exit()
            elif ev.type == pg.KEYUP:
                if ev.key == pg.K_ESCAPE: run = False
            elif ev.type == pg.MOUSEBUTTONDOWN:
                if pge.getMousePressed(5)[3]: run = False
                
        ShowFPS()
        pge.draw_widgets(save_select_widgets)
        if to_confirm_delete and not (to_delete_id in ['',' ',None,'None']):
            pge.draw_rect((30*RATIO, 290*RATIO), (740*RATIO, 150*RATIO), pge.Colors.DARKGRAY, alpha=190, border_color=pge.Colors.LIGHTGRAY, border_width=3)
            pge.draw_text((40*RATIO, 300*RATIO), 'Are you sure you want to delete this save?', PPF16, pge.Colors.WHITE)
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