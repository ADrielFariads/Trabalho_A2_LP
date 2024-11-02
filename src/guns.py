import pygame

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, image, damage, cool_down, bullet, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(image).convert_alpha()
        self.player = player
        #formating image
        self.image_width, self.image_height = self.image.get_size()
        self.original_image = pygame.transform.scale(self.image, (self.image_width * 2, self.image_height * 2))
        
        self.position = self.player.get_position()
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.player.get_position())

        self.base_damage = damage
        self.bullet = bullet
        self.cool_down = cool_down

    def update_position(self):
        self.position = self.player.get_position()
        self.rect.center = (self.position[0]-10, self.position[1]+15)

    def update(self):
        self.update_position()
        if self.player.facing_right:
            self.image = self.original_image
            self.rect.center = (self.position[0]-10, self.position[1]+15)
        else:
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.rect.center = (self.position[0], self.position[1]+15)

        
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
