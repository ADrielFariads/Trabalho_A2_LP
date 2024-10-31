import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, posx, posy, health, speed):
        super().__init__()
        #animation
        self.image = pygame.image.load("assets/images/testimage01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100)).convert_alpha()
        self.position = pygame.math.Vector2(posx, posy)
        self.rect = self.image.get_rect(center = (posx, posy))
        self.health_bar_lenght = 500

        #player atributes 
        self.speed = speed
        self.max_health = health
        self.current_health = self.max_health
        self.health_ratio = self.current_health/self.max_health
        
        
        
    def update(self, keys, screen_rect): #player moviment 
        direction = pygame.math.Vector2(0,0)

        if keys[pygame.K_a]:
            direction.x = -1
        if keys[pygame.K_d]:
            direction.x = 1
        if keys[pygame.K_w]:
            direction.y = -1
        if keys[pygame.K_s]:
            direction.y = 1

        if direction.length() > 0:
            direction = direction.normalize()

        self.position += direction * self.speed
        self.rect.center = self.position

        self.rect.clamp_ip(screen_rect)
        self.position = pygame.math.Vector2(self.rect.center)

    def get_damaged(self, damage):
        if self.current_health > 0:
            self.current_health -= damage

        if self.current_health <= 0:
            self.current_health = 0

    def get_healed(self, heal):
        if self.current_health < self.max_health:
            self.current_health += heal
        if self.current_health >= self.max_health:
            self.current_health = self.max_health

    def health_bar(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (10, 10, self.current_health/self.health_ratio, 15))
        pygame.draw.rect(surface, (255, 255, 255), (10, 10, self.health_bar_lenght, 15), 4)


        
