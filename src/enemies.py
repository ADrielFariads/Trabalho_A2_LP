"""
This module handles the creation and management of enemies. It provides classes for various enemy types, each with unique behaviors and attributes, as well as functions for dynamically spawning enemies on the map.

"""

import pygame
import random

import config

image_dict = config.load_enemies_images()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_sheet, frames_x, frames_y, health, speed, damage, attack_range, attack_delay, player, bullets_group, group, colliders=None):
        """
        Initializes the Enemy sprite with specified attributes.

        Args:
        pos (tuple): The position of the enemy (x, y).
        sprite_sheet (str): Sprite sheet loaded with pygame
        frames_x (int): The number of frames in the horizontal direction.
        frames_y (int): The number of frames in the vertical direction.
        health (int): The initial health of the enemy.
        speed (int): The movement speed of the enemy.
        damage (int): The damage dealt by the enemy.
        attack_range (int): The range within which the enemy can attack.
        attack_delay (int): Delay between consecutive attacks.
        player (Player): The player character the enemy will interact with.
        bullets_group (pygame.sprite.Group): Group containing all the bullets.
        group (pygame.sprite.Group): Group the enemy belongs to.
        colliders (list, optional): List of colliders to check for collisions.

        """
        super().__init__()

        # Loading image
        self.sprite_sheet = sprite_sheet

        self.frames_x = frames_x
        self.frames_y = frames_y

        # Load frames
        self.load_frames()

        # Initial frame setting
        self.current_frame_index = 0
        self.animation_speed = 10  # Bigger values for a smoother animation
        self.frame_counter = 0  # Counter of animation
        self.original_animation_speed = 10

        self.x = pos[0]
        self.y = pos[1]
        self.position = pygame.math.Vector2(self.x, self.y)
        self.image = self.frames[self.current_frame_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Attributes
        self.max_health = health
        self.health = health
        self.speed = speed
        self.original_speed = speed
        self.damage = damage
        self.attack_range = attack_range
        self.attack_delay = attack_delay
        self.attack_counter = 50  # Time between attacks

        # Player interaction
        self.attack_counter = 0
        self.target = player
        self.bullets = bullets_group
        self.experience_given = 10
        self.colliders = colliders

        #groups
        self.z_index = 8
        group.add(self)
        self.group = group

    def reset_enemies(self, enemies):
        """
        Resets the state of all enemies in the list to their initial conditions.

        Args:
        enemies (list): List of enemies to be reset.

        """
        for enemy in enemies:
            enemy.health = enemy.max_health
            enemy.position = pygame.math.Vector2(enemy.x, enemy.y)
            enemy.image = enemy.frames[enemy.current_frame_index]
            enemy.rect = enemy.image.get_rect(center=(enemy.x, enemy.y))
            enemy.current_frame_index = 0
            enemy.animation_speed = 10  
            enemy.frame_counter = 0

    def load_frames(self):
        """
        Loads frames from the sprite sheet based on the number of frames horizontally and vertically.

        """
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
        """
        Updates the current animation frame based on the animation speed.

        """
        # Increment frame counter and update frame index
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.image = self.frames[self.current_frame_index]
            self.frame_counter = 0
    # Fight logic
    def get_damaged(self, damage):
        """
        Reduces the enemy's health by the given damage.

        Args:
        damage (int): The amount of damage to be applied to the enemy.

        """
        self.health -= damage
    
    def get_healed(self, amount):
        """
        Increases the enemy's health by the specified amount, ensuring it doesn't exceed the maximum health.

        Args:
        amount (int): The amount to heal.

        """
        if self.health <= self.max_health:
            self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def attack(self, target):
        """
        Attacks the target player, reducing their health by the enemy's damage.

        Args:
        target (Player): The target player to be attacked.

        """
        target.get_damaged(self.damage)

    def player_distance(self):
        """
        Calculates the distance between the enemy and the player.

        Returns:
        float: The distance between the enemy and the player.

        """
        player_pos = pygame.math.Vector2(self.target.rect.center)
        current_pos = pygame.math.Vector2(self.rect.center)
        distance = current_pos.distance_to(player_pos)
        return distance

    def track_player(self):
        """
        Tracks the player's position and moves the enemy toward the player, considering the attack range.

        """
        player_pos = pygame.math.Vector2(self.target.rect.center)
        current_pos = pygame.math.Vector2(self.rect.center)
        if self.player_distance() > self.attack_range:
            self.direction = (player_pos - current_pos).normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)

        movement = self.direction * self.speed

        self.rect.x += movement.x
        self.rect.y += movement.y
        self.collision("horizontal")
        self.collision("vertical")

    def behavior(self):
        """
        Placeholder for enemy behavior logic, can be extended in subclasses.

        """
        pass

    def collision(self, direction):
        """
        Handles collision detection and resolution for the enemy.

        Args:
        direction (str): The direction to check for collisions ('horizontal' or 'vertical').

        """
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
        """
        Updates the enemy state, including checking for death, handling bullet collisions, and animating.

        """
        # Checks the mob's death
        if self.health <= 0:
            self.target.experience += self.damage
            self.target.enemy_killed()
            self.kill()
            return None
        
        collided_bullets = pygame.sprite.spritecollide(self, self.bullets, True)
        for bullet in collided_bullets:
            self.get_damaged(bullet.damage)
        
        self.behavior()

        # Animation logic
        self.animate()
        self.position.x = self.rect.x
        self.position.y = self.rect.y

    def update_target(self, new_target):
        """
        Dynamically updates the enemy's target to a new player.

        Args:
        new_target (Player): The new player target.

        """
        self.target = new_target


