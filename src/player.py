"""
This module implements the Player class, managing the player's attributes, animations, movement, 
collision detection, health, experience, and skill usage. The player interacts with the game world through sprite-based 
actions and can level up, heal, and use special abilities while navigating within map boundaries.
"""


import pygame

import config
import skills

#loading images

player_sprites = config.load_player_images()
cyborg_images_dict = player_sprites[0]
blademaster_image_dict = player_sprites[1]
berserker_image_dict = player_sprites[2]


class Player(pygame.sprite.Sprite):
    """
    A class representing the player character in the game.
    Inherits from pygame.sprite.Sprite to manage sprite actions and animations.

    Attributes:
        pos (tuple): Initial position of the player.
        health (int): Initial health value of the player.
        speed (int): Speed at which the player moves.
        map_bounds (pygame.Rect): Bounds of the map for movement restrictions.
        skills (list): List of skills available to the player.
        colidders (list, optional): List of collidable objects for detecting collisions.
    """

    def __init__(self, pos, health, speed, map_bounds, skills, spritesheet_dict, colidders=None):
        """
        Initializes the player character with the given attributes.

        Args:
            pos (tuple): Initial position of the player.
            health (int): Initial health value of the player.
            speed (int): Speed at which the player moves.
            map_bounds (pygame.Rect): Bounds of the map for movement restrictions.
            skills (list): List of skills available to the player.
            colidders (list, optional): List of collidable objects for detecting collisions.
        """
        super().__init__()

        self.sprite_sheet_dict = spritesheet_dict

        #loads the image
        self.sprite_sheet = self.sprite_sheet_dict['IDLE']
        self.current_action = "idle"

        #calculating the frame size
        frames_x_axis = 4
        frame_widht = self.sprite_sheet.get_width() // frames_x_axis
        frame_height = self.sprite_sheet.get_height()

        #generating frames
        self.frames = []
        for each in range(frames_x_axis):
            frame = self.sprite_sheet.subsurface((each * frame_widht, 0, frame_widht, frame_height))
            scale_factor = 2 # makes the image a little bigger
            redimentioned_frame = pygame.transform.scale(frame, (int(frame_widht)*scale_factor, int(frame_height)*scale_factor))
            self.frames.append(redimentioned_frame)

        #initial frame setting
        self.current_frame_index = 0
        self.animation_speed = 5 #bigger values for a smothier animation
        self.frame_counter = 0 #counter of animation
        self.image = self.frames[self.current_frame_index] #current image 
        self.facing_right = True #side facing animation

        #position logic
        self.initial_pos = pos
        self.position = pygame.math.Vector2(self.initial_pos)
        self.rect = self.image.get_rect(center=(self.initial_pos))
        self.z_index = 10

        #health logic
        self.health = health
        self.target_health = health
        self.direction = pygame.math.Vector2(0, 0)

        #experience logic
        self.experience = 0
        self.current_level = 1
        self.killed_enemies = 0
        self.experience_needed = 500 * self.current_level

        #colidders
        self.colliders = colidders
        self.map_bounds = map_bounds

        #player atributes
        self.speed = speed
        self.max_health = health
        self.current_health = self.max_health
        self.armor = 0
        self.life_steal = 0

        #skills logic
        self.skills = skills

