import pygame
import math
from npc import NPC


class NPCFactory:
    @staticmethod
    def create_npc(npc_type, player, raycaster, map, pos):
        if npc_type == "soldier":
            return SoldierNPC(player, raycaster, map, "python/wolfenstein/sprite/npc/stand1.png", pos)
        elif npc_type == "officer":
            return OfficerNPC(player, raycaster, map, "python/wolfenstein/sprite/npc/officer/stand/stand.png", pos)

        else:
            raise ValueError(f"Unknown NPC type: {npc_type}")


class SoldierNPC(NPC):
    def __init__(self, player, raycaster, map, path, pos, scale=30, shift=0.01):
        super().__init__(player, raycaster, map, path, pos, scale, shift)


class OfficerNPC(NPC):
    def __init__(self, player, raycaster, map, path, pos, scale=30, shift=0.1):
        super().__init__(player, raycaster, map, path, pos, scale, shift)

        self.health = 200
        self.damage = 20
        self.shoot_images = self.get_images(
            "python/wolfenstein/sprite/npc/officer/shoot")
        self.death_images = self.get_images(
            "python/wolfenstein/sprite/npc/officer/death")
        self.stand_images = self.get_images(
            "python/wolfenstein/sprite/npc/officer/stand")
        self.hurt_images = self.get_images(
            "python/wolfenstein/sprite/npc/officer/hurt")
        self.walk_images = self.get_images(
            "python/wolfenstein/sprite/npc/officer/walk")
