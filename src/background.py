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
    
    def draw(self):
        # Draw all tiles on the screen
        self.screen.fill((30, 30, 30))
        self.sprite_group.draw(self.screen)

if __name__ == "__main__":
    window_width, window_height = 940, 640
    screen = pygame.display.set_mode((window_width, window_height))

    background = Background(map_path="assets\\background_files\\map001.tmx", tile_size=16, screen=screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        background.draw()
        
        pygame.display.update()