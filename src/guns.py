import pygame
import math

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
        self.bullet_class = bullet
        self.cool_down = cool_down
        self.last_shot_time = 0

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

    def shoot(self, bullet_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.cool_down:
            self.last_shot_time = current_time
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullet = self.bullet_class(self.rect.center, mouse_x, mouse_y, bullet_group)
            return bullet
        return None
        
    
class Bullet(pygame.sprite.Sprite):

    def __init__(self, position, target_x, target_y, group):
        super().__init__(group)
        self.image = pygame.Surface((5,5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=position)

        self.speed = 15

        self.dx = target_x - self.rect.centerx
        self.dy = target_y - self.rect.centery
        distance = math.sqrt(self.dx**2 + self.dy**2)

        if distance !=0:
            self.dx /= distance
            self.dy /= distance
    
    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if self.rect.x < 0 or self.rect.x > 1280 or self.rect.y < 0 or self.rect.y > 720:
            self.kill()



        