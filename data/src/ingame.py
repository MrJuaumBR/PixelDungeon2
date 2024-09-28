from .config import *

from .save import Save,Player, World
from data.src.tiles import Red_Brick


def game(save:Save):
    """
    Game Loop
    """
    player:Player = save.Saveplayer
    world:World = save.Saveworld
    world.add(player)
    
    Menu_widgets = [GameMenu.InGame_ResumeButton, GameMenu.InGame_SaveButton, GameMenu.InGame_QuitButton, GameMenu.InGame_QuitToDesktopButton]
    
    Menu_Open:bool = False
    
    run = True    
    while run:
        GAME_SCREEN = 4
        GameObject.screen_id = GAME_SCREEN
        
        world.draw()
        if Menu_Open:
            pge.draw_rect((5*RATIO,5*RATIO), (300*RATIO, (CURRENT_SCREEN_SIZE[1]-10)*RATIO),pge.Colors.DARKGRAY, 2, pge.Colors.WHITE, alpha=128)
            pge.draw_text((7*RATIO, 10*RATIO), 'Menu', PPF24, pge.Colors.WHITE)
            pge.draw_widgets(Menu_widgets)
            pge.draw_text((10*RATIO, 200*RATIO), f'Opened Times: {save.opened_times}', PPF14, pge.Colors.WHITE)
            
            if GameMenu.InGame_ResumeButton.value:
                Menu_Open = False
            elif GameMenu.InGame_SaveButton.value:
                db.update_value('saves', 'data', save.id, save.getData())
                db.save()
            elif GameMenu.InGame_QuitButton.value:
                run = False
            elif GameMenu.InGame_QuitToDesktopButton.value:
                db.update_value('saves', 'data', save.id, save.getData())
                db.save()
                pge.exit()
        
        for ev in pge.events:
            if ev.type == pyge.QUIT:
                # Autosaves
                db.update_value('saves', 'data', save.id, save.getData())
                db.save()
                pge.exit()
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    Menu_Open = not Menu_Open
                elif ev.key == pg.K_b:
                    print(f'Offset: {world.offset.xy}')
        
        
        mods.draw_mods(pge,GameObject, player=player, world=world)
        ShowFPS()
        pge.update()
        world.update()
        pge.fpsw()
        pge.fill(pge.Colors.BLACK)
        
        
    db.update_value('saves', 'data', save.id, save.getData())
    db.save()