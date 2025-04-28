from sprites import *
from npc import *
class ObjectHandler:
    def __init__(self,player,raycaster,map ):
        self.player = player
        self.raycaster = raycaster
        self.map = map
        self.sprite_list = []
        self.npc_list = []
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        add_sprite(SpriteObject(player,raycaster))
        # add_sprite(AnimatedSprite(player,raycaster,"python/wolfenstein/sprite/animated/anim1.png",(250,200)))
        # add_sprite(SpriteObject(player,raycaster,'python/wolfenstein/sprite/barrel.png',(350,200),20))
        # add_sprite(AnimatedSprite(player,raycaster))

        add_npc(NPC(player,raycaster,map))
        add_npc(NPC(player,raycaster,map,"python/wolfenstein/sprite/npc/stand1.png",(200,200)))
    def add_sprite(self, sprite):
            self.sprite_list.append(sprite)

    def add_npc(self, npc):
            self.npc_list.append(npc)
    def print_sprites(self):
        for sprite in self.sprite_list:
            sprite.update()

        for npc in self.npc_list:
            npc.update()        