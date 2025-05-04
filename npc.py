import random
from sprites import *
from constant import *
from mapas import *
import math
import pygame
from ray import *
from ammo import *
from gun import Gunmanager


class NPC(AnimatedSprite):
    def __init__(self, player, raycaster, map, path, pos, scale, shift):
        super().__init__(player, raycaster, path, pos, scale, shift)
        self.shoot_images = self.get_images(
            "python/wolfenstein/sprite/npc/shoot")
        self.death_images = self.get_images(
            "python/wolfenstein/sprite/npc/death")
        self.stand_images = self.get_images(
            "python/wolfenstein/sprite/npc/stand")
        self.hurt_images = self.get_images(
            "python/wolfenstein/sprite/npc/hurt")
        self.walk_images = self.get_images(
            "python/wolfenstein/sprite/npc/walk")
        self.pain_animationtrigger = False
        self.alive = True
        self.indexspeed = 0.05
        self.health = 100
        self.pain = False
        self.map = map

        self.animation_0 = False
        self.animation_1 = False

        self.damage = 10

        self.raycaster = raycaster
        self.player = player
        self.cansee = False
        self.x = pos[0]
        self.y = pos[1]
        self.distance = 0

        self.is_facing_down = self.theta > 0 and self.theta < math.pi
        self.is_facing_up = not self.is_facing_down
        self.is_facing_right = self.theta < 0.5 * math.pi or self.theta > 1.5 * math.pi
        self.is_facing_left = not self.is_facing_right
        self.ammopickedup = False

    def check_hit_in_npc(self):
        if self.player._has_shot and WINDOW_WIDTH/2 - self.sprite_half_width < self.screen_x < WINDOW_HEIGHT + self.sprite_half_width:

            if self.cansee == True and self.distance <= self.player._gun_shoot_distance:
                self.health -= self.player._damage
                self.pain = True
                self.pain_animationtrigger = True
                self.animation_0 == False

            self.player._has_shot = False

    def health_check(self, object_handler):
        if self.health <= 0:
            self.alive = False
            if not self.ammopickedup:
                self.spawn_ammo(object_handler)
                self.ammopickedup = True
        else:
            self.alive = True

    def spawn_ammo(self, object_handler):
        # Create an ammo sprite at the NPC's position
        # print(self.x, self.y)
        ammo = Ammo(self.player, self.raycaster, (int(self.x), int(
            self.y)), "python/wolfenstein/sprite/ammo/ammo.png")
        object_handler.add_sprite(ammo)

    def damage_player(self):
        self.player._health -= self.damage
        # print(self.player._health)
        if self.player._health < 1:
            pygame.quit()
            exit()

    def update(self, object_handler):
        self.rajucaster()
        self.move()
        self.image = self.animate()
        self.health_check(object_handler)
        self.run()
        super().get_sprite()

    def run(self):

        if self.alive:

            self.check_hit_in_npc()

            if self.pain_animationtrigger == True and self.cansee == True:

                if self.animation_0 == False:
                    self.index = 0
                    # print("pain animation")
                    self.animation_0 = True

                self.indexspeed = 0.07
                self.array = self.hurt_images
                self.animate()
                if self.index >= 4:
                    self.pain_animationtrigger = False
                    self.animation_0 = False

            elif self.distance < 100 and self.cansee == True and self.pain_animationtrigger == False:
                if self.index >= 2.4:
                    self.index = 0
                    self.animation_1 = False
                self.indexspeed = 0.007
                self.array = self.shoot_images
                self.animate()
                if self.index >= 2 and self.animation_1 == False:
                    self.damage_player()
                    self.animation_1 = True

            elif self.cansee and self.distance > 100:
                if self.index >= 3.4:
                    self.index = 0

                self.indexspeed = 0.05
                self.array = self.walk_images
                self.animate()
        else:

            if self.animation_1 == False:
                self.player._score += 100
                self.animation_1 = True

            self.indexspeed = 0.07
            if self.index >= 4:

                self.indexspeed = 0

            self.array = self.death_images
            self.animate()

    def rajucaster(self):
        ray = Ray(self.theta, self.player, self.map)
        ray.cast()
        self.distance = math.sqrt(
            (self.x - self.player._x) ** 2 + (self.y - self.player._y) ** 2)
        if ray.distance < self.distance:
            self.cansee = False
        else:
            self.cansee = True

    def move(self):
        if self.cansee == True and self.alive == True and self.pain_animationtrigger == False:
            if self.distance > 100:
                dx = -math.cos(self.theta)
                dy = -math.sin(self.theta)
                self.x += dx
                self.y += dy

    def check_collision_with_player(self):

        if self.distance < 35:
            return True
        else:
            return False
