import pygame
from pytmx.util_pygame import load_pygame

pygame.init()

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self,pos, size, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)

class PlantSprite(pygame.sprite.Sprite):
    def __init__(self, image, pos, width, height, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = pygame.rect.Rect(pos[0], pos[1], width, height).inflate(-80, -80)
        self.rect.center = (pos[0], pos[1])

class Background:
    def __init__(self, map_path, tile_size, screen):
        self.map_path = map_path
        self.tile_size = tile_size
        self.screen = screen
        self.ground_group = pygame.sprite.Group()
        self.collision_group = pygame.sprite.Group()
        
        # Load the map and set up tiles and collision objects
        self.load_map()

    def load_map(self):
        self.tmx_data = load_pygame(self.map_path)
        
        # Load tile layers
        # for layer in self.tmx_data.visible_layers:
        #     if hasattr(layer, 'data'):
        #         for x, y, surf in layer.tiles():
        #             pos = (x * self.tile_size, y * self.tile_size)
        #             Tile(pos=pos, image=surf, groups=self.ground_group)
        
        #load objects
        for obj in self.tmx_data.objects:
            if obj.type == "plants":
                self.collision_group.add(PlantSprite(obj.image, (obj.x, obj.y), obj.width, obj.height))



        