class Goblin(Enemy):
    def __init__(self, pos, player, bullets_group):
        # Initialize the sprite sheet and animation parameters
        self.sprite_sheet = image_dict["GOBLIN"]
        self.frames_x = 11  # colums
        self.frames_y = 5  # lines
        self.health = 500
        self.speed = random.uniform(2, 6)  # Random speed for each goblin
        self.damage = 100
        self.attack_delay = 50
        self.attack_range = 50
        self.experience_given = 30
        super().__init__(pos, self.sprite_sheet, self.frames_x, self.frames_y, self.health, self.speed, self.damage, self.attack_range, self.attack_delay, player, bullets_group)
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
    def __init__(self, pos, player, bullets_group, enemy_group):
        """
        Initialize the Andromaluis class with specific attributes such as sprite sheet, health, 
        speed, damage, attack delay, attack range, and skill-related attributes.
        
        :param pos: The initial position of Andromaluis.
        :param player: The player object that Andromaluis will target.
        :param bullets_group: The group of bullets for collision detection.
        :param enemy_group: The group to which Andromaluis belongs, for adding spawned enemies.
        """
        self.sprite_sheet = image_dict["ANDROMALUIS"]
        self.frames_x = 8
        self.frames_y = 3
        self.health = 1500
        self.speed = 1
        self.damage = 100
        self.attack_delay = 1000
        self.attack_range = 500
        self.enemy_group = enemy_group
        self.experience_given = 100
        
        # Skill attributes
        self.generation_interval = 100
        self.generation_timer = 10
        super().__init__(pos, self.sprite_sheet, self.frames_x, self.frames_y, self.health, self.speed, self.damage, self.attack_range, self.attack_delay, player, bullets_group)

    def behavior(self):
        """
        Define the behavior of Andromaluis. It generates goblins if the distance to the target is 
        less than 200 and the generation timer has elapsed.
        """
        # Calculate the distance to the target (player)
        distance_to_enemy = self.target.position - self.position

        if distance_to_enemy.length() < 200:
            # If the distance is less than 200 and the generation timer has elapsed, generate goblins
            if self.generation_timer <= 0:
                generate_goblins(4, self.rect.top, self.rect.bottom, self.rect.left, self.rect.right, self.target, self.bullets, self.enemy_group)
                self.generation_timer = self.generation_interval

        # Decrease the generation timer
        self.generation_timer -= 1



class Centipede(Enemy):
    def __init__(self, pos, player, bullets_group):
        """
        Initialize the Centipede class with specific attributes such as sprite sheet, health, 
        speed, damage, attack delay, and attack range.

        :param pos: The initial position of the centipede.
        :param player: The player object that the centipede will target.
        :param bullets_group: The group of bullets for collision detection.
        """
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
        """
        Load the frames from the sprite sheet and divide them into sublists based on the movement direction.
        """
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
        """
        Define the behavior of the Centipede. The centipede will either track the player or attack 
        if within range.
        """
        if self.player_distance() > self.attack_range:
            # Track the player if the distance is greater than the attack range
            self.track_player()
        else:
            # If within attack range, perform an attack
            if self.attack_counter >= self.attack_delay:
                self.attack(self.target)
                self.attack_counter = 0
        self.attack_counter += 1


