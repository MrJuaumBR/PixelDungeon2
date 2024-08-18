from data.src import constant
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

def game(game_state, save:Save):
    """
    Game Loop
    """
    player:Player = save.Saveplayer
    world:World = save.Saveworld
    if save.opened_times == 0:
        world.gen_world()
    save.opened_times += 1

    game_state.menu_exitButton.value = False    

    menu_widgets = [game_state.menu_resumeButton, game_state.menu_saveButton, game_state.menu_exitButton, game_state.menu_exitButton2]
    GAME_SCREEN = constant.Menu.GAME
    GameObject.screen_id = GAME_SCREEN 
    
    key = game_state.input_state.key
    if key[constant.Key.BACKSPACE].is_down and not key[constant.Key.BACKSPACE].was_down:
        game_state.menu_isOpen = not game_state.menu_isOpen    
        
    for wid in menu_widgets:
        x = pge.findWidgetById(wid._id)
        if x:
            pge.widgets.remove(x)

    world.update()

    pge.fill(pge.Colors.BLACK)

    def draw_menu(menu_isOpen:bool):
        run = True
        if game_state.menu_resumeButton.value: 
            menu_isOpen = False
        if game_state.menu_saveButton.value:
            db.update_value('saves', 'data', save.id, save.getData())
        if game_state.menu_exitButton.value: 
            run = False
        if game_state.menu_exitButton2.value: 
            db.update_value('saves', 'data', save.id, save.getData())
            pge.exit()        
        
        pge.draw_rect((25*RATIO,25*RATIO), (250*RATIO,250*RATIO), P_DARKGRAY, 3, pge.Colors.LIGHTGRAY, alpha=180)
        pge.draw_text((55*RATIO,30*RATIO), f'PAUSED', GGF22,pge.Colors.DARKGRAY)
        pge.draw_text((57*RATIO,30*RATIO), f'PAUSED', GGF22,pge.Colors.WHITE)
        pge.draw_widgets(menu_widgets)
        
        return menu_isOpen, run
               
    world.draw()
    mods.draw_mods(pge, GameObject, game_variables=dict(globals(), **locals())) 

    if game_state.menu_isOpen: 
        game_state.menu_isOpen, run = draw_menu(game_state.menu_isOpen)  

    ShowFPS()
    
    if game_state.menu_exitButton.value:
        game_state.menu_isOpen = False
        db.update_value('saves', 'data', save.id, save.getData())

def create_save(game_state):
    name_list1 = ['Robert','Carl','Michael','Stew','John','David','Sonic','Shapened','Robloxian','Ex','Neymar','Usually','Mr']
    name_list2 = ['Hooke','Jonson','Stewart','Jones','Wright','Green','Pythonic','Gunner','Slicer','Ninja','Programmer','Jr','Potato','Juan']
    preset_name = random.choice(name_list1) + f'{"_" if random.randint(0,1)==1 else ""}' + random.choice(name_list2)    

    create_save_widgets = [game_state.difficulties_select, game_state.elements_select, game_state.name_textbox, game_state.save_button, game_state.cancel_button]       

    GAME_SCREEN = constant.Menu.CREATE_SAVE
    GameObject.screen_id = GAME_SCREEN
    
    pge.fill(pge.Colors.BLACK)
    
    # Game Title + Shadow
    pge.draw_text((13*RATIO,15*RATIO),'Create Save', GGF32, pge.Colors.DARKGRAY)
    pge.draw_text((15*RATIO,15*RATIO), 'Create Save', GGF34, pge.Colors.WHITE)

    # Form
    pge.draw_text((10*RATIO, 100*RATIO), 'Name: ', PPF20, pge.Colors.WHITE)
    pge.draw_text((10*RATIO, 180*RATIO), 'Difficulty: ', PPF20, pge.Colors.WHITE)
    game_state.difficulties_select.colors[0] = colors['difficulty'][str(game_state.difficulties_select.value)]
    
    pge.draw_text((10*RATIO, 260*RATIO), 'Element: ', PPF20, pge.Colors.WHITE)
    game_state.elements_select.colors[0] = colors['element'][str(game_state.elements_select.value)]
    
    if game_state.cancel_button.value:
        game_state.name_textbox.text = preset_name
        game_state.Create_Save_Button.value = False
    elif game_state.save_button.value:
        # Create Save
        SS = Save(game_state.name_textbox.value, game_state.difficulties_select.value, game_state.elements_select.value)
        SS.id = SS.Savename+str(random.randint(0,10000))
        
        if 'saves' in db.tables.keys():
            db.add_value('saves', 'data',id=SS.id, value=SS.getData())
            db.save()
        game_state.name_textbox.text = preset_name
        game_state.Create_Save_Button.value = False  
            
    #@TODO: HACK
    for widget in create_save_widgets:
        if widget == None:            
            widget.build_widget_display() 
        elif widget == game_state.name_textbox:
            if game_state.name_textbox.active:
                for key in game_state.key_pressed:
                    if (key >= constant.Key.SPACE) and (key <= constant.Key.Z):
                        game_state.name_textbox.text += chr(key)
                    
                    game_state.key_pressed.pop(0)
            else:
                game_state.key_pressed.clear()

    pge.draw_widgets(create_save_widgets)
    mods.draw_mods(pge,GameObject)

    ShowFPS()   

