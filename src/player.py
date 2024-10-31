import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, posx, posy, health, speed):
        super().__init__()
        #animation
        self.image = pygame.image.load("assets/images/testimage01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50)).convert_alpha()
        self.position = pygame.math.Vector2(posx, posy)
        self.rect = self.image.get_rect(center = (posx, posy))

        #player atributes 
        self.speed = speed
        self.health = health
        
        
    def update(self, keys): #player moviment 
        direction = pygame.math.Vector2(0,0)

        if keys[pygame.K_a]:
            direction = -1
        if keys[pygame.K_d]:
            direction = 1
        if keys[pygame.K_w]:
            direction = -1
        if keys[pygame.K_s]:
            direction = 1

        if direction.length() > 0:
            direction = direction.normalize()

        self.position += direction * self.speed
        self.rect.center = self.position

        
