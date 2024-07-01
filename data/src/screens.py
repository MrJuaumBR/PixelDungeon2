from .ingame import *

def modsscreen():
    """
    Mods screen
    """
    run = True
    Back_Button = pyge.Button(pge, (5*RATIO, 5*RATIO), PPF12, '< BACK', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    
    Warn_LongText = pyge.Longtext(pge, (0, (DEFAULT_SCREEN_SIZE[1]-100)*RATIO), PPF14, f'A Total of: {len(mods.mods)} mods loaded!\nPlease be careful about the mods you use, mods can be used for scam peoples, and then, steal information.', [pge.Colors.WHITE, P_DARKGRAY, pge.Colors.BROWN])
    
    mods_widgets = [Back_Button, Warn_LongText]
    
    while run:        
        GAME_SCREEN = 3
        if Back_Button.value: run = False
        
        nx,ny = 0,30
        for mod in mods.mods:
            r = pge.draw_rect(((nx+30)*RATIO,(ny+30)*RATIO), (256*RATIO,128*RATIO), P_DARKGRAY, 3,pge.Colors.DARKBROWN) # Background
            pge.draw_text(((nx+40)*RATIO,(ny+40)*RATIO), mod[0]['Mod_Name'][:18], PPF14, pge.Colors.WHITE) # Mod Name
            pge.draw_text(((nx+35)*RATIO,(ny+55)*RATIO), str(mod[1])[:24], PPF10, pge.Colors.GRAY) # Mod Path
            pge.draw_text(((nx+35)*RATIO,(ny+70)*RATIO),mod[0]['Mod_Author'][:24], PPF12, pge.Colors.WHITE) # Mod Author
            pge.draw_text(((nx+35)*RATIO,(ny+85)*RATIO), mod[0]['Mod_Version'][:24], PPF12, pge.Colors.WHITE) # Mod Version
            
            # Description
            texts = split_lines(mod[0]['Mod_Description'][:64], PPF12, 128*RATIO)
            pos = [nx+30, (ny+105)*RATIO]
            for line in texts:
                pge.draw_text(pos, line, PPF10, pge.Colors.WHITE)
                pos[1] += PPF10.size(line)[1]
                
            
            
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
        # Screen Title + Shadow
        pge.draw_text((13*RATIO,15*RATIO),'Mods', GGF32, pge.Colors.DARKGRAY)
        pge.draw_text((15*RATIO,15*RATIO), 'Mods', GGF34, pge.Colors.WHITE)
        pge.update()
        pge.fill(pge.Colors.BLACK)
        pge.fpsw()

def options():
    """
    Options Screen
    """
    run = True
    Volume_Slider = pyge.Slider(pge, (20*RATIO, 100*RATIO), (740*RATIO,30*RATIO), [P_PEAR, P_DARKGRAY, P_DARKGRAY],value=CONFIG['volume'], fill_passed=True)
    Screen_size_select = pyge.Select(pge, (250*RATIO, 140*RATIO),PPF14, [pge.Colors.WHITE, pge.Colors.BLACK, P_DARKGRAY], [f'{c[0]}x{c[1]}' for c in SCREEN_SIZE_OPTIONS], CONFIG['screen_size'], False)
    FPS_select = pyge.Select(pge, (130*RATIO, 180*RATIO),PPF14, [pge.Colors.WHITE, pge.Colors.BLACK, P_DARKGRAY], [f'{c}' for c in FPS_OPTIONS], CONFIG['fps'], False)
    Fullscreen_checkbox = pyge.Checkbox(pge, (20*RATIO, 220*RATIO), PPF14, 'Fullscreen', [pge.Colors.WHITE, P_LIGHTRED, P_LIGHTGREEN, P_DARKGRAY])
    Fullscreen_checkbox.value = CONFIG['fullscreen']
    
    ShowFPS_checkbox = pyge.Checkbox(pge, (20*RATIO, 260*RATIO), PPF14, 'Show FPS', [pge.Colors.WHITE, P_LIGHTRED, P_LIGHTGREEN, P_DARKGRAY])
    ShowFPS_checkbox.value = CONFIG['show_fps']
    
    FPSDynamic_checkbox = pyge.Checkbox(pge, (20*RATIO, 300*RATIO), PPF14, 'Dynamic FPS', [pge.Colors.WHITE, P_LIGHTRED, P_LIGHTGREEN, P_DARKGRAY])
    FPSDynamic_checkbox.value = CONFIG['dynamic_fps']
    
    Mods_Button = pyge.Button(pge, (25*RATIO, 400*RATIO), PPF26, 'MODS', [P_PEAR, P_DARKGRAY, pge.Colors.BLACK])
    
    options_widgets = [
        Volume_Slider,
        Screen_size_select,
        FPS_select,
        Fullscreen_checkbox,
        ShowFPS_checkbox,
        Mods_Button,
        FPSDynamic_checkbox
    ]
    while run:
        GAME_SCREEN = 2
        # Screen Title + Shadow
        pge.draw_text((13*RATIO,15*RATIO),'Options', GGF32, pge.Colors.DARKGRAY)
        pge.draw_text((15*RATIO,15*RATIO), 'Options', GGF34, pge.Colors.WHITE)
        
        # Texts
        pge.draw_text((15*RATIO,70*RATIO), f'Volume: {int(Volume_Slider.value*100)}', PPF16, pge.Colors.WHITE)
        pge.draw_text((20*RATIO,140*RATIO), f'Screen Size: ', PPF16, pge.Colors.WHITE)
        pge.draw_text((20*RATIO,180*RATIO), f'FPS:', PPF16, pge.Colors.WHITE)
        
        # Update
        CONFIG['volume'] = round(Volume_Slider.value,2)
        CONFIG['screen_size'] = Screen_size_select.value
        CONFIG['fps'] = FPS_select.value
        CONFIG['show_fps'] = ShowFPS_checkbox.value
        CONFIG['fullscreen'] = Fullscreen_checkbox.value
        CONFIG['dynamic_fps'] = FPSDynamic_checkbox.value
        
        if Mods_Button.value: modsscreen()
        
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
        pge.update()
        pge.fill(pge.Colors.BLACK)
        pge.fpsw()
        
    # Update Config
    db.update_value('cfg', 'data', 0, CONFIG)
    db.save()
    
    pge.setFPS(FPS_OPTIONS[CONFIG['fps']])