import pygame

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, image, damage, cool_down, bullet, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.player = player
        self.position = self.player.get_position()
        self.base_damage = damage
        self.bullet = bullet
        self.cool_down = cool_down

    def update_position(self):
        self.position = self.player.get_position()

    def update(self):
        self.update_position()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        

        
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
