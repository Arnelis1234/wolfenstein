import pygame
import math
from constant import *
from mapas import *
from ray import *
from player import *

from raycast import *

# from sprites import *
from  sprite_handler import *  
from gun import *
from npc import *
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# start_screen=pygame.transform.scale(pygame.image.load("python/wolfenstein/textures/Wolf3D-Title.png").convert_alpha(), (WINDOW_WIDTH,WINDOW_HEIGHT))
# def show_start_screen():
    
#     waiting = True
#     while waiting:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
              
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 waiting = False
#                 game_active=True
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     pygame.quit()
                
#                 waiting = False
#         screen.blit(start_screen, (0, 0))







game_active=True
map=Map()
player=Player(map)
clock=pygame.time.Clock()
renderer=ObjectRenderer()
raycaster=Raycaster(player, map,renderer)
# sprite=SpriteObject(player,raycaster)
# animatedSprite=AnimatedSprite(player,raycaster)
sprite_handler=ObjectHandler(player,raycaster,map)
# game =Game(player)
# show_start_screen()
gun=Gun(player,raycaster)
# npc=NPC(player,raycaster)
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and game_active==False:
            game_active=True

    if game_active:
        pygame.display.set_caption(f"{clock.get_fps()}")
        pygame.draw.rect(screen, (60,60,60),(0,0,WINDOW_WIDTH, WINDOW_HEIGHT/2))
        pygame.draw.rect(screen, (100,100,100),(0,WINDOW_HEIGHT/2,WINDOW_WIDTH, WINDOW_HEIGHT))
        #map.render(screen) 
        # plaayer.player_position(screen)  
        
        
        player.update(map)
        raycaster.castallrays()

        # #   
        
        raycaster.render()


        # sprite.get_sprite()
        # animatedSprite.update()



        sprite_handler.print_sprites()
        raycaster.render_objects(screen) 
        gun.update(screen)




        # npc.run(screen) 
        # npc.update(screen)
        # game.render_sprites(screen,raycaster.depth_buffer)
        pygame.display.update()
    
    
    
    # else:   
    #     screen.blit(start_screen, (0, 0))
    #     pygame.display.update()
    #     continue
    
pygame.quit()
