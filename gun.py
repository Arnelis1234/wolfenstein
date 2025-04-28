import pygame
import math
import time
import asyncio
from constant import *
from sprites import AnimatedSprite
class Gun(AnimatedSprite):
    def __init__(self,player, raycaster,path="python/wolfenstein/sprite/gun/1.png",pos=(100,100),scale=10):
        super().__init__(player=player,raycaster=raycaster, path=path,pos=pos,scale=50)
        # self.indexspeed=0.1
        self.x=WINDOW_WIDTH/2-192/2
        self.y=WINDOW_HEIGHT-192
        # self.name = name
        # self.ammo = ammo
        # self.image = pygame.image.load(f"resources/gun/{name}.png").convert_alpha()
        self.indexspeed = 200  # Delay in milliseconds between frames
        self.last_update_time = pygame.time.get_ticks()  # Track the last update time
        self.current_index = 0 
        self.a=0
        # self.reloading=False

    def checkif_shot(self):
            if self.player.has_shot:
                self.player.reloading=True


    def reload(self,screen):#  self.image=pygame.image.load(self.path).convert_alpha()
        # self.checkif_shot()
        # if self.player.reloading==True:
        if  self.player.reloading==True: 
            
            self.a+=0.15
            if self.a>=len(self.array):
                self.player.has_shot=False    
                self.player.reloading=False
                self.a=0
            screen.blit(pygame.image.load(self.array[int(self.a)]).convert_alpha(), (self.x, self.y))
            # self.image=self.animate()
            # screen.blit(self.image, (self.x, self.y))

            
        else:
            first=pygame.image.load(self.array[0]).convert_alpha()
            screen.blit(first, (self.x, self.y))
        
        # self.image=self.animate()
        # super().get_sprite()
        # self.draw(screen)
    def update(self,screen):
        self.reload(screen)
        