
import pygame
from constant import *


class Map():
    def __init__(self):
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
    def position(self, x, y):
        tile_value = self.grid[int(y // TILESIZE)][int(x // TILESIZE)]

        return tile_value   # Solid if not 0

    def render(self, screen):
        screen.fill((60, 60, 60))
        for i in range(10):
            for j in range(15):
                tilex = j*TILESIZE
                tiley = i*TILESIZE

                if self.grid[i][j] > 0:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (tilex, tiley, TILESIZE-1, TILESIZE - 1))
                elif self.grid[i][j] == -1:  # Closed door
                    pygame.draw.rect(
                        screen, (139, 69, 19), (tilex + TILESIZE // 4, tiley, TILESIZE // 2, TILESIZE - 1))
                elif self.grid[i][j] == -2:  # Open door
                    pygame.draw.rect(
                        screen, (210, 180, 140), (tilex + TILESIZE // 4, tiley, TILESIZE // 2, TILESIZE - 1))

                else:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (tilex, tiley, TILESIZE-1, TILESIZE - 1))

    def win_condition(self, player):
        # Calculate the tile the player is facing
        target_x = player._x + math.cos(player._rotation_angle) * TILESIZE // 2
        target_y = player._y + math.sin(player._rotation_angle) * TILESIZE // 2

        # Get the tile value
        tile_value = self.grid[int(target_y // TILESIZE)
                               ][int(target_x // TILESIZE)]

        # Check if the tile is the win wall
        if tile_value == 4:
            # print("You win!")
            return True
        return False
