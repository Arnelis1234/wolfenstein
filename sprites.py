


import pygame 
from constant import *

import os
# from collections import deque

class SpriteObject:
    def __init__(self, player,raycaster, path='python/wolfenstein/sprite/light1.png',
                 pos=(300,200), scale=50, shift=0):
   
        self.player = player
       
        self.x, self.y = pos
        self.image = pygame.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

  
        self.raycaster=raycaster

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = (self.theta - self.player.rotationangle) % (2 * math.pi)


        # if (dx > 0 and self.player.rotationangle > math.pi) or (dx < 0 and dy < 0):
        #     delta += math.tau
        if delta > math.pi:
            delta -= 2 * math.pi
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        # krc pirma window witht buvo screen distance bet pakeitus tai ir dar delta numinusuotu -2pi veikia

        #nu jo cia tipo printina kai ekrano yra spraitai bet screen x man atrodo vidury yra ir kai nutolsta nuo spraito  krc spraitas nepalieka ekrano
        if -self.IMAGE_WIDTH-100 < self.screen_x < (WINDOW_WIDTH + self.IMAGE_WIDTH+100) and self.norm_dist > 17:
            proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
            proj_width, proj_height = proj * self.IMAGE_RATIO, proj

            image = pygame.transform.scale(self.image, (proj_width, proj_height))

            self.sprite_half_width = proj_width // 2
            height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
            pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

            self.raycaster.objects_to_render.append((self.norm_dist, image, pos))    

    def update(self):
        self.get_sprite()
        # self.image = pygame.transform.scale(self.image, (self.SPRITE_SCALE, self.SPRITE_SCALE))
        # self.image.set_colorkey((255, 0, 255))        



# class AnimatedSprite(SpriteObject):
#     def __init__(self, player,raycaster,path="python/wolfenstein/sprite/animated/anim1.png",
#                  pos=(100, 100), scale=50, shift=-0.1, animation_time=120):
#         super().__init__(player,raycaster, path, pos, scale, shift)
   
     
        
#         self.images = pygame.image.load(path).convert_alpha()
#         self.path = self.path = path.rsplit('/', 1)[0]

#         self.index = 0

#         self.array = [
#             #  "python/wolfenstein/sprite/animated/anim1.png",
#             #  "python/wolfenstein/sprite/animated/anim2.png", 
#             #  "python/wolfenstein/sprite/animated/anim3.png",
#             # "python/wolfenstein/sprite/animated/anim4.png"
#         ]


#     def update(self):
#         self.image=self.animate()
#         super().get_sprite()
        
        
#     def animate(self):
#         # self.array=os.listdir(self.path)
        
#         b=pygame.image.load(self.array[int(self.index)]).convert_alpha()
       
#         self.index+=0.15
        
#         if self.index>=len(self.array):
#             self.index=0
#         return b
   

    

class AnimatedSprite(SpriteObject):
    def __init__(self, player,raycaster,path="python/wolfenstein/sprite/animated/anim1.png",
                 pos=(100, 100), scale=50, shift=-0.1):
        super().__init__(player,raycaster, path, pos, scale, shift)

        
        self.index = 0
        self.path = path.rsplit('/', 1)[0]
        self.array = self.get_images(self.path)
        self.image=None
        self.indexspeed=0.15
    def update(self):
        self.image=self.animate()

        super().get_sprite()
      
        
    def animate(self):
        # self.array=os.listdir(self.path)
        
        b=pygame.image.load(self.array[int(self.index)]).convert_alpha()
       
        self.index+=self.indexspeed
        
        if self.index>=len(self.array):
            self.index=0
        return b
    

    def get_images(self, path):
        images = []
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = (path + '/' + file_name)
                images.append(img)
        
        
        return images