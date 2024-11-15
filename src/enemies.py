"""
Module for enemies creation and enemies generation

"""


import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_sheet, frames_x, frames_y, health, speed, damage, attack_range, attack_delay, player, bullets_group):
        super().__init__()

        #loading image
        self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()

        frames_x_axis = frames_x #frames in sprite sheet
        frames_y_axis = frames_y
        frame_width = self.sprite_sheet.get_width() // frames_x_axis
        frame_height = self.sprite_sheet.get_height() // frames_y

        self.frames = []
        for y in range(frames_y_axis):
            for x in range(frames_x_axis):
                frame = self.sprite_sheet.subsurface((x * frame_width, y * frame_height, frame_width, frame_height))
                redimentioned_frame = pygame.transform.scale(frame, (int(frame_width), int(frame_height)))
                self.frames.append(redimentioned_frame)

        #initial frame setting
        self.current_frame_index = 0
        self.animation_speed = 10 #bigger values for a smothier animation
        self.frame_counter = 0 #counter of animation

        self.x = pos[0]
        self.y = pos[1]
        self.position = pygame.math.Vector2(self.x, self.y)
        self.image = self.frames[self.current_frame_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))


        
        #atributes
        self.max_health = health
        self.health = health
        self.speed = speed
        self.damage = damage
        self.attack_range = attack_range
        self.attack_delay = attack_delay
        self.attack_counter = 50 #time between attacks

        #player interaction
        self.target = player
        self.bullets = bullets_group

    def animate(self):
        # Increment frame counter and update frame index
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.image = self.frames[self.current_frame_index]
            self.frame_counter = 0

    #fight logic
    def get_damaged(self, damage):
        self.health -= damage
    
    def get_healed(self, amount):
        if self.health <= self.max_health:
            self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def attack(self, target):
        target.get_damaged(self.damage)

    def player_distance(self):
        player_pos = pygame.math.Vector2(self.target.rect.center)
        current_pos = pygame.math.Vector2(self.rect.center)
        distance = current_pos.distance_to(player_pos)
        return distance


    #
    def track_player(self):
        player_pos = pygame.math.Vector2(self.target.rect.center)
        current_pos = pygame.math.Vector2(self.rect.center)
        if player_pos != current_pos:
            self.direction = (player_pos - current_pos).normalize()
        else: self.direction = pygame.math.Vector2(0, 0)
        movement = self.direction * self.speed
        self.rect.center += movement

    def behavior(self):
        pass

    def update(self):
        #checks the mob's death
        
        if self.health <= 0:
            self.kill()
            return None
        
        if pygame.sprite.spritecollide(self, self.bullets, True):
            self.get_damaged(10)

        self.behavior()
        


        #animation logic
        self.animate()


class Goblin(Enemy):
    def __init__(self, pos, player, bullets_group):

        self.sprite_sheet = "assets\\images\\enemies\\goblins\\goblin_front_view.png"
        self.frames_x = 11
        self.frames_y = 1
        self.health = 50
        self.speed = 4
        self.damage = 100
        self.attack_delay = 50
        self.attack_range = 50
        super().__init__(pos, self.sprite_sheet, self.frames_x,self.frames_y, self.health,  self.speed, self.damage, self.attack_range, self.attack_delay, player, bullets_group)

    def behavior(self):
        if self.player_distance() > self.attack_range:
            self.track_player()
        else:
            if self.attack_counter >= self.attack_delay:
                self.attack(self.target)
                self.attack_counter = 0
        self.attack_counter += 1 





def generate_goblins(num_goblins, map_width, map_height, player, bullets_group, goblins_group):
    for _ in range(num_goblins):
        # Gerar uma posição aleatória dentro dos limites do mapa
        random_x = random.randint(0, map_width)
        random_y = random.randint(0, map_height)

        # Criar um novo goblin na posição aleatória
        goblin = Goblin((random_x, random_y), player, bullets_group)

        # Adicionar o goblin ao grupo de inimigos existente
        goblins_group.add(goblin)


class Andromaluis(Enemy):
    def __init__(self, pos,player, bullets_group, enemy_group):

        self.sprite_sheet = "assets\\images\\enemies\\andromaluis\\andromalius.png"
        self.frames_x = 8
        self.frames_y = 3
        self.health = 500
        self.speed = 1
        self.damage = 100
        self.attack_delay = 1000
        self.attack_range = 500
        self.enemy_group = enemy_group
        super().__init__(pos, self.sprite_sheet, self.frames_x, self.frames_y, self.health, self.speed, self.damage, self.attack_range, self.attack_delay, player, bullets_group)

    def get_damaged(self, damage):
        generate_goblins(1, 1000, 1000, self.target, self.bullets, self.enemy_group)
        return super().get_damaged(damage)
        