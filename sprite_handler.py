from sprites import *
from npc import *
from factory import *
# from ammo import *


class ObjectHandler:
    def __init__(self, player, raycaster, map):
        self.player = player
        self.raycaster = raycaster
        self.map = map
        self.if_hit_npc = []
        self.sprite_list = []
        self.npc_list = []
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        add_sprite(SpriteObject(player, raycaster,path='python/wolfenstein/sprite/light1.png',
                 pos=(368, 240)))
        add_sprite(SpriteObject(player, raycaster,path='python/wolfenstein/sprite/light1.png',
                 pos=(240, 240)))
        add_sprite(Gold(player, raycaster, (48, 208)))
        add_sprite(Gold(player, raycaster, (48, 240)))
        add_sprite(Gold(player, raycaster, (80, 208)))
        add_sprite(Gold(player, raycaster, (80, 240)))

        add_npc(NPCFactory.create_npc(
            "soldier", player, raycaster, map, (304, 144)))
        add_npc(NPCFactory.create_npc(
            "soldier", player, raycaster, map, (368, 112)))
        add_npc(NPCFactory.create_npc(
            "officer", player, raycaster, map, (400, 208)))
        add_npc(NPCFactory.create_npc(
            "officer", player, raycaster, map, (272, 240)))

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def print_sprites(self):
        # print("sprite_list:", self.sprite_list)
        # print("npc_list:", self.npc_list)
        for sprite in self.sprite_list:
            sprite.check_pickup()
            sprite.update()

        for npc in self.npc_list:

            npc.update(self)
            if npc.alive:
                self.if_hit_npc.append(npc.check_collision_with_player())

    def hit(self):

        if not any(self.if_hit_npc):
            self.player._sprite_colision = False
        else:
            self.player._sprite_colision = True
        if len(self.if_hit_npc) > 4:
            self.if_hit_npc.clear()
