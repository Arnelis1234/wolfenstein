import random
from sprites import *
from constant import *
from mapas import *
import math
import pygame
from ray import *
class NPC(AnimatedSprite):
    def __init__(self, player, raycaster,map, path="python/wolfenstein/sprite/npc/stand1.png", pos=(300, 200), scale=30, shift=0):
        super().__init__(player, raycaster, path, pos, scale, shift)
        self.shoot_images = self.get_images("python/wolfenstein/sprite/npc/shoot")
        self.death_images = self.get_images("python/wolfenstein/sprite/npc/death")
        self.stand_images = self.get_images("python/wolfenstein/sprite/npc/stand")
        self.hurt_images = self.get_images("python/wolfenstein/sprite/npc/hurt")
        self.walk_images = self.get_images("python/wolfenstein/sprite/npc/walk")
        self.pain_animationtrigger = False
        self.alive=True
        self.indexspeed = 0.05
        self.health = 100
        self.pain = False
        self.map=map
        # print(f"NPC initialized at position: x={self.x}, y={self.y}")
        # self.took_damage = False
        self.animation_0= False
        self.animation_1= False
        
       
        
        self.raycaster = raycaster
        self.player=player
        self.cansee=False
        self.x=pos[0]
        self.y=pos[1]
        self.distance=0


        self.is_facing_down = self.theta > 0 and self.theta < math.pi
        self.is_facing_up = not self.is_facing_down
        self.is_facing_right = self.theta < 0.5 * math.pi or self.theta > 1.5 * math.pi
        self.is_facing_left = not self.is_facing_right

    def check_hit_in_npc(self):
        if  self.player.has_shot and WINDOW_WIDTH/2- self.sprite_half_width < self.screen_x < WINDOW_HEIGHT + self.sprite_half_width:

                self.pain_animationtrigger = True
                self.animation_0==False
                self.pain = True
                if self.cansee==True:
                    self.health -= self.player.damage
                print(self.health)
                # kodel
                self.player.has_shot = False
    def health_check(self):
        if self.health <= 0:
            self.alive = False
        else:
            self.alive = True

    


    def damage_player(self):
        self.player.health -=5
        print(self.player.health)
        if self.player.health<5:
            pygame.quit()
            exit()

    def update(self):
        self.rajucaster()
        # print(normalize_angle(self.theta))
        self.move()
        self.image=self.animate()
        self.run()
        super().get_sprite()
        


    def run(self):
        # self.ray_check()
        self.health_check()
        if self.alive:
            
            self.check_hit_in_npc()
          
            if self.pain_animationtrigger == False:
                self.indexspeed = 0.025
                self.array = self.stand_images
                self.animate()


            

            if self.pain_animationtrigger == True and self.cansee==True:

                if self.animation_0==False:
                    self.index = 0
                    print("pain animation")
                    self.animation_0=True
                
                
       
             
                self.indexspeed = 0.07
                self.array = self.hurt_images
                self.animate()
                if self.index>= 4:
                    self.pain_animationtrigger = False
                    self.animation_0=False

           

            elif self.distance<100 and self.cansee==True and self.pain_animationtrigger==False: 
                if self.index>= 2.4:
                    self.index=0  
                    self.animation_1=False
                self.indexspeed = 0.007
                self.array = self.shoot_images
                self.animate()                     
                if self.index>= 2 and self.animation_1==False:
                    self.damage_player()
                    
                    self.player

                    self.animation_1=True



            elif self.cansee and self.distance>100 :
                if self.index>= 3.4:
                    self.index=0
                
                self.indexspeed = 0.05
                self.array = self.walk_images
                self.animate()
 
                    

        else :
            self.indexspeed=0.07
            
            if self.index>= 4:
                
                self.indexspeed=0
            
            self.array = self.death_images
            self.animate()


        

    def rajucaster(self):
            ray=Ray(self.theta,self.player, self.map)
            ray.cast() 
            self.distance=math.sqrt((self.x - self.player.x) ** 2 + (self.y - self.player.y) ** 2)
            if ray.distance<self.distance:
                self.cansee=False   
            else:
                self.cansee=True


            if self.distance<=20:
                self.player.spritecolision=True
            else:
                self.player.spritecolision=False
            

    def move(self):
        if self.cansee==True and self.alive==True and self.pain_animationtrigger==False:
            if self.distance>100:
                dx = -math.cos(self.theta) 
                dy = -math.sin(self.theta) 
                self.x += dx 
                self.y += dy 

        # else:
        #     self.x+=random.randint(-1,1)
        #     self.y+=random.randint(-1,1)

        # print(self.x,self.y)











