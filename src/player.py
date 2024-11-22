"""
This module implements the Player class, managing the player's attributes, animations, movement, 
collision detection, health, experience, and skill usage. The player interacts with the game world through sprite-based 
actions and can level up, heal, and use special abilities while navigating within map boundaries.
"""


import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, health, speed, map_bounds, skills, colidders=None):
        super().__init__()
        #loads the image
        self.sprite_sheet = pygame.image.load("assets/images/Player/Idle1.png").convert_alpha()
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
        self.position = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center = (pos))


        #health logic
        self.target_health = health
        self.direction = pygame.math.Vector2(0,0)

        #experience logic
        self.experience = 0
        self.current_level = 1

        #colidders
        self.colliders = colidders
        self.map_bounds = map_bounds

        #player atributes 
        self.speed = speed
        self.max_health = health
        self.current_health = self.max_health
        self.armor = 0
        

        #skills logic
        self.skills = skills

################# ANIMATING FRAMES ##########################################################
    def load_frames(self, sprite_sheet, frames_x):
        "Extract and scale frames from the given sprite sheet."
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
    def set_action(self, action="idle"):#action setter for animation
        
        if self.current_action != action:
            self.current_action = action
            self.current_frame_index = 0

        if action == "idle":
            self.current_action = "idle"
            self.sprite_sheet = pygame.image.load("assets/images/Player/Idle1.png").convert_alpha()
            self.frames = self.load_frames(self.sprite_sheet, 4)
        
        if action == "walk":
            self.current_action = "walk"
            self.sprite_sheet = pygame.image.load("assets/images/Player/Walk1.png").convert_alpha()
            self.frames = self.load_frames(self.sprite_sheet, 6)

        if action == "walkup":
            self.current_action = "walkup"
            self.sprite_sheet = pygame.image.load("assets/images/Player/WalkUp.png").convert_alpha() 
            self.frames = self.load_frames(self.sprite_sheet, 8)

        if action == "walkdown":
            self.current_action = "walkdown"
            self.sprite_sheet = pygame.image.load("assets/images/Player/WalkDown.png").convert_alpha() 
            self.frames = self.load_frames(self.sprite_sheet, 8)

################# GETTER METHODS ###################################################
    def get_position(self):
        return self.position

################# COLLISION METHOD ####################################################     
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
    

################# UPDATE METHOD #################################################### 
    def update(self, keys):
        #animation logic
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.image = self.frames[self.current_frame_index]
            self.frame_counter = 0


        #movement logic
        
        self.direction.x = 0
        self.direction.y = 0
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
            self.set_action("walk")

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True

        if keys[pygame.K_w]:
            self.direction.y = -1
        if keys[pygame.K_s]:
            self.direction.y = 1

        if self.direction.length() > 0: #walk detection for animation
            self.direction = self.direction.normalize()
            self.set_action("walk")

        elif keys[pygame.K_w] and not keys[pygame.K_s]:  # up only
            self.direction.y = -1
            self.set_action("walkup")

        elif keys[pygame.K_s] and not keys[pygame.K_w]:  # down only
            self.direction.y = 1
            self.set_action("walkdown")

         
        if self.direction.length() == 0: #verify is player is idle
            self.set_action("idle")


        ##collisions
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

        if self.experience >= 500:
            self.level_up()
        
        #skills

        for skill in self.skills:
            skill.update(self)

        if keys[pygame.K_q]:
            self.skills[-2].use(self)

        if keys[pygame.K_e]:
            self.skills[-1].use(self)
            

################# HEALTH LOGIC ##############################################################
    def get_damaged(self, damage):
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
        self.current_level += 1 
        self.experience = 0

