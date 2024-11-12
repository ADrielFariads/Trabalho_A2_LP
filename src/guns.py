import pygame
import math

import pygame
import math

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, image, damage, cool_down, bullet, *groups):
        super().__init__(*groups)
        self.player = player
        self.image = pygame.image.load(image).convert_alpha()
        self.original_image = self.image.copy()
        
        # Redimensionar a imagem da arma
        self.scale_factor = 1.5  # Fator de escala para aumentar o tamanho
        self.original_image = pygame.transform.scale(
            self.original_image,
            (int(self.original_image.get_width() * self.scale_factor), int(self.original_image.get_height() * self.scale_factor))
        )
        
        self.rect = self.image.get_rect(center=self.player.get_position())
        self.damage = damage
        self.cool_down = cool_down
        self.bullet_class = bullet
        self.last_shot_time = 0

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.center = self.player.get_position()
        angle = math.degrees(math.atan2(mouse_pos[1] - self.rect.centery, mouse_pos[0] - self.rect.centerx))
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

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

        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=position)

        self.speed = 15

        self.dx = target_x - self.rect.centerx
        self.dy = target_y - self.rect.centery
        distance = math.sqrt(self.dx ** 2 + self.dy ** 2)

        if distance != 0:
            self.dx /= distance
            self.dy /= distance

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if self.rect.x < 0 or self.rect.x > 1280 or self.rect.y < 0 or self.rect.y > 720:
            self.kill()
