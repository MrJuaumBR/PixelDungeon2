from typing import Any
from .config import *

from threading import Thread
from .map_generation import MapGenerator
from .player import Player
from .tiles import *

class World(pyge.pg.sprite.Group):
    saveable = ['difficulty', 'zoom']
    difficulty = 0
    player:Player
    surface:pyge.pg.SurfaceType
    mapgen:MapGenerator
    save = None
    zoom = 1
    gravity:float = 7.8
    time_of_day:int = 0
    
    x_shift:int = 0
    y_shift:int = 0
    
    bg_color:tuple[int,int,int] = (255,255,255)
    
    can_draw:bool = False
    def __init__(self, save,player:Player, diffculty = 0):
        super().__init__()
        self.save = save
        self.player = player
        self.difficulty = diffculty
        self.mapgen = MapGenerator(32,32,32)
        self.surface = pge.createSurface(self.mapgen.width*self.mapgen.pixel_size,self.mapgen.height*self.mapgen.pixel_size)
    def gen_world(self):
        if self.save.opened_times <= 0:
            print("World Generating...")
            self.mapgen.generate_map()
        else:
            self.mapgen.generate_map()
            
        terr = self.mapgen.str_terrain
        
        for y in range(len(terr)):
            for x in range(len(terr[y])):
                if terr[y][x] != 'air' and terr[y][x] != 'player':
                    sprite = getattr(sys.modules[__name__], f'Tile_{terr[y][x]}')(pyge.pg.math.Vector2(x*(self.mapgen.pixel_size-1),y*(self.mapgen.pixel_size-1)),pyge.pg.math.Vector2(self.mapgen.pixel_size,self.mapgen.pixel_size))
                    try:
                        self.add(sprite)
                    except Exception as e:
                        print(e)
                elif terr[y][x] == 'player' and self.player.is_spawned == False:
                    self.player.setPos((x*self.mapgen.pixel_size,y*self.mapgen.pixel_size), 'center')
                    self.player.is_spawned = True
                    
                    # Update X and Y Shift
                    self.x_shift = 0
                    self.y_shift = 0
    
    def delete_tiles(self):
        for sprite in self.sprites():
            if sprite.type != 'player':
                self.remove(sprite)
    
    def scroll_x(self):
        player = self.player
        if player:
            direction_x = player.direction.x
            
            speed = self.player.speed * self.zoom
            
            self.x_shift = (speed * direction_x)
            
    
    def scroll_y(self):
        player = self.player
        if player:
            direction_y = player.direction.y
            
            speed = self.player.speed * self.zoom
            
            self.y_shift = (speed * direction_y)
    
    def collision(self,player,sprite):
        if sprite.canCollide and sprite.canDamage:
            sprite.damage(player.damage)
    
    def x_collision(self, player_rect:pyge.pg.Rect):
        player = self.player
        
        # player.d.x += player.direction.x * player.speed
        for sprite in self.sprites():
            if sprite.type != 'player':
                try:
                    if sprite.canCollide:
                        if sprite.rect.colliderect(player.rect):
                            if player.direction.x < 0:
                                player.rect.right = sprite.rect.left
                            elif player.direction.x > 0:
                                player.rect.left = sprite.rect.right
                            self.collision(player,sprite)
                except Exception as ex: print('X Collision Error',ex)
                    
    def y_collision(self, player_rect:pyge.pg.Rect):
        player = self.player
        
        if not player.locked:
            player.apply_gravity()
            
        for sprite in self.sprites():
            if sprite.type != 'player':
                try:
                    if sprite.canCollide:
                        if sprite.rect.colliderect(player_rect):
                            if player.direction.y < 0:
                                player.rect.top = sprite.rect.bottom
                                player.direction.y = 0
                            elif player.direction.y > 0:
                                player.rect.bottom = sprite.rect.top
                                player.direction.y = 0
                                self.y_shift -= player.getGravity() * self.player.speed
                                player.on_floor = True
                            self.collision(player,sprite)
                except Exception as ex: raise(ex) #print('Y Collision Error',ex)
    
    def ScrollUpdate(self):
        for sprite in self.sprites():
            sprite.rect.x -= self.x_shift * ( 60 / FPS_OPTIONS[CONFIG['fps']] )
            sprite.rect.y -= self.y_shift * ( 60 / FPS_OPTIONS[CONFIG['fps']] )
            sprite.start_pos = (sprite.start_pos[0] - self.x_shift, sprite.start_pos[1] - self.y_shift)
        
        # Resets Scrolls
        self.x_shift = 0
        self.y_shift = 0
    
    def ScrollHandler(self):        
        # Make Scrolls
        plr_rect = pyge.pg.Rect(0,0,32,32)
        plr_rect.center = (CURRENT_SCREEN_SIZE[0]/2, CURRENT_SCREEN_SIZE[1]/2)
        self.scroll_x() # X Axis
        self.scroll_y() # Y Axis
        
        # Update Scrolls
        self.ScrollUpdate()
        
        # Collisions Detector
        #Thread(target=self.x_collision, args=(plr_rect,)).start() # Using Thread for Performance
        self.x_collision(plr_rect)
        self.y_collision(plr_rect)
                
    def draw(self):
        changed:bool = self.mapgen.hotreload_map()
        self.surface.fill(self.bg_color)
        if changed:
            print('Map Reload')
            # Clear sprites
            self.delete_tiles()
            
            self.gen_world()
        for sprite in self.sprites():
            sprite:pyge.pg.sprite.Sprite
            # Check if sprite is in Field Of View
            # Player Field Of View
            if self.player.FOV_Rect.colliderect(sprite.rect):
                # Is inside of FOV, then draw
            
                # Draw Sprite
                sprite.draw(self.surface,self.zoom)
                
        
        # Draw Player
        self.player.draw(self.surface,self.zoom)
        
        # def_size = self.surface.get_size()
        # rec:pg.rect.RectType = pg.Rect(0, 0, def_size[0]*self.zoom, def_size[1]*self.zoom)
        # rec.center = (CURRENT_SCREEN_SIZE[0]/2, CURRENT_SCREEN_SIZE[1]/2)
        
        # pge.screen.blit(pg.transform.scale(self.surface, rec.size), rec)

        pge.screen.blit(self.surface, (0,0))
        
    def getInput(self):
        ZOOM_IN = pge.hasKeyPressed(pg.K_PLUS) or pge.hasKeyPressed(pg.K_KP_PLUS) or pge.hasKeyPressed(pg.K_o)
        ZOOM_OUT = pge.hasKeyPressed(pg.K_MINUS) or pge.hasKeyPressed(pg.K_KP_MINUS) or pge.hasKeyPressed(pg.K_i)
        ZOOM_EQUAL = pge.hasKeyPressed(pg.K_EQUALS) or pge.hasKeyPressed(pg.K_KP_EQUALS) or pge.hasKeyPressed(pg.K_u) or pge.hasKeyPressed(pg.K_KP_ENTER)
        
        if ZOOM_IN:
            self.zoom += 0.05
            if self.zoom > 1.5: self.zoom = 1.5
        elif ZOOM_OUT:
            self.zoom -= 0.05
            if self.zoom < 0.7: self.zoom = 0.7
        elif ZOOM_EQUAL:
            self.zoom = 1
        
        if ZOOM_IN or ZOOM_OUT or ZOOM_EQUAL: # Changed Zoom
            # Needs to change player Rect
            self.player.rect.size = (self.player.irect.width * self.zoom, self.player.irect.height * self.zoom)
            self.player.rect.center = (CURRENT_SCREEN_SIZE[0]/2, CURRENT_SCREEN_SIZE[1]/2)
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.getInput()
        for sprite in self.sprites():
            if sprite.type != 'player':
                sprite.update(self.player)
            else:
                sprite.update()
                
        if not self.player.world:
            self.player.world = self
            
        self.ScrollHandler()
        self.player.update()
        return super().update(*args, **kwargs)
    
    def getCorrectData(self) -> dict:
        s:dict = {}
        for var in self.__dict__.keys():
            if var in self.saveable:
                s[var] = self.__dict__[var]
                
        s['mapgen'] = self.mapgen.data()
        return s
            
    def loadData(self,data:dict):
        for key in data.keys():
            if key in self.saveable:
                self.__dict__[key] = data[key]
            elif key == 'mapgen':
                self.mapgen = MapGenerator(0,0,0)
                self.mapgen.load_data(data[key])