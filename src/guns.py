import pygame

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, image, damage, cool_down, bullet, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.image.load(image).convert_alpha()
        self.player = player
        self.rect = self.image.get_rect(center=self.player.get_position())
        self.position = self.player.get_position()
        self.base_damage = damage
        self.bullet = bullet
        self.cool_down = cool_down

    def update_position(self):
        self.position = self.player.get_position()
        self.rect.center = (self.position[0], self.position[1]+10)

    def update(self):
        self.update_position()
    

        
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