################# ANIMATING FRAMES ##########################################################
    def reset_player(self):
        """
        Resets the player attributes to their initial settings.
        """
        self.current_frame_index = 0
        self.frame_counter = 0
        self.image = self.frames[self.current_frame_index]
        self.facing_right = True
        self.current_health = self.max_health
        self.position = pygame.math.Vector2(self.initial_pos)
        self.rect = self.image.get_rect(center=(self.initial_pos))
        self.current_action = "idle"
        self.target_health = self.health

    def load_frames(self, sprite_sheet, frames_x):
        """
        Extracts and scales frames from the given sprite sheet.

        Args:
            sprite_sheet (pygame.Surface): The sprite sheet containing the frames.
            frames_x (int): Number of frames along the x-axis in the sprite sheet.

        Returns:
            list: A list of scaled frames as pygame surfaces.
        """
        frames = []
        frame_width = sprite_sheet.get_width() // frames_x
        frame_height = sprite_sheet.get_height()

        # Define the scaling factor
        scale_factor = 2
        new_frame_width = int(frame_width * scale_factor)
        new_frame_height = int(frame_height * scale_factor)

        for x in range(frames_x):
            frame = sprite_sheet.subsurface((x * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (new_frame_width, new_frame_height))
            frames.append(scaled_frame)
        return frames

################# ACTIONS LOGIC ################################## 
    def set_action(self, action="idle"):
        """
        Sets the current action of the player character and loads corresponding animation frames.

        Args:
            action (str): The action to set, such as "idle", "walk", "walkup", "walkdown".
        """
        if self.current_action != action:
            self.current_action = action
            self.current_frame_index = 0

        if action == "idle":
            self.current_action = "idle"
            self.sprite_sheet = self.sprite_sheet_dict['IDLE']
            self.frames = self.load_frames(self.sprite_sheet, 4)

        if action == "walk":
            self.current_action = "walk"
            self.sprite_sheet = self.sprite_sheet_dict['WALK']
            self.frames = self.load_frames(self.sprite_sheet, 6)

        if action == "walkup":
            self.current_action = "walkup"
            self.sprite_sheet = self.sprite_sheet_dict['WALKUP']
            self.frames = self.load_frames(self.sprite_sheet, 6)

        if action == "walkdown":
            self.current_action = "walkdown"
            self.sprite_sheet = self.sprite_sheet_dict['WALKDOWN']
            self.frames = self.load_frames(self.sprite_sheet, 6)

################# GETTER METHODS ###################################################
    def get_position(self):
        """
        Returns the current position of the player.

        Returns:
            pygame.math.Vector2: The current position of the player.
        """
        return self.position

################# COLLISION METHOD ####################################################     
    def collision(self, direction):
        """
        Checks and resolves collisions with other sprites in the given direction.

        Args:
            direction (str): The direction of the collision to check ("horizontal" or "vertical").
        """
        if self.colliders is not None:
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

################# UPDATE METHOD #################################################### 
    def update(self, keys):
        """
        Updates the player's state, including animation, movement, and collisions.

        Args:
            keys (pygame.key.get_pressed): The current key states for movement and actions.
        """
        #animation logic
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.image = self.frames[self.current_frame_index]
            self.frame_counter = 0

        #movement logic

        # Reset direction vector
        self.direction.x = 0
        self.direction.y = 0

        # Horizontal movement first (priority)
        if keys[pygame.K_a]:  # Left
            self.direction.x = -1
            self.facing_right = False
            self.set_action("walk")
        elif keys[pygame.K_d]:  # Right
            self.direction.x = 1
            self.facing_right = True
            self.set_action("walk")

        # Vertical animation only if no horizontal input
        
        if keys[pygame.K_w]:  # Up
            self.direction.y = -1
            if self.direction.x == 0:
                    self.set_action("walkup")
        elif keys[pygame.K_s]:  # Down
            self.direction.y = 1
            if self.direction.x == 0:
                self.set_action("walkdown")

        # Set idle if no keys are pressed
        if self.direction.length() == 0:
            self.set_action("idle")
        else:
            self.direction.normalize_ip()

        # Update sprite flip for horizontal movement
        if not self.facing_right:
            self.image = pygame.transform.flip(self.frames[self.current_frame_index], True, False)
        else:
            self.image = self.frames[self.current_frame_index]

        # Update position based on speed
        self.position.x += self.direction.x * self.speed
        self.rect.centerx = self.position.x
        self.collision("horizontal")

        self.position.y += self.direction.y * self.speed
        self.rect.centery = self.position.y
        self.collision("vertical")

        self.position = pygame.math.Vector2(self.rect.center)

        if self.position.x < self.map_bounds.left:
            self.position.x = self.map_bounds.left
        elif self.position.x > self.map_bounds.right:
            self.position.x = self.map_bounds.right

        if self.position.y < self.map_bounds.top:
            self.position.y = self.map_bounds.top
        elif self.position.y > self.map_bounds.bottom:
            self.position.y = self.map_bounds.bottom

        current_image = self.frames[self.current_frame_index]

        if not self.facing_right:
            self.image = pygame.transform.flip(current_image, True, False)
        else:
            self.image = current_image

        if self.experience >= self.experience_needed:
            self.level_up()
        
        #skills

        for skill in self.skills:
            skill.update(self)

        if keys[pygame.K_q] and self.current_level >= self.skills[-2].unlock_level:
            self.skills[-2].use(self)

        if keys[pygame.K_e] and self.current_level >= self.skills[-1].unlock_level:
            self.skills[-1].use(self)

################# HEALTH LOGIC ##############################################################

    def get_damaged(self, damage):
        """
        Applies damage to the player, reducing health based on armor.

        Args:
            damage (int): The amount of damage to apply.
        """
        if self.target_health > 0:
            self.target_health -= int(damage*(1-self.armor))

        if self.target_health <= 0:
            self.target_health = 0

    def get_healed(self, heal):
        if self.target_health < self.max_health:
            self.target_health += heal

        if self.target_health >= self.max_health:
            self.target_health = self.max_health

######## level logic ######################################################################

    def level_up(self):
        """
        Increases the player's level and resets experience points.
        """
        self.current_level += 1
        self.experience = 0


    def enemy_killed(self):
        """
        Heals the player based on life steal and increments the killed enemies count.
        """
        self.get_healed(self.life_steal)
        self.killed_enemies += 1



############################################### subclasses creation ########################################################
cyborg_skills = [skills.MachineGunRender(), skills.LethalTempo(), skills.MissilRain()]
blademaster_skills = [skills.KnifeThrowerRender(), skills.Bloodlust(), skills.TimeManipulation()]
berserker_skills = [skills.ShotgunRender(), skills.IronWill(), skills.GravitionVortex()]

class Cyborg(Player):
    def __init__(self, pos, map_bounds, colidders=None):
        health = 1500
        speed = 8
        super().__init__(pos, health, speed, map_bounds, cyborg_skills, cyborg_images_dict, colidders)

class BladeMaster(Player):
    def __init__(self, pos, map_bounds, colidders=None):

        health = 1200
        speed = 10
        super().__init__(pos, health, speed, map_bounds, blademaster_skills, blademaster_image_dict, colidders)

class Berserker(Player):
    def __init__(self, pos, map_bounds, colidders=None):

        health = 2000
        speed = 7
        super().__init__(pos, health, speed, map_bounds, berserker_skills, berserker_image_dict, colidders)