class Slime(Enemy):
    def __init__(self, pos, player, bullets_group, level, group):
        """
        Initialize the Slime class with specific attributes such as sprite sheet, health, 
        speed, damage, attack delay, attack range, and level-specific attributes.

        :param pos: The initial position of the slime.
        :param player: The player object that the slime will target.
        :param bullets_group: The group of bullets for collision detection.
        :param level: The level of the slime, affecting its attributes.
        :param group: The group to which the slime belongs, used for collision detection.
        """
        self.sprite_sheet = image_dict["SLIME"]
        self.frames_x = 4
        self.frames_y = 2
        self.level = min(level, 3)
        self.health = 500 * self.level
        self.speed = 8 - self.level
        self.damage = 20 * self.level
        self.attack_delay = 100
        self.attack_range = 10
        self.level = level
        super().__init__(pos, self.sprite_sheet, self.frames_x, self.frames_y, self.health, self.speed, self.damage, self.attack_range, self.attack_delay, player, bullets_group, group)
        self.sprite_sheet = pygame.transform.scale_by(self.sprite_sheet, self.level)
        self.load_frames()
        self.rect = self.image.get_rect(center=pos)
        self.rect.size = (64 * self.level - 32, 64 * self.level - 32)

    def load_frames(self):
        """
        Load the frames from the sprite sheet, cutting 80% of the frame height and 
        resizing them to the appropriate size.

        The frames are divided into sublists based on their direction.
        """
        frame_width = self.sprite_sheet.get_width() // self.frames_x
        frame_height = self.sprite_sheet.get_height() // self.frames_y

        self.frames = []
        for y in range(self.frames_y):
            for x in range(self.frames_x):
                # Calculate the cutting position to get the bottom 80% of the frame
                y_offset = y * frame_height + int(frame_height * 0.3)  # Starting from 30% of the frame height
                new_frame_height = int(frame_height * 0.7)  # The height of the cut will be 80% of the original frame height

                # Cut the bottom part of the frame
                frame = self.sprite_sheet.subsurface((x * frame_width, y_offset, frame_width, new_frame_height))

                # Resize to the original size
                redimensioned_frame = pygame.transform.scale(frame, (frame_width, new_frame_height))

                self.frames.append(redimensioned_frame)

        # Divide the frames into sublists for each direction
        self.divided_frames = [self.frames[i:i + self.frames_x] for i in range(0, len(self.frames), self.frames_x)]

    def behavior(self):
        """
        Define the behavior of the slime. The slime tracks the player and attacks 
        if within range.
        """
        self.track_player()
        self.attack_counter += 1
        if self.player_distance() <= self.attack_range:
            # Attack the player if within range and the attack delay has passed
            if self.attack_counter >= self.attack_delay:
                self.attack(self.target)
                self.attack_counter = 0

    def duplicate(self):
        """
        Duplicate the slime if its level is greater than 1. This creates two smaller 
        slimes at positions near the original slime.

        This method is called when the slime is killed.
        """
        if self.level > 1:
            # Create two smaller slimes at different positions
            child_1 = Slime((self.position.x + 50, self.position.y), self.target, self.bullets, (self.level - 1), self.group)
            child_2 = Slime((self.position.x - 50, self.position.y), self.target, self.bullets, (self.level - 1), self.group)
            child_1.colliders = self.colliders
            child_2.colliders = self.colliders

    def update(self):
        """
        Update the slime's behavior and check if its level has reached zero. If so, 
        the slime is killed and duplicates are created.

        :return: The result of the superclass update method.
        """
        if self.level <= 0:
            self.kill()
        return super().update()

    def kill(self):
        """
        Kill the slime by duplicating it before removing it from the game.

        :return: The result of the superclass kill method.
        """
        self.duplicate()
        return super().kill()

class AlienBat(Enemy):
    def __init__(self, pos, player, bullets_group, group):
        """
        Initialize the AlienBat class with specific attributes such as sprite sheet, health, 
        speed, damage, attack delay, attack range, and a flag for duplication.

        :param pos: The initial position of the alien bat.
        :param player: The player object that the alien bat will target.
        :param bullets_group: The group of bullets for collision detection.
        :param group: The group to which the alien bat belongs, used for collision detection.
        """
        self.group = group
        self.sprite_sheet = image_dict["ALIENBAT"]
        self.frames_x = 6
        self.frames_y = 2
        self.health = 300
        self.speed = 5
        self.damage = 100
        self.attack_delay = 200
        self.attack_range = 100
        super().__init__(pos, self.sprite_sheet, self.frames_x, self.frames_y, self.health, self.speed, self.damage, self.attack_range, self.attack_delay, player, bullets_group, self.group)
        self.colliders = None
        self.duplicate = True

    def behavior(self):
        """
        Define the behavior of the AlienBat. The AlienBat tracks the player and attacks 
        when within range. If it attacks, it replicates itself if the duplication flag is True.

        The attack counter is incremented and checked to ensure the attack is delayed appropriately.
        """
        self.track_player()
        self.attack_counter += 1
        if self.player_distance() <= self.attack_range:
            if self.attack_counter >= self.attack_delay:
                # Attack the player if within range
                self.attack(self.target)
                self.attack_counter = 0
                if self.duplicate:
                    self.replicate()

    def replicate(self):
        """
        Create a duplicate of the AlienBat at the same position and target.
        The duplication flag is set to False to prevent further replication.

        A new AlienBat instance is created with the same position, target, and bullets group.
        """
        child = AlienBat(self.position, self.target, self.bullets, self.group)
        self.duplicate = False


        
        