def save_select(game_state):
    """
    Save Select Screen
    """
    
    saves:dict[Save,] = {}
    for save in db.get_all('saves'):
        x = Save('',0,0)
        x.loadData(save['data'])
        saves[str(save['id'])] = x
    
    # for id in saves.keys():
    #     save:Save = saves[id]
    #     print(id,save.Savename)
            
    save_select_widgets = [game_state.Back_Button2, game_state.Create_Save_Button, game_state.Load_Save_Button]
    buttons_save:list[list[pyge.Button, pyge.Button, Save]] = []        
    buttons_save_ids = [] 
    
    if game_state.Back_Button2.value: 
        game_state.Play_Button.value = False
        game_state.mode = constant.Menu.MAIN

    GAME_SCREEN = constant.Menu.SAVE_SELECT
    GameObject.screen_id = GAME_SCREEN    
    if len(saves) <= 0: pge.draw_text((60*RATIO, 240*RATIO),'A little bit empty here...', PPF18, pge.Colors.DARKGRAY, alpha=200)
    
    if game_state.Create_Save_Button.value and len(db.get_all('saves')) < 9:        
        create_save(game_state)
        saves:dict[Save,] = {}
        for save in db.get_all('saves'):
            x = Save('',0,0)
            x.loadData(save['data'])
            saves[str(save['id'])] = x

    if game_state.Create_Save_Button.value:
        return

    pge.fill(pge.Colors.BLACK)

    # Screen Title + Shadow
    pge.draw_text((13*RATIO,15*RATIO),'Save Select', GGF32, pge.Colors.DARKGRAY)
    pge.draw_text((15*RATIO,15*RATIO), 'Save Select', GGF34, pge.Colors.WHITE)

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
    
    #game_state.current_save = buttons_save[0][2]
    for buttons in buttons_save:
        if game_state.current_save == None:
            game_state.current_save = buttons[2]

        if buttons[0].value:
            game_state.current_save = buttons[2]
        elif buttons[1].value:
            game_state.to_confirm_delete = True
            game_state.to_delete_id = buttons[2].id       

    pge.draw_text((240*RATIO, 551*RATIO),f'Current: {game_state.current_save.Savename[:10] if game_state.current_save else "None"}', PPF18, pge.Colors.WHITE, bgColor=pge.Colors.DARKGRAY, border_width=3, border_color=pge.Colors.BLACK)
    pge.draw_text((10*RATIO, 575*RATIO), f'Used Save Slots: {len(db.get_all("saves"))}/9', PPF12, pge.Colors.WHITE if len(db.get_all("saves")) < 9 else pge.Colors.DARKGRAY)                
                    
    if game_state.to_confirm_delete and not (game_state.to_delete_id in ['',' ',None,'None']):
        pge.draw_rect((30*RATIO, 290*RATIO), (740*RATIO, 150*RATIO), pge.Colors.DARKGRAY, alpha=190, border_color=pge.Colors.LIGHTGRAY, border_width=3)
        pge.draw_text((40*RATIO, 300*RATIO), 'Are you sure you want to delete this save?', PPF16, pge.Colors.WHITE)
        pge.draw_text((40*RATIO, 330*RATIO), f'Savename: {game_state.to_delete_id}', PPF12, pge.Colors.WHITE)
        game_state.confirm_delete_button.draw()
        game_state.cancel_delete_button.draw()
        keys = game_state.input_state.key #pge.getKeys()
        id1 = f'{game_state.to_delete_id}button_select'
        id2 = f'{game_state.to_delete_id}button_delete'
        if keys[constant.Key.Y].is_down: # Delete
            db.delete_values('saves',game_state.to_delete_id)
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
            game_state.to_delete_id = ''
        elif keys[constant.Key.N].is_down: # Cancel
            to_confirm_delete = False
            game_state.to_delete_id = ''
        else:
            if game_state.confirm_delete_button.value: # Delete
                db.delete_values('saves',game_state.to_delete_id)
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
                game_state.to_delete_id = ''
            elif game_state.cancel_delete_button.value: # Cancel
                to_confirm_delete = False
                game_state.to_delete_id = ''    

    if game_state.Load_Save_Button.value and game_state.current_save is not None:
        game(game_state, game_state.current_save)
        if not game_state.menu_exitButton.value:
            return

    #@TODO: HACK
    for widget in save_select_widgets:
        if widget == None:
            widget.build_widget_display() 
    pge.draw_widgets(save_select_widgets)
    mods.draw_mods(pge,GameObject, current_save=game_state.current_save)
    
    ShowFPS()   