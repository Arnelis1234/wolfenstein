
import pygame
from constant import *

# -1-closed -2 open
class Map():
    def __init__(self):
        self.grid=[
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   ]
# grazina 1 arba 0 kuris yra tame indekse
    def position(self, x,y):
        tile_value=self.grid[int(y // TILESIZE)][int(x // TILESIZE)]
        if tile_value == -1:  # Closed door
            return 1  # Treat as a solid block
        elif tile_value == -2:  # Open door
            return 0  # Treat as empty space
        else:
            return tile_value   # Solid if not 0


    def get_tile(self, x, y):
        return [int(y // TILESIZE)][int(x // TILESIZE)]


    def render(self, screen):
        screen.fill((60,60,60))
        for i in range(10):
            for j in range(15):
                tilex=j*TILESIZE
                tiley=i*TILESIZE

                if self.grid[i][j]>0:
                    pygame.draw.rect(screen, (0,0,0),(tilex,tiley,TILESIZE-1,TILESIZE -1))
                elif self.grid[i][j] == -1:  # Closed door
                    pygame.draw.rect(screen, (139, 69, 19), (tilex + TILESIZE // 4, tiley, TILESIZE // 2, TILESIZE - 1))
                elif self.grid[i][j] == -2:  # Open door
                    pygame.draw.rect(screen, (210, 180, 140), (tilex + TILESIZE // 4, tiley, TILESIZE // 2, TILESIZE - 1))
               
               
                else:
                    pygame.draw.rect(screen, (255,255,255),(tilex,tiley,TILESIZE-1,TILESIZE -1))





    def toggle_door(self, x, y):
        grid_x = int(x // TILESIZE)
        grid_y = int(y // TILESIZE)
        if self.grid[grid_y][grid_x] == -1:  # Closed door
            self.grid[grid_y][grid_x] = -2  # Open it
        elif self.grid[grid_y][grid_x] == -2:  # Open door
            self.grid[grid_y][grid_x] = -1  # Close it