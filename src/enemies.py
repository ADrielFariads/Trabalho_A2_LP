"""
This module handles the creation and management of enemies. It provides classes for various enemy types, each with unique behaviors and attributes, as well as functions for dynamically spawning enemies on the map.

"""


import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_sheet, frames_x, frames_y, health, speed, damage, attack_range, attack_delay, player, bullets_group, colliders=None):
        super().__init__()

        # Loading image
        self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()

        self.frames_x = frames_x
        self.frames_y = frames_y

        # Load frames
        self.load_frames()

        # Initial frame setting
        self.current_frame_index = 0
        self.animation_speed = 10  # Bigger values for a smoother animation
        self.frame_counter = 0  # Counter of animation

        self.x = pos[0]
        self.y = pos[1]
        self.position = pygame.math.Vector2(self.x, self.y)
        self.image = self.frames[self.current_frame_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Attributes
        self.max_health = health
        self.health = health
        self.speed = speed
        self.damage = damage
        self.attack_range = attack_range
        self.attack_delay = attack_delay
        self.attack_counter = 50  # Time between attacks

        # Player interaction
        self.target = player
        self.bullets = bullets_group
        self.experience_given = 10
        self.colliders = colliders

    def load_frames(self):
        frame_width = self.sprite_sheet.get_width() // self.frames_x
        frame_height = self.sprite_sheet.get_height() // self.frames_y

        self.frames = []
        for y in range(self.frames_y):
            for x in range(self.frames_x):
                frame = self.sprite_sheet.subsurface((x * frame_width, y * frame_height, frame_width, frame_height))
                redimensioned_frame = pygame.transform.scale(frame, (int(frame_width), int(frame_height)))
                self.frames.append(redimensioned_frame)

        self.divided_frames = [self.frames[i:i+self.frames_x] for i in range(0, len(self.frames), self.frames_x)]

    def animate(self):
        # Increment frame counter and update frame index
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.image = self.frames[self.current_frame_index]
            self.frame_counter = 0

    # Fight logic
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

    def track_player(self):
        player_pos = pygame.math.Vector2(self.target.rect.center)
        current_pos = pygame.math.Vector2(self.rect.center)
        if player_pos != current_pos:
            self.direction = (player_pos - current_pos).normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)
        movement = self.direction * self.speed
        self.rect.center += movement

    def behavior(self):
        pass
    def collision(self, direction):
        if self.colliders != None:
            for sprite in self.colliders:
                if sprite.rect.colliderect(self.rect):
                    if direction == "horizontal":
                        if self.direction.x > 0:
                            self.rect.right = sprite.rect.left

                        if self.direction.x < 0:
                            self.rect.left = sprite.rect.right

                    if direction == "vertical":
                        if self.direction.y > 0:
                            self.rect.bottom = sprite.rect.top

                        if self.direction.y < 0:
                            self.rect.top = sprite.rect.bottom


    def update(self):
        # Checks the mob's death
        if self.health <= 0:
            self.target.experience += self.damage
            self.kill()
            return None
        
        collided_bullets = pygame.sprite.spritecollide(self, self.bullets, True)
        for bullet in collided_bullets:
            self.get_damaged(bullet.damage)

        self.behavior()

        # Animation logic
        self.animate()

class Goblin(Enemy):
    def __init__(self, pos, player, bullets_group):
        # Initialize the sprite sheet and animation parameters
        self.sprite_sheet = "assets\\images\\enemies\\goblins\\goblin.png"
        self.frames_x = 11  # colums
        self.frames_y = 4  # lines
        self.health = 50
        self.speed = random.uniform(2, 6)  # Random speed for each goblin
        self.damage = 100
        self.attack_delay = 50
        self.attack_range = 50
        self.experience_given = 30
        super().__init__(pos, self.sprite_sheet, self.frames_x, self.frames_y, self.health, self.speed, self.damage, self.attack_range, self.attack_delay, player, bullets_group)
        self.attack_counter = 0
        self.direction = pygame.math.Vector2(0, 0)  # Initialize direction

    def load_frames(self):
        # Calculate frame dimensions
        frame_width = self.sprite_sheet.get_width() // self.frames_x
        frame_height = self.sprite_sheet.get_height() // self.frames_y

        self.frames = []
        for y in range(self.frames_y):
            for x in range(self.frames_x):
                # Extract each frame from the sprite sheet
                frame = self.sprite_sheet.subsurface((x * frame_width, y * frame_height, frame_width, frame_height))
                redimensioned_frame = pygame.transform.scale(frame, (int(frame_width), int(frame_height)))
                self.frames.append(redimensioned_frame)

        # Divide frames into sublists for each direction
        self.divided_frames = [self.frames[i:i+self.frames_x] for i in range(0, len(self.frames), self.frames_x)]

    def behavior(self):
        if self.player_distance() > self.attack_range:
            # Calculate direction towards the player
            direction = pygame.math.Vector2(self.target.rect.center) - pygame.math.Vector2(self.rect.center)
            if direction.length() > 0:
                direction = direction.normalize()
            
            # Add a small random variation to the direction
            randomness = pygame.math.Vector2(random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2))
            direction += randomness
            direction = direction.normalize()

            # Move the goblin in the calculated direction
            self.position += direction * self.speed * 0.5
            self.rect.center = self.position

            # Update frames based on movement direction
            if direction.x > 0 and abs(direction.x) >= abs(direction.y):
                self.frames = self.divided_frames[1]  # Moving right
            elif direction.x < 0 and abs(direction.x) >= abs(direction.y):
                self.frames = self.divided_frames[3]  # Moving left
            elif direction.y < 0 and abs(direction.y) > abs(direction.x):
                self.frames = self.divided_frames[2]  # Moving up
            elif direction.y > 0 and abs(direction.y) > abs(direction.x):
                self.frames = self.divided_frames[0]  # Moving down

            # Update the direction attribute
            self.direction = direction
        else:
            if self.attack_counter >= self.attack_delay:
                # Attack the player if within range
                self.attack(self.target)
                self.attack_counter = 0
        self.attack_counter += 1



def generate_goblins(num_goblins, top, bottom, left, right, player, bullets_group, goblins_group):
    for _ in range(num_goblins):
        # Generate a random position within the map boundaries
        random_x = random.randint(left, right)
        random_y = random.randint(top, bottom)

        # Add a random variation to the initial position
        random_x += random.randint(-50, 50)
        random_y += random.randint(-50, 50)

        # Create a new goblin at the random position with a random speed
        goblin = Goblin((random_x, random_y), player, bullets_group)
        goblin.speed = random.uniform(5, 10)  # Speed range between 5 and 10

        # Add the goblin to the existing group of enemies
        goblins_group.add(goblin)

class Andromaluis(Enemy):
    def __init__(self, pos,player, bullets_group, enemy_group):

        self.sprite_sheet = "assets\\images\\enemies\\andromaluis\\andromalius.png"
        self.frames_x = 8
        self.frames_y = 3
        self.health = 5000
        self.speed = 1
        self.damage = 100
        self.attack_delay = 1000
        self.attack_range = 500
        self.enemy_group = enemy_group
        self.experience_given = 100

        #skill atributes
        self.generation_interval = 500
        self.generation_timer = 10
        super().__init__(pos, self.sprite_sheet, self.frames_x, self.frames_y, self.health, self.speed, self.damage, self.attack_range, self.attack_delay, player, bullets_group)



    def behavior(self):
        distance_to_enemy = self.target.position - self.position

        if distance_to_enemy.length() < 200:
            if self.generation_timer <= 0:
                generate_goblins(4, self.rect.top, self.rect.bottom, self.rect.left, self.rect.right, self.target, self.bullets, self.enemy_group)
                self.generation_timer = self.generation_interval
        else:
            self.generation_timer -= 1


class Centipede(Enemy):
    def __init__(self, pos, player, bullets_group):
        self.sprite_sheet = "assets\\images\\enemies\\Centipeder\\Centipede_walk.png"
        self.frames_x = 4
        self.frames_y = 1
        self.health = 50
        self.speed = 3
        self.damage = 40
        self.attack_delay = 50
        self.attack_range = 50

        super().__init__(pos, self.sprite_sheet, self.frames_x, self.frames_y, self.health, self.speed, self.damage, self.attack_range, self.attack_delay, player, bullets_group)

    def load_frames(self):
        frame_width = self.sprite_sheet.get_width() // self.frames_x
        frame_height = self.sprite_sheet.get_height() // self.frames_y

        self.frames = []
        for y in range(self.frames_y):
            for x in range(self.frames_x):
                frame = self.sprite_sheet.subsurface((x * frame_width, y * frame_height, frame_width, frame_height))
                redimensioned_frame = pygame.transform.scale(frame, (int(frame_width), int(frame_height)))
                self.frames.append(redimensioned_frame)

        self.divided_frames = [self.frames[i:i+self.frames_x] for i in range(0, len(self.frames), self.frames_x)]

    def behavior(self):
        if self.player_distance() > self.attack_range:
            self.track_player()
        else:
            if self.attack_counter >= self.attack_delay:
                self.attack(self.target)
                self.attack_counter = 0
        self.attack_counter += 1

class Slime(Enemy):
    def __init__(self, pos, player, bullets_group):
        self.sprite_sheet = "assets\\images\\enemies\\Slime\\slime_idle.png"
        self.frames_x = 4
        self.frames_y = 2
        self.health = 100
        self.speed = 3
        self.damage = 40
        self.attack_delay = 50
        self.attack_range = 50

        super().__init__(pos, self.sprite_sheet, self.frames_x, self.frames_y, self.health, self.speed, self.damage, self.attack_range, self.attack_delay, player, bullets_group)

