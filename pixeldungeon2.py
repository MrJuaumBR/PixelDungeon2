from data.src.config import *
from data.src.screens import options, save_select


def confirm_exit():
    """
    Confirm Exit
    """
    run = True
    will_exit = False
    
    Confirm_Button = pyge.Button(pge, (50*RATIO, 130*RATIO), PPF16, 'Confirm (Y)', [P_LIGHTRED, P_DARKGRAY, pge.Colors.BLACK])
    Cancel_Button = pyge.Button(pge, (400*RATIO, 130*RATIO), PPF16, 'Cancel (N)', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    
    exit_widgets = [
        Confirm_Button,
        Cancel_Button
    ]
    start_frame = 0
    while run:
        GAME_SCREEN = 5
        if start_frame < pge.TimeSys.s2f(0.5):
            start_frame += 1
        
        # Title Screen  + Shadow
        pge.draw_text((13*RATIO,15*RATIO),'Confirm Exit', GGF32, pge.Colors.DARKGRAY)
        pge.draw_text((15*RATIO,15*RATIO), 'Confirm Exit', GGF34, pge.Colors.WHITE)
        
        # Texts
        pge.draw_text((50*RATIO,100*RATIO), 'Are you sure you want to exit?', PPF24, pge.Colors.WHITE)
        
        for ev in pge.events:
            if ev.type == pg.QUIT: pge.exit()
            elif ev.type == pg.KEYUP:
                if start_frame >= pge.TimeSys.s2f(0.5):
                    if ev.key == pg.K_ESCAPE: run = False
                    elif ev.key == pg.K_y:
                        will_exit = True
                        run = False
                    elif ev.key == pg.K_n:
                        will_exit = False
                        run = False
            elif ev.type == pg.MOUSEBUTTONDOWN:
                if pge.getMousePressed(5)[3]: run = False
                
        pge.draw_widgets(exit_widgets)
        pge.update()
        pge.fill(pge.Colors.BLACK)
    
    if will_exit:
        pge.exit()
    

def main():
    """
    Main Loop + Main Menu
    """
    pge.enableFPS_unstable(CONFIG['dynamic_fps'])
    Play_Button = pyge.Button(pge, (25*RATIO, 100*RATIO), PPF26, 'PLAY', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    Options_Button = pyge.Button(pge, (25*RATIO, 138*RATIO), PPF26, 'OPTIONS', [P_LIGHTBLUE, P_DARKGRAY, pge.Colors.BLACK])
    Exit_Button = pyge.Button(pge, (25*RATIO, 176*RATIO), PPF26, 'EXIT', [P_LIGHTRED, P_DARKGRAY, pge.Colors.BLACK])
    main_widgets = [
        Play_Button,
        Options_Button,
        Exit_Button
    ]
    mods.import_mods()
    while True:
        GAME_SCREEN = 0
        # Game Title + Shadow
        pge.draw_text((13*RATIO,15*RATIO), f'{GAME_TITLE}', GGF54,pge.Colors.DARKGRAY)
        pge.draw_text((15*RATIO,15*RATIO), f'{GAME_TITLE}', GGF56,pge.Colors.WHITE)
        
        # Game version
        pge.draw_text((20*RATIO,70*RATIO), f'Version {GAME_VERSION}', PPF16,pge.Colors.WHITE)
        
        # Buttons
        if Play_Button.value and GAME_SCREEN != 5:
            save_select()
        if Options_Button.value and GAME_SCREEN != 5:
            options()
        if Exit_Button.value:
            confirm_exit()
        
        for ev in pge.events:
            if ev.type == pg.QUIT:
                pge.exit()
            elif ev.type == pg.KEYUP:
                if ev.key == pg.K_ESCAPE:
                    confirm_exit()
        
        ShowFPS()
        pge.draw_widgets(main_widgets)        
        pge.update()
        pge.fill(pge.Colors.BLACK)
        pge.fpsw()


def run():
    if __name__ == '__main__':
        main()
run()