import pygame
from constant import *
from ray import *
from object_rend import *


class Raycaster:
    def __init__(self, player, map, object_renderer):
        self.depth_buffer = [0] * NUM_RAYS
        self.rays = []
        self.player = player
        self.map = map
        self.texture = None
        self.object_renderer = object_renderer

        self.objects_to_render = []

    def castallrays(self):
        self.rays = []
        self.depth_buffer = []
        rayangle = self.player._rotation_angle-FOV/2
        for i in range(NUM_RAYS):
            ray = Ray(rayangle, self.player, self.map)
            ray.cast()
            self.rays.append(ray)
            self.depth_buffer.append(ray.distance)
            rayangle += FOV/NUM_RAYS

    def render(self):

        i = 0
        for ray in self.rays:
            # ray.render(screen)
            ray.distance = max(ray.distance, 10)
            self.texture = self.object_renderer.get_texture_path(ray.map_tile)

            wall_column = self.texture.subsurface(
                ray.offset % TILESIZE, 0, 1, TILESIZE)
            wall_column = pygame.transform.scale(
                wall_column, (SCALE, int(PROJ_COEFF / ray.distance)))
            pos = (i * SCALE, HALF_HEIGHT - wall_column.get_height() // 2)
            self.objects_to_render.append((ray.distance, wall_column, pos))

            i += 1

    def render_objects(self, screen):
        for distance, wall_column, pos in sorted(self.objects_to_render, key=lambda t: t[0], reverse=True):
            screen.blit(wall_column, pos)
        self.objects_to_render.clear()
