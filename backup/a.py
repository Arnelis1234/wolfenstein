import math
TILESIZE=64
EILES =10
STULPAI=15
WINDOW_WIDTH=STULPAI*TILESIZE
WINDOW_HEIGHT=EILES*TILESIZE
FOV=math.pi/3
RES=1

NUM_RAYS= WINDOW_WIDTH//RES




SCALE = WINDOW_WIDTH // NUM_RAYS
HALF_HEIGHT=WINDOW_HEIGHT//2
DIST = NUM_RAYS / (2 * math.tan(FOV/2))
PROJ_COEFF =DIST * TILESIZE



HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS

import math, pygame
from constant import *
from mapas import Map
from player import *

def normalize_angle(angle):
    angle = angle % (2 * math.pi)
    if (angle <= 0):
        angle = (2 * math.pi) + angle
    return angle

def distance_between(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))


class Ray:
    def __init__(self, angle, player, map):
        self.rayAngle = normalize_angle(angle)
        self.player= Player = player
        self.map: Map = map

        self.is_facing_down = self.rayAngle > 0 and self.rayAngle < math.pi
        self.is_facing_up = not self.is_facing_down
        self.is_facing_right = self.rayAngle < 0.5 * math.pi or self.rayAngle > 1.5 * math.pi
        self.is_facing_left = not self.is_facing_right

        self.wall_hit_x = 0
        self.wall_hit_y = 0

        self.distance = 0

        self.color = 255

        self.offset=0 


        self.map_tile=0

        self.texturehas=None
    def cast(self):
        # HORIZONTAL CHECKING
        found_horizontal_wall = False
        horizontal_hit_x = 0
        horizontal_hit_y = 0

        # The first intersection is the intersection where we need to offset by the player's position
        first_intersection_x = None
        first_intersection_y = None

        # finding y first
        if self.is_facing_up:
            first_intersection_y = ((self.player.y // TILESIZE) * TILESIZE) - 0.01
        elif self.is_facing_down:
            first_intersection_y = ((self.player.y // TILESIZE) * TILESIZE) + TILESIZE
        
        # finding x
        first_intersection_x = self.player.x + (first_intersection_y - self.player.y) / math.tan(self.rayAngle)

        # These variables will be used later
        nextHorizontalX = first_intersection_x
        nextHorizontalY = first_intersection_y

        # NOW, that we just figured out the first intersection, we need to continue checking
        # However, now the player won't go into our calculations

        xa = 0
        ya = 0


        # 1. Finding Ya
        if self.is_facing_up:
            ya = -TILESIZE
        elif self.is_facing_down:
            ya = TILESIZE
        
        # 2. Finding Xa
        xa = ya / math.tan(self.rayAngle)

        """
        if hit wall 
            store the position of the horizontal hit
        else
            add xa and ya to the current position
        """

        # while it is inside the window
        while (nextHorizontalX <= WINDOW_WIDTH and nextHorizontalX >= 0 and nextHorizontalY <= WINDOW_HEIGHT and nextHorizontalY >= 0):
            if self.map.position(nextHorizontalX, nextHorizontalY):
                found_horizontal_wall = True
                horizontal_hit_x = nextHorizontalX
                horizontal_hit_y = nextHorizontalY
                #self.texturehas=self.map.position(nextHorizontalX, nextHorizontalY)
                break
            else:
                nextHorizontalX += xa
                nextHorizontalY += ya
            

        # VERTICAL CHECKING
        found_vertical_wall = False
        vertical_hit_x = 0
        vertical_hit_y = 0

        if self.is_facing_right:
            first_intersection_x = ((self.player.x // TILESIZE) * TILESIZE) + TILESIZE
        elif self.is_facing_left:
            first_intersection_x = ((self.player.x // TILESIZE) * TILESIZE) - 0.01
        
        first_intersection_y = self.player.y + (first_intersection_x - self.player.x) * math.tan(self.rayAngle)
        
        nextVerticalX = first_intersection_x
        nextVerticalY = first_intersection_y

        # Now that we found the first intersection, we continue without the player, just as before

        # 1. Find Xa (just the width of the grid)

        if self.is_facing_right:
            xa = TILESIZE
        elif self.is_facing_left:
            xa = -TILESIZE
        
        ya = xa * math.tan(self.rayAngle)

        # while it is inside the window
        while (nextVerticalX <= WINDOW_WIDTH and nextVerticalX >= 0 and nextVerticalY <= WINDOW_HEIGHT and nextVerticalY >= 0):
            if self.map.position(nextVerticalX, nextVerticalY):
                found_vertical_wall = True
                vertical_hit_x = nextVerticalX
                vertical_hit_y = nextVerticalY

                # if self.map.position(nextVerticalX, nextHorizontalY) ==3:
                  
                break
            else:
                nextVerticalX += xa
                nextVerticalY += ya

        # # testing (temp)

        # self.wall_hit_x = horizontal_hit_x
        # self.wall_hit_y = horizontal_hit_y


        # DISTANCE CALCULATION

        horizontal_distance = 0
        vertical_distance = 0

        if found_horizontal_wall:
            horizontal_distance = distance_between(self.player.x, self.player.y, horizontal_hit_x, horizontal_hit_y)
        else:
            horizontal_distance = 999
        if found_vertical_wall:
            vertical_distance = distance_between(self.player.x, self.player.y, vertical_hit_x, vertical_hit_y)
        else:
            vertical_distance = 999
        

        if horizontal_distance < vertical_distance:
            self.wall_hit_x = horizontal_hit_x
            self.wall_hit_y = horizontal_hit_y
            self.distance = horizontal_distance
            self.color = 160
            self.offset=horizontal_hit_x
            

        else:
            self.wall_hit_x = vertical_hit_x
            self.wall_hit_y = vertical_hit_y
            self.distance = vertical_distance
            self.offset=vertical_hit_y

            # if vertical_offset==0:
            #     vertical_offset=TILESIZE  

        self.map_tile=self.map.position(self.wall_hit_x, self.wall_hit_y)

        self.distance *= math.cos(self.player.rotationangle - self.rayAngle)

        self.color *= (1 / self.distance) * 60
        if self.color > 255:
            self.color = 255
        elif self.color < 0:
            self.color = 0

    def render(self, screen):
        pygame.draw.line(screen, (255, 0, 0), 
                         (self.player.x, self.player.y), 
                         (self.wall_hit_x, self.wall_hit_y))


import pygame
import math
from constant import *
from python.wolfenstein.mapas import *
#from ray import *
from player import *
from python.wolfenstein.ray import *
from raycast import *
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))











map=Map()
player=Player(map)
clock=pygame.time.Clock()
renderer=ObjectRenderer()
raycaster=Raycaster(player, map,renderer)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.set_caption(f"{clock.get_fps()}")
    pygame.draw.rect(screen, (60,60,60),(0,0,WINDOW_WIDTH, WINDOW_HEIGHT/2))
    pygame.draw.rect(screen, (200,200,200),(0,WINDOW_HEIGHT/2,WINDOW_WIDTH, WINDOW_HEIGHT))
    #map.render(screen) 
    player.update(map)
    raycaster.castallrays()

    player.player_position(screen)    
    #player.colision_with_wall() 
    raycaster.render(screen)    
    pygame.display.update()


import pygame
from constant import *
from python.wolfenstein.rayhujnia import *

class Map():
    def __init__(self):
        self.grid=[
            [1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [2, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [2, 0, 0, 2, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   ]

    def position(self, x,y):
        return self.grid[int(y // TILESIZE)][int(x // TILESIZE)]

    def render(self, screen):
        screen.fill((60,60,60))
        for i in range(10):
            for j in range(15):
                tilex=j*TILESIZE
                tiley=i*TILESIZE

                if self.grid[i][j]==1:
                    pygame.draw.rect(screen, (0,0,0),(tilex,tiley,TILESIZE-1,TILESIZE -1))
                else:
                    pygame.draw.rect(screen, (255,255,255),(tilex,tiley,TILESIZE-1,TILESIZE -1))

import pygame
from constant import *


class ObjectRenderer:
    def __init__(self):
      
        self.texture_paths = {
            1: "python/wolfenstein/textures/1.png",
            2: "python/wolfenstein/textures/2.png",
            3: "python/wolfenstein/textures/3.png",
        }
        self.wall_textures = self.load_wall_textures()
    


    def load_wall_textures(self):
        textures = {}
        for texture_id, texture_path in self.texture_paths.items():
            textures[texture_id] = pygame.transform.scale(pygame.image.load(texture_path).convert_alpha(), (TILESIZE, TILESIZE))
        return textures

    def get_texture_path(self, texture_id):
        return self.wall_textures.get(texture_id)
    
    import pygame
import math
from constant import *
from python.wolfenstein.mapas import *

class Player():
    def __init__(self ,map):
        self.red=(255,0,0)
        self.radius=6
        self.x=80
        self.y=80
        self.turndirection=0
        self.walkdirection=0
        self.rotationangle=0*math.pi/180
        self.movespeed=2.5
        self.rotationspeed=2*math.pi/180

        self.map=map
        self.colisionx=False
        self.colisionx=False


    def colision_with_wallforward(self,map):
        self.colisionx=False        
        target_x=self.x+math.cos(self.rotationangle)*self.radius
        target_y=self.y+math.sin(self.rotationangle)*self.radius
        if self.map.position(target_x,target_y):
            return True
        else : False             
        
            
            #print("colision")
            # self.x-=math.cos(self.rotationangle)*self.radius
            # self.y-=math.sin(self.rotationangle)*self.radius

    def colision_with_wallbackward(self,map):
        self.colisiony=False
        target_x=self.x-math.cos(self.rotationangle)*self.radius
        target_y=self.y-math.sin(self.rotationangle)*self.radius
        if self.map.position(target_x,target_y):
            return True
        else : False
          
            #print("colision")
            # self.x+=math.cos(self.rotationangle)*self.radius
            # self.y+=math.sin(self.rotationangle)*self.radius

    def update(self,map):
        keys=pygame.key.get_pressed()
        self.turndirection=0
        self.walkdirection=0

        if keys[pygame.K_d]:
            self.turndirection=1
        if keys[pygame.K_a]:
            self.turndirection=-1
        if keys[pygame.K_w]:
            
            # if self.colision_with_wallx(self.map)==False:
            #     self.walkdirection=0
               
            self.walkdirection=1
            if self.colision_with_wallforward(map):
                self.walkdirection=0
        if keys[pygame.K_s]:
            self.walkdirection=-1
            if self.colision_with_wallbackward(map):
                self.walkdirection=0
        movestep=self.walkdirection*self.movespeed
        self.rotationangle+=self.turndirection*self.rotationspeed
        self.x+=math.cos(self.rotationangle)*movestep
        self.y+=math.sin(self.rotationangle)*movestep

    def player_position(self,screen):
        pygame.draw.circle(screen,self.red,(self.x ,self.y),self.radius)
        
        pygame.draw.line(screen,self.red, (self.x ,self.y),(self.x+math.cos(self.rotationangle)*50 ,self.y+math.sin(self.rotationangle)*50))
        #print(math.sin(self.rotationangle))

        import pygame
from constant import *
from python.wolfenstein.ray import *
from object_rend import *
class Raycaster:
    def __init__(self, player,map,object_renderer):
        # self.object_renderer = object_renderer
        self.rays=[]
        self.player=player 
        self.map=map   
        self.texture=None
        self.object_renderer = object_renderer
        # self.texture1=pygame.transform.scale(pygame.image.load("python/wolfenstein/textures/1.png").convert_alpha(), (TILESIZE, TILESIZE))
        # self.texture2=pygame.transform.scale(pygame.image.load("python/wolfenstein/textures/2.png").convert_alpha(), (TILESIZE, TILESIZE))
        # self.texture3=pygame.transform.scale(pygame.image.load("python/wolfenstein/textures/3.png").convert_alpha(), (TILESIZE, TILESIZE))
    def castallrays(self):
        self.rays=[]
        rayangle=self.player.rotationangle-FOV/2    
        for i in range (NUM_RAYS):
            ray=Ray(rayangle,self.player, self.map)
            ray.cast()
            self.rays.append(ray)

            rayangle+=FOV/NUM_RAYS
    
    # def render(self, screen):
    #     for i, ray in enumerate(self.rays):
    #         # Calculate the line height based on the distance to the wall
    #         line_height = (TILESIZE / ray.distance) * (WINDOW_HEIGHT / 2)

    #         # Ensure the line height does not exceed the screen height
    #         line_height = min(line_height, WINDOW_HEIGHT)

    #         # Calculate the start and end positions for the wall slice
    #         draw_begin = max(0, (WINDOW_HEIGHT / 2) - (line_height / 2))
    #         draw_end = min(WINDOW_HEIGHT, (WINDOW_HEIGHT / 2) + (line_height / 2))

    #         # Calculate the x-coordinate for the current ray
    #         x = i * (WINDOW_WIDTH / NUM_RAYS)

    #         # Draw the wall slice as a rectangle
    #         pygame.draw.rect(screen, (255, 0, 0), (x, draw_begin, (WINDOW_WIDTH / NUM_RAYS), draw_end - draw_begin))
    

    
    
    def render (self, screen ):   
                       
        i=0
        for ray in self.rays:
            # ray.render(screen)
            ray.distance = max(ray.distance, 0.1)
            self.texture = self.object_renderer.get_texture_path(ray.map_tile)

              

            wall_column = self.texture.subsurface(ray.offset%TILESIZE, 0, 1, TILESIZE)
            wall_column = pygame.transform.scale(wall_column, (SCALE, int(PROJ_COEFF / ray.distance)))
            screen.blit(wall_column, (i * SCALE, HALF_HEIGHT - wall_column.get_height() // 2))
            i+=1
       