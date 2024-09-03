from .config import *

from .save import Save,Player, World


def game(save:Save):
    """
    Game Loop
    """
    player:Player = save.Saveplayer
    world:World = save.Saveworld
    world.gen_world()
    save.opened_times += 1
    
    menu_resumeButton = pyge.Button(pge, (50*RATIO, 70*RATIO), PPF16, 'RESUME', [pge.Colors.LIGHTGREEN, pge.Colors.DARKGREEN])
    menu_saveButton = pyge.Button(pge, (50*RATIO, 90*RATIO), PPF16, 'SAVE', [pge.Colors.LIGHTBLUE, pge.Colors.DARKBLUE])
    menu_exitButton = pyge.Button(pge, (50*RATIO, 110*RATIO), PPF16, 'EXIT', [pge.Colors.LIGHTRED, pge.Colors.DARKRED])
    menu_exitButton2 = pyge.Button(pge, (50*RATIO, 130*RATIO), PPF14, 'EXIT TO DESKTOP', [pge.Colors.LIGHTRED, pge.Colors.DARKRED])
    
    menu_isOpen:bool = False
    
    menu_widgets = [menu_resumeButton, menu_saveButton, menu_exitButton, menu_exitButton2]
    for wid in menu_widgets:
        x = pge.findWidgetById(wid._id)
        if x:
            pge.widgets.remove(x)
    run = True
    def draw_menu(menu_isOpen:bool, run:bool):
        if menu_resumeButton.value: menu_isOpen = False
        if menu_saveButton.value:
            db.update_value('saves', 'data', save.id, save.getData())
        if menu_exitButton.value: run = False
        if menu_exitButton2.value: 
            db.update_value('saves', 'data', save.id, save.getData())
            pge.exit()
        
        
        pge.draw_rect((25*RATIO,25*RATIO), (250*RATIO,250*RATIO), P_DARKGRAY, 3, pge.Colors.LIGHTGRAY, alpha=180)
        pge.draw_text((55*RATIO,30*RATIO), f'PAUSED', GGF22,pge.Colors.DARKGRAY)
        pge.draw_text((57*RATIO,30*RATIO), f'PAUSED', GGF22,pge.Colors.WHITE)
        pge.draw_widgets(menu_widgets)
        
        return menu_isOpen, run

    while run:
        GAME_SCREEN = 4
        GameObject.screen_id = GAME_SCREEN
        if menu_isOpen: menu_isOpen, run = draw_menu(menu_isOpen, run)
        for ev in pge.events:
            if ev.type == pg.QUIT: pge.exit()
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    menu_isOpen:bool = not menu_isOpen
        
        
        ShowFPS()
        world.update()
        pge.update()
        mods.draw_mods(pge, GameObject, game_variables=dict(globals(), **locals()))
        pge.fpsw()
        pge.fill(pge.Colors.BLACK)
        world.draw()
    db.update_value('saves', 'data', save.id, save.getData())