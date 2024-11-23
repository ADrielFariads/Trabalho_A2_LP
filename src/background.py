import pygame


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self,pos, size, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)



        