import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, posx, posy, health, speed):
        super().__init__()

        self.position = pygame.math.Vector2(posx, posy)
        self.rect = self.image.get_rect(center = (posx, posy))
        self.speed = speed
        self.health = health
        
    def update(self, keys): #player moviment 
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

