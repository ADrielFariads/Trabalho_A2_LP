import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, posx, posy, health, speed):
        super().__init__()
        #animation
        #loads the image
        self.image = pygame.image.load("assets/images/Player/Idle1.png").convert_alpha()
        
        self.position = pygame.math.Vector2(posx, posy)
        self.rect = self.image.get_rect(center = (posx, posy))
        self.health_bar_lenght = 500
        self.health_change_speed = 1
        self.target_health = health

        #player atributes 
        self.speed = speed
        self.max_health = health
        self.current_health = self.max_health
        self.health_ratio = self.current_health/self.health_bar_lenght
        
        
        
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
        if self.target_health > 0:
            self.target_health -= damage

        if self.target_health <= 0:
            self.target_health = 0

    def get_healed(self, heal):
        if self.target_health < self.max_health:
            self.target_health += heal

        if self.target_health >= self.max_health:
            self.target_health = self.max_health

    def health_bar(self, surface):
        transition_width = 0
        transition_color = (255, 255, 255)
        
        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health-self.current_health)/self.health_ratio)
            transition_color = (0, 255, 0)
        
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health-self.current_health)/self.health_ratio)
            transition_color = (255, 255, 0)      

        health_bar_rect = pygame.Rect(10, 10, self.current_health/self.health_ratio, 15)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, 10, transition_width, 15)

        pygame.draw.rect(surface, (255, 0, 0), health_bar_rect)
        pygame.draw.rect(surface, transition_color, transition_bar_rect)
        pygame.draw.rect(surface, (255, 255, 255), (10, 10, self.health_bar_lenght, 15), 4)
        
        
