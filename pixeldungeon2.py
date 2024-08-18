from data.src import constant
from data.src.config import *
from data.src.screens import options, save_select, modsscreen

class ButtonState:
    is_down = False
    was_down = False

class MouseState:
    x = 0
    y = 0
    left_button = ButtonState()
    middle_button = ButtonState()
    right_button = ButtonState()

class InputState:
    key = {}
    mouse = MouseState()

class GameState:
    mode = constant.Menu.MAIN
    old_input_state = InputState()
    input_state = InputState()
    #@TODO: Clean up
    Confirm_Button = pyge.Button(pge, (50*RATIO, 130*RATIO), PPF16, 'Confirm (Y)', [P_LIGHTRED, P_DARKGRAY, pge.Colors.BLACK])
    Cancel_Button = pyge.Button(pge, (400*RATIO, 130*RATIO), PPF16, 'Cancel (N)', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])

def confirm_exit(game_state):
    """
    Confirm Exit
    """
    result = False
    
    will_exit = False
    
    Confirm_Button = game_state.Confirm_Button
    Cancel_Button = game_state.Cancel_Button
    
    exit_widgets = [
        game_state.Confirm_Button,
        game_state.Cancel_Button
    ]
    
    key = game_state.input_state.key        

    if key[constant.Key.Y].is_down:
        will_exit = True
        result = True    
    elif key[constant.Key.N].is_down:
        game_state.mode = constant.Menu.MAIN

    pge.fill(pge.Colors.BLACK)

    # Title Screen  + Shadow
    pge.draw_text((13*RATIO,15*RATIO),'Confirm Exit', GGF32, pge.Colors.DARKGRAY)
    pge.draw_text((15*RATIO,15*RATIO), 'Confirm Exit', GGF34, pge.Colors.WHITE)
    
    # Texts
    pge.draw_text((50*RATIO,100*RATIO), 'Are you sure you want to exit?', PPF24, pge.Colors.WHITE)          

    if Confirm_Button.value:
        will_exit = True
        result = True
    elif Cancel_Button.value:
        will_exit = False
        game_state.mode = constant.Menu.MAIN
    
    pge.draw_widgets(exit_widgets)

    if will_exit:
        pge.exit()
    
    return result

def main():
    """
    Main Loop + Main Menu
    """
    # setup our input_state, I forgot the mouse btw...
    game_state = GameState() 
    for key, value in vars(constant.Key).items():
        if (not callable(value)) and (not key.startswith("__")):
            game_state.input_state.key[value] = ButtonState()

    pge.enableFPS_unstable(CONFIG['dynamic_fps'])
    Play_Button = pyge.Button(pge, (25*RATIO, 100*RATIO), PPF26, 'PLAY', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    Options_Button = pyge.Button(pge, (25*RATIO, 138*RATIO), PPF26, 'OPTIONS', [P_LIGHTBLUE, P_DARKGRAY, pge.Colors.BLACK])
    Mods_Button = pyge.Button(pge, (25*RATIO, 176*RATIO), PPF26, 'MODS', [P_YELLOW, P_DARKGRAY, pge.Colors.BLACK])
    Exit_Button = pyge.Button(pge, (25*RATIO, 214*RATIO), PPF26, 'EXIT', [P_LIGHTRED, P_DARKGRAY, pge.Colors.BLACK])
    
    main_widgets = [
        Play_Button,
        Options_Button,
        Mods_Button,
        Exit_Button
    ]    
    
    GameObject.pid = os.getpid()
    mods.import_mods(pge, GameObject)    
    is_running = True
    while is_running:
        # events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pge.exit()
            elif (event.type == pg.KEYDOWN) or (event.type == pg.KEYUP):
                key = event.key
                is_down = event.type == pg.KEYDOWN           
                game_state.input_state.key[key].is_down = is_down 
        
        # logic
        key = game_state.input_state.key        

        if key[constant.Key.ESCAPE].is_down:
            Exit_Button.value = True

        if Play_Button.value:
            game_state.mode = constant.Menu.SAVE_SELECT
        elif Options_Button.value:
            game_state.mode = constant.Menu.OPTIONS
        elif Mods_Button.value: 
            game_state.mode = constant.Menu.MODS_SCREEN
        elif Exit_Button.value:
            game_state.mode = constant.Menu.CONFIRM_EXIT
        
        Play_Button.value = Options_Button.value = Mods_Button.value = Exit_Button.value = False

        # draw
        pge.fill(pge.Colors.BLACK)
        
        if game_state.mode == constant.Menu.MAIN:
            GameObject.screen_id = game_state.mode
            # Game Title + Shadow
            pge.draw_text((13*RATIO,15*RATIO), f'{GAME_TITLE}', GGF54,pge.Colors.DARKGRAY)
            pge.draw_text((15*RATIO,15*RATIO), f'{GAME_TITLE}', GGF56,pge.Colors.WHITE)
            
            # Game version
            pge.draw_text((20*RATIO,70*RATIO), f'Version {GAME_VERSION}', PPF16,pge.Colors.WHITE)                                       
            
            pge.draw_widgets(main_widgets)  
        elif game_state.mode == constant.Menu.SAVE_SELECT:
            try:
                save_select()
            except Exception as e:
                raise e
        elif game_state.mode == constant.Menu.OPTIONS:
            options()
        elif game_state.mode == constant.Menu.MODS_SCREEN: 
            modsscreen()
        elif game_state.mode == constant.Menu.CONFIRM_EXIT:
            confirm_exit_result = confirm_exit(game_state)
            is_running = not confirm_exit_result

        #@TODO: Should probably be the last thing we do but i need to fix the timer first. Also its not my fault to be messy.
        for key, value in vars(constant.Key).items():
            if (not callable(value)) and (not key.startswith("__")):
                game_state.input_state.key[value].was_down = game_state.input_state.key[value].is_down

        mods.draw_mods(pge,GameObject)
        ShowFPS()
        pg.display.update()
        pge.fpsw()        

def run():
    if __name__ == '__main__':
        main()
        pge.is_running = False
        
run()