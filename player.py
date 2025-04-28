import pygame
import math
from constant import *
from mapas import *

class Player():
    def __init__(self ,map):
        self.red=(255,0,0)
        self.radius=8
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
        
        self.has_shot=False
        self.damage=10
        self.reloading=False
        self.space_was_pressed = False

    
        # Initialize direction and plane
        self.dir_x = math.cos(self.rotationangle)
        self.dir_y = math.sin(self.rotationangle)
        self.plane_x = -self.dir_y * 0.66
        self.plane_y = self.dir_x * 0.66

        self.spritecolision=False

        self.health=100
    def update_direction_and_plane(self):
        self.dir_x = math.cos(self.rotationangle)
        self.dir_y = math.sin(self.rotationangle)
        self.plane_x = -self.dir_y * 0.66
        self.plane_y = self.dir_x * 0.66
        # end of update_direction_and_plane for sprites
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
            # elif self.spritecolision and :
            #     self.walkdirection=0
        if keys[pygame.K_s]:
            self.walkdirection=-1
            if self.colision_with_wallbackward(map):
                self.walkdirection=0

        # Interact with doors
        if keys[pygame.K_e]:
            target_x = self.x + math.cos(self.rotationangle) * TILESIZE // 2
            target_y = self.y + math.sin(self.rotationangle) * TILESIZE // 2
            map.toggle_door(target_x, target_y)
            pygame.time.delay(500)




        if keys[pygame.K_SPACE] and not self.reloading  and not self.space_was_pressed:
        # and not self.reloading: 
           
            self.has_shot=True
            self.reloading=True
            print("self.has_shot")
            self.space_was_pressed = True

        if not keys[pygame.K_SPACE]:
            self.space_was_pressed = False

        movestep=self.walkdirection*self.movespeed
        self.rotationangle+=self.turndirection*self.rotationspeed
        self.x+=math.cos(self.rotationangle)*movestep
        self.y+=math.sin(self.rotationangle)*movestep
        self.update_direction_and_plane()
    def player_position(self,screen):
        pygame.draw.circle(screen,self.red,(self.x ,self.y),self.radius)
        
        pygame.draw.line(screen,self.red, (self.x ,self.y),(self.x+math.cos(self.rotationangle)*50 ,self.y+math.sin(self.rotationangle)*50))
        #print(math.sin(self.rotationangle))