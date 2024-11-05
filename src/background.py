import pygame
import sys
from pytmx.util_pygame import load_pygame

pygame.init()

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

class Background:
    def __init__(self, map_path, tile_size, screen):
        self.map_path = map_path
        self.tile_size = tile_size
        self.screen = screen
        self.sprite_group = pygame.sprite.Group()
        self.collision_obj = []
        
        # Load the map and set up tiles and collision objects
        self.load_map()

    def load_map(self):
        tmx_data = load_pygame(self.map_path)
        
        # Load tile layers
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * self.tile_size, y * self.tile_size)
                    Tile(pos=pos, image=surf, groups=self.sprite_group)
        
        # Load collision objects
        for obj in tmx_data.objects:
               if obj.type == "limiters":
                 rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                 self.collision_obj.append(rect)
    
    def draw(self, camera):
        # Draw all tiles on the screen
        self.sprite_group.draw(self.screen)

        #using camera logic
        for tile in self.sprite_group:
            # Aply camera to the tiles
            self.screen.blit(tile.image, camera.apply(tile))
