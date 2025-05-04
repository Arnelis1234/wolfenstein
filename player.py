import pygame
import math
from constant import *
from mapas import *
from menu import *
from highscore import *


class Player():
    def __init__(self, map):
        self._red = (255, 0, 0)
        self._radius = 8
        self._x = 80
        self._y = 80
        self._turn_direction = 0
        self._walk_direction = 0
        self._rotation_angle = 0*math.pi/180
        self._move_speed = 2.5
        self._rotation_speed = 2*math.pi/180

        self._map = map
        self._colision_x = False
        self._colision_x = False

        self._has_shot = False
        self._damage = 40
        self._reloading = False
        self._space_was_pressed = False

        # Initialize direction and plane
        self._dir_x = math.cos(self._rotation_angle)
        self._dir_y = math.sin(self._rotation_angle)
        self._plane_x = -self._dir_y * 0.66
        self._plane_y = self._dir_x * 0.66
        self._being_printed = False
        self._sprite_colision = False
        self._score = 0
        self._health = 100
        self._ammo = 15
        self._gun_shoot_distance = 1

    @property
    def rotation_angle(self):
        return self._rotation_angle

    @property
    def health(self):
        return self._health

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def ammo(self):
        return self._ammo

    @ammo.setter
    def ammo(self, value):
        self._ammo = value

    @property
    def has_shot(self):
        return self._has_shot

    @has_shot.setter
    def has_shot(self, value):
        self._has_shot = value

    @property
    def reloading(self):
        return self._reloading

    @reloading.setter
    def reloading(self, value):
        self._reloading = value

    def update_direction_and_plane(self):
        self._dir_x = math.cos(self._rotation_angle)
        self._dir_y = math.sin(self._rotation_angle)
        self._plane_x = -self._dir_y * 0.66
        self._plane_y = self._dir_x * 0.66

    def colision_with_wallforward(self):
        self._colision_x = False
        target_x = self._x+math.cos(self._rotation_angle)*self._radius
        target_y = self._y+math.sin(self._rotation_angle)*self._radius
        if self._map.position(target_x, target_y):
            return True
        else:
            False

    def colision_with_wallbackward(self):
        self._colision_y = False
        target_x = self._x-math.cos(self._rotation_angle)*self._radius
        target_y = self._y-math.sin(self._rotation_angle)*self._radius
        if self._map.position(target_x, target_y):
            return True
        else:
            False

    def update(self, map, screen):
        keys = pygame.key.get_pressed()
        self._turn_direction = 0
        self._walk_direction = 0

        if keys[pygame.K_ESCAPE]:
            pygame.quit()

        if keys[pygame.K_d]:
            self._turn_direction = 1
        if keys[pygame.K_a]:
            self._turn_direction = -1
        if keys[pygame.K_w]:

            self._walk_direction = 1
            if self._sprite_colision or self.colision_with_wallforward():
                self._walk_direction = 0

        if keys[pygame.K_s]:
            self._walk_direction = -1
            if self.colision_with_wallbackward():
                self._walk_direction = 0

        if keys[pygame.K_e]:
            if map.win_condition(self):
                write_highscore(self._score)
                current_state = 0
                return True
            return False

        if keys[pygame.K_SPACE] and not self._reloading and not self._space_was_pressed:
            if self._ammo > 0:
                self._ammo -= 1
            self._has_shot = True
            self._reloading = True
            # print("self.has_shot")
            self._space_was_pressed = True

        if not keys[pygame.K_SPACE]:
            self._space_was_pressed = False

        movestep = self._walk_direction*self._move_speed
        self._rotation_angle += self._turn_direction*self._rotation_speed
        self._x += math.cos(self._rotation_angle)*movestep
        self._y += math.sin(self._rotation_angle)*movestep
        self.update_direction_and_plane()
        self.draw_ui(screen)

    def draw_ui(self, screen):

        font = pygame.font.SysFont('arial', 36)

        # Render the score text
        score_text = font.render(
            f"Score:{self._score}", False, (255, 255, 255))
        ammo_text = font.render(f"Ammo:{self._ammo}", False, (255, 255, 255))
        health_text = font.render(
            f"Health:{self._health}", False, (255, 255, 255))
        # Blit the text onto the screen
        pygame.draw.rect(screen, (0, 0, 255),
                         (0, WINDOW_HEIGHT-50, 500, WINDOW_HEIGHT))
        screen.blit(score_text, (10, WINDOW_HEIGHT-50))
        screen.blit(ammo_text, (150, WINDOW_HEIGHT-50))
        screen.blit(health_text, (300, WINDOW_HEIGHT-50))
