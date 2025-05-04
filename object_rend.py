import pygame
from constant import *


class ObjectRenderer:
    def __init__(self):

        self.texture_paths = {
            1: "python/wolfenstein/textures/1.png",
            2: "python/wolfenstein/textures/2.png",
            4: "python/wolfenstein/textures/3.png",
        }
        self.wall_textures = self.load_wall_textures()

    def load_wall_textures(self):
        textures = {}
        for texture_id, texture_path in self.texture_paths.items():
            textures[texture_id] = pygame.transform.scale(
                pygame.image.load(texture_path).convert_alpha(), (TILESIZE, TILESIZE))
        return textures

    def get_texture_path(self, texture_id):
        if texture_id == -2:
            return None
        return self.wall_textures.get(texture_id)
