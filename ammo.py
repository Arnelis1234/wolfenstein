from sprites import SpriteObject
import pygame


import os
from abc import ABC, abstractmethod


class weapon(ABC):
    @abstractmethod
    def dothing(self):
        pass


class Ammo(SpriteObject, weapon):
    def __init__(self, player, raycaster, pos=(200, 200), path="python/wolfenstein/sprite/ammo/ammo.png", scale=4, shift=4):
        resolved_path = os.path.abspath(path)
        super().__init__(player, raycaster, resolved_path, pos=pos, scale=scale, shift=shift)
        self.is_pickupable = True

    def dothing(self):
        self.player._ammo += 5


class Gold(SpriteObject, weapon):
    def __init__(self, player, raycaster, pos=(250, 200), path="python/wolfenstein/sprite/gold/gold.png", scale=30, shift=0.05):
        super().__init__(player, raycaster, path, pos, scale=scale, shift=shift)
        self.is_pickupable = True

    def dothing(self):
        self.player._score += 500
