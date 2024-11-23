import pygame
from guns import Gun
import config

class AllSpritesgroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset.update(-(target_pos[0] - 600), -(target_pos[1] - 350))    
        for sprite in self:
            if hasattr(sprite, "image"):
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)