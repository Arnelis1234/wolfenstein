import pygame
from constant import *
from sprites import AnimatedSprite


class Knife(AnimatedSprite):
    def __init__(self, player, raycaster, path="python/wolfenstein/sprite/knife/knife.png", pos=(100, 100), scale=50):
        super().__init__(player=player, raycaster=raycaster, path=path)

        self.scale = 10
        self.x = HALF_WIDTH-(self.scale*64/2)
        self.y = WINDOW_HEIGHT-(self.scale*64)

        self.name = "knife"
        self.damage = 10
        self.a = 0
        self.hurt_distance = 40

    def checkif_shot(self):
        if self.player._has_shot:
            self.player._reloading = True

    def reload(self, screen):  # self.image=pygame.image.load(self.path).convert_alpha()
        # self.checkif_shot()
        # if self.player.reloading==True:

        if self.player._reloading == True:

            self.a += 0.15
            if self.a >= len(self.array):
                self.player._has_shot = False
                self.player._reloading = False
                self.a = 0
            img = pygame.image.load(self.array[int(self.a)]).convert_alpha()
            scaled_img = pygame.transform.scale(
                img, (img.get_width()*self.scale, img.get_height()*self.scale))
            screen.blit(scaled_img, (self.x, self.y))

        else:
            first = pygame.image.load(self.array[0]).convert_alpha()
            scaled_first = pygame.transform.scale(
                first, (first.get_width()*self.scale, first.get_height()*self.scale))

            screen.blit(scaled_first, (self.x, self.y))

    def update(self, screen):
        self.reload(screen)


class Gun(AnimatedSprite):
    def __init__(self, player, raycaster, path="python/wolfenstein/sprite/gun/1.png", pos=(100, 100), scale=50):
        super().__init__(player=player, raycaster=raycaster, path=path)

        self.scale = 3
        self.x = WINDOW_WIDTH/2-self.scale*192/2
        self.y = WINDOW_HEIGHT-self.scale*192
        self.name = "gun"
        self.damage = 40
        self.hurt_distance = 999
        self.a = 0

    def checkif_shot(self):
        if self.player._has_shot:
            self.player._reloading = True

    def reload(self, screen):

        if self.player._reloading == True:

            self.a += 0.15
            if self.a >= len(self.array):
                self.player._has_shot = False
                self.player._reloading = False
                self.a = 0
            img = pygame.image.load(self.array[int(self.a)]).convert_alpha()
            scaled_img = pygame.transform.scale(
                img, (img.get_width()*self.scale, img.get_height()*self.scale))
            screen.blit(scaled_img, (self.x, self.y))

        else:
            first = pygame.image.load(self.array[0]).convert_alpha()
            scaled_first = pygame.transform.scale(
                first, (first.get_width()*self.scale, first.get_height()*self.scale))

            screen.blit(scaled_first, (self.x, self.y))

    def update(self, screen):
        self.reload(screen)


class Gunmanager():
    def __init__(self, player, raycaster):
        self.player = player
        self.current_weapon_index = 1
        self.weapons = [Knife(player, raycaster), Gun(player, raycaster)]

    def update(self, screen):
        current_weapon = self.weapons[self.current_weapon_index]
        if self.player._ammo > 0:
            self.current_weapon_index = 1
        # If the current weapon is the gun and ammo is 0, check if it's reloading
        if isinstance(current_weapon, Gun) and self.player._ammo == 0:
            if self.player._reloading:  # Continue updating the gun until reload is complete
                current_weapon.update(screen)
            else:
                self.current_weapon_index = 0  # Switch to the knife after reload is complete
        else:

            current_weapon.update(screen)

    def get_current_weapon(self):
        return self.weapons[self.current_weapon_index]

    def update_player_damage(self):
        current_weapon = self.get_current_weapon()
        self.player._damage = current_weapon.damage

    def update_player_distance(self):
        current_weapon = self.get_current_weapon()
        self.player._gun_shoot_distance = current_weapon.hurt_distance
