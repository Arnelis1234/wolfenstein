import pygame
import math
from constant import *
from mapas import *
from ray import *
from player import *
from raycast import *
from sprite_handler import *
from gun import *
from npc import *
from menu import *

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Wolfenstein")

# Game states
MENU = 0
GAME = 1
current_state = MENU

# Game objects initialization
map = Map()
player = Player(map)
renderer = ObjectRenderer()
raycaster = Raycaster(player, map, renderer)
sprite_handler = ObjectHandler(player, raycaster, map)
gunmanager = Gunmanager(player, raycaster)
clock = pygame.time.Clock()


def reset_game():
    global map, player, renderer, raycaster, sprite_handler, gunmanager
    # Reinitialize all game objects
    map = Map()
    player = Player(map)
    renderer = ObjectRenderer()
    raycaster = Raycaster(player, map, renderer)
    sprite_handler = ObjectHandler(player, raycaster, map)
    gunmanager = Gunmanager(player, raycaster)


# Main game loop
running = True
while running:
    clock.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # State management
    if current_state == MENU:
        # Show menu and wait for user choice
        menu_result = show_menu(screen)

        if menu_result == "start":
            reset_game()
            current_state = GAME
        elif menu_result == "quit":
            running = False

    elif current_state == GAME:
        # Game rendering and logic
        pygame.display.set_caption(f"{int(clock.get_fps())}")

        # Background
        pygame.draw.rect(screen, (60, 60, 60),
                         (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT/2))
        pygame.draw.rect(screen, (100, 100, 100),
                         (0, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT))

        # Game systems
        raycaster.castallrays()
        raycaster.render()
        gunmanager.update_player_damage()
        gunmanager.update_player_distance()
        sprite_handler.print_sprites()
        sprite_handler.hit()
        raycaster.render_objects(screen)
        gunmanager.update(screen)

        if player.update(map, screen):
            current_state = MENU
        # Check for escape to return to menu
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            current_state = MENU

    pygame.display.update()

pygame.quit()
