from data.src import constant
from data.src.config import *
from data.src.screens import options, save_select, modsscreen

class ButtonState:
    is_down = False
    was_down = False

class MouseState:
    x = 0
    y = 0
    button = [ButtonState()] * 4

class InputState:
    key = {}
    mouse = MouseState()

class GameState:
    mode = constant.Menu.MAIN
    old_input_state = InputState()
    input_state = InputState()
    
    Confirm_Button = pyge.Button(pge, (50*RATIO, 130*RATIO), PPF16, 'Confirm (Y)', [P_LIGHTRED, P_DARKGRAY, pge.Colors.BLACK])
    Cancel_Button = pyge.Button(pge, (400*RATIO, 130*RATIO), PPF16, 'Cancel (N)', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    
    Play_Button = pyge.Button(pge, (25*RATIO, 100*RATIO), PPF26, 'PLAY', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    Options_Button = pyge.Button(pge, (25*RATIO, 138*RATIO), PPF26, 'OPTIONS', [P_LIGHTBLUE, P_DARKGRAY, pge.Colors.BLACK])
    Mods_Button = pyge.Button(pge, (25*RATIO, 176*RATIO), PPF26, 'MODS', [P_YELLOW, P_DARKGRAY, pge.Colors.BLACK])
    Exit_Button = pyge.Button(pge, (25*RATIO, 214*RATIO), PPF26, 'EXIT', [P_LIGHTRED, P_DARKGRAY, pge.Colors.BLACK])

    Back_Button = pyge.Button(pge, (5*RATIO, 5*RATIO), PPF12, '< BACK', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])    
    Volume_Slider = pyge.Slider(pge, (20*RATIO, 100*RATIO), (740*RATIO,30*RATIO), [P_PEAR, P_DARKGRAY, P_DARKGRAY],value=CONFIG['volume'], fill_passed=True)    
    Screen_size_select = pyge.Select(pge, (250*RATIO, 140*RATIO),PPF14, [pge.Colors.WHITE, pge.Colors.BLACK, P_DARKGRAY], [f'{c[0]}x{c[1]}' for c in SCREEN_SIZE_OPTIONS], CONFIG['screen_size'], False, tip=('Screen Size, using the size of your monitor with Fullscreen ON will make it gives a quality gain.',PPF10))    
    FPS_select = pyge.Select(pge, (130*RATIO, 180*RATIO),PPF14, [pge.Colors.WHITE, pge.Colors.BLACK, P_DARKGRAY], [f'{c}' for c in FPS_OPTIONS], CONFIG['fps'], False, tip=('Sets the limit that the game will run of FPS.',PPF10))
    Fullscreen_checkbox = pyge.Checkbox(pge, (20*RATIO, 220*RATIO), PPF14, 'Fullscreen', [pge.Colors.WHITE, P_LIGHTRED, P_LIGHTGREEN, P_DARKGRAY],tip=('Enables fullscreen mode.',PPF10))
    ShowFPS_checkbox = pyge.Checkbox(pge, (20*RATIO, 260*RATIO), PPF14, 'Show FPS', [pge.Colors.WHITE, P_LIGHTRED, P_LIGHTGREEN, P_DARKGRAY],tip=('Shows FPS counter.',PPF10))
    RenderDistance_select = pyge.Select(pge, (300*RATIO, 340*RATIO),PPF14, [pge.Colors.WHITE, pge.Colors.BLACK, P_DARKGRAY], [f'{c}' for c in RenderDistance_OPTIONS], CONFIG['RenderDistance'], False, tip=('Render Distance in pixels.',PPF10))
    FPSDynamic_checkbox = pyge.Checkbox(pge, (20*RATIO, 300*RATIO), PPF14, 'Dynamic FPS', [pge.Colors.WHITE, P_LIGHTRED, P_LIGHTGREEN, P_DARKGRAY],tip=('Will make the Time system work better with FPS floating.',PPF10))
    
    Back_Button2 = pyge.Button(pge, (5*RATIO, 5*RATIO), PPF12, '< BACK', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    Create_Save_Button = pyge.Button(pge, (10*RATIO, 550*RATIO), PPF20, 'CREATE SAVE', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    Load_Save_Button = pyge.Button(pge, (600*RATIO, 550*RATIO), PPF20, 'LOAD SAVE', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    confirm_delete_button = pyge.Button(pge, (40*RATIO, 350*RATIO), PPF20, 'CONFIRM(y)', [P_LIGHTRED, P_DARKGRAY, pge.Colors.BLACK])
    cancel_delete_button = pyge.Button(pge, (250*RATIO, 350*RATIO), PPF20, 'CANCEL(n)', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    to_confirm_delete = False
    to_delete_id:str = ''    
    
def confirm_exit(game_state):
    """
    Confirm Exit
    """
    result = False
    
    # Logic
    will_exit = False
    
    Confirm_Button = game_state.Confirm_Button
    Cancel_Button = game_state.Cancel_Button
    
    exit_widgets = [
        game_state.Confirm_Button,
        game_state.Cancel_Button
    ]
    
    key = game_state.input_state.key

    if key[constant.Key.Y].is_down or Confirm_Button.value:
        will_exit = True
        result = True    
    elif key[constant.Key.N].is_down or Cancel_Button.value:
        game_state.Exit_Button.value = False
        game_state.mode = constant.Menu.MAIN

    # Draw
    pge.fill(pge.Colors.BLACK)

    # Title Screen  + Shadow
    pge.draw_text((13*RATIO,15*RATIO),'Confirm Exit', GGF32, pge.Colors.DARKGRAY)
    pge.draw_text((15*RATIO,15*RATIO), 'Confirm Exit', GGF34, pge.Colors.WHITE)
    
    # Texts
    pge.draw_text((50*RATIO,100*RATIO), 'Are you sure you want to exit?', PPF24, pge.Colors.WHITE)          
    
    pge.draw_widgets(exit_widgets)

    if will_exit:
        pge.exit()
    
    return result

def main():
    """
    Main Loop + Main Menu
    """
    # Setup our input_state
    game_state = GameState() 
    game_state.Fullscreen_checkbox.value = CONFIG['fullscreen']   
    game_state.ShowFPS_checkbox.value = CONFIG['show_fps']        
    game_state.FPSDynamic_checkbox.value = CONFIG['dynamic_fps']  

    for key, value in vars(constant.Key).items():
        if (not callable(value)) and (not key.startswith("__")):
            game_state.input_state.key[value] = ButtonState()

    pge.enableFPS_unstable(CONFIG['dynamic_fps'])    
    
    main_widgets = [
        game_state.Play_Button,
        game_state.Options_Button,
        game_state.Mods_Button,
        game_state.Exit_Button
    ]    
    
    GameObject.pid = os.getpid()
    mods.import_mods(pge, GameObject)    
    is_running = True
    while is_running:
        # Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pge.exit()
            elif (event.type == pg.KEYDOWN) or (event.type == pg.KEYUP):
                key = event.key
                is_down = event.type == pg.KEYDOWN         

                game_state.input_state.key[key].is_down = is_down 
            elif (event.type == pg.MOUSEBUTTONDOWN) or (event.type == pg.MOUSEBUTTONUP):
                is_down = event.type == pg.MOUSEBUTTONDOWN

                for index in range(0, len(game_state.input_state.mouse.button)):
                    if event.button == index:
                        game_state.input_state.mouse.button[index].is_down = is_down
                        break
            
        # Logic
        key = game_state.input_state.key        
        if key[constant.Key.ESCAPE].is_down:
            game_state.Exit_Button.value = True            
                
        if game_state.Play_Button.value:
            game_state.mode = constant.Menu.SAVE_SELECT
        elif game_state.Options_Button.value:
            game_state.mode = constant.Menu.OPTIONS
        elif game_state.Mods_Button.value: 
            game_state.mode = constant.Menu.MODS_SCREEN
        elif game_state.Exit_Button.value:
            game_state.mode = constant.Menu.CONFIRM_EXIT
        
        game_state.Play_Button.value = game_state.Options_Button.value = game_state.Mods_Button.value = game_state.Exit_Button.value = False

        # Draw
        #
        
        if game_state.mode == constant.Menu.MAIN:
            GameObject.screen_id = game_state.mode

            pge.fill(pge.Colors.BLACK)
            # Game Title + Shadow
            pge.draw_text((13*RATIO,15*RATIO), f'{GAME_TITLE}', GGF54,pge.Colors.DARKGRAY)
            pge.draw_text((15*RATIO,15*RATIO), f'{GAME_TITLE}', GGF56,pge.Colors.WHITE)
            
            # Game version
            pge.draw_text((20*RATIO,70*RATIO), f'Version {GAME_VERSION}', PPF16,pge.Colors.WHITE)                                       
            
            pge.draw_widgets(main_widgets)  
            mods.draw_mods(pge,GameObject)
            ShowFPS()
        elif game_state.mode == constant.Menu.SAVE_SELECT:
            try:
                save_select(game_state)
            except Exception as e:
                raise e
        elif game_state.mode == constant.Menu.OPTIONS:
            options(game_state)
        elif game_state.mode == constant.Menu.MODS_SCREEN: 
            modsscreen(game_state)
        elif game_state.mode == constant.Menu.CONFIRM_EXIT:
            confirm_exit_result = confirm_exit(game_state)
            is_running = not confirm_exit_result

        #@TODO: Should probably be the last thing we do but i need to fix the timer first. Also its not my fault to be messy.
        for key, value in vars(constant.Key).items():
            if (not callable(value)) and (not key.startswith("__")):
                game_state.input_state.key[value].was_down = game_state.input_state.key[value].is_down                
        for index in range(0, len(game_state.input_state.mouse.button)):
            game_state.input_state.mouse.button[index].was_down = game_state.input_state.mouse.button[index].is_down
        
        pg.display.update()
        pge.fpsw()        

def run():
    if __name__ == '__main__':
        main()
        pge.is_running = False
        
run()