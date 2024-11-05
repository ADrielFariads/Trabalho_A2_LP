import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos_x, pos_y, image, health, speed, damage, range, player):
        super().__init__()
        #load image
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        
        #atributes
        self.max_health = health
        self.health = health
        self.speed = speed
        self.damage = damage
        self.range = range

        #player interaction
        self.target = player

    #fight logic
    def get_damaged(self, damage):
        self.health -= damage
    
    def get_healed(self, amount):
        if self.health <= self.max_health:
            self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def atack(self, target):
        target.get_damaged(self.damage)

    def player_distance(self):
        player_pos = pygame.math.Vector2(self.target.rect.center)
        current_pos = pygame.math.Vector2(self.rect.center)
        distance = current_pos.distance_to(player_pos)
        return distance

    def track_player(self):
        player_pos = pygame.math.Vector2(self.target.rect.center)
        current_pos = pygame.math.Vector2(self.rect.center)
        if player_pos != current_pos:
            self.direction = (player_pos - current_pos).normalize()
        else: self.direction = pygame.math.Vector2(0, 0)
        movement = self.direction * self.speed
        self.rect.center += movement

    

    def update(self):
        #checks the mob's death
        
        if self.health <= 0:
            self.kill()
            return None
        if self.player_distance() > self.range:
            self.track_player()
        else:
            self.atack(self.target)
