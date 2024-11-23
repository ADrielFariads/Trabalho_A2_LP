import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, health, speed, map_bounds, colidders=None):
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
        self.initial_pos = pos
        self.position = pygame.math.Vector2(self.initial_pos)
        self.rect = self.image.get_rect(center = (self.initial_pos))


        #health bar logic
        self.health_bar_length = 500
        self.health_change_speed = 2
        self.target_health = health
        self.direction = pygame.math.Vector2(0,0)

        #experience logic
        self.experience_bar_lenght = 500
        self.experience = 0
        self.current_level = 1

        #colidders
        self.colliders = colidders
        self.map_bounds = map_bounds

        #player atributes 
        self.speed = speed
        self.max_health = health
        self.current_health = self.max_health
        self.health_ratio = self.current_health/self.health_bar_length
        
################# ANIMATING FRAMES ##########################################################
    def reset_player(self, player):
        '''
        Reset player attribues to initial setting
        '''
        player.current_frame_index = 0
        player.frame_counter = 0 
        player.image = player.frames[player.current_frame_index] 
        player.facing_right = True 
        player.current_health = player.max_health
        player.health_ratio = player.current_health/player.health_bar_lenght
        player.position = pygame.math.Vector2(player.initial_pos)
        player.rect = player.image.get_rect(center = (player.initial_pos))
        player.current_action = "idle"
        player.target_health = player.health

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

        if self.experience >= self.experience_bar_lenght:
            self.level_up()
        

################# HEALTH LOGIC ##############################################################
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

    def health_bar(self, surface): #health bar 
        transition_width = 0
        transition_color = (255, 255, 255)
        health_bar_rect = pygame.Rect(10, 10, self.current_health/self.health_ratio, 15)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, 10, transition_width, 15)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health-self.current_health)/self.health_ratio)
            transition_color = (0, 255, 0)
            transition_bar_rect = pygame.Rect(health_bar_rect.right, 10, transition_width, 15)

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int(abs((self.target_health-self.current_health)/self.health_ratio))
            transition_color = (255, 255, 0) 
            transition_bar_rect = pygame.Rect(health_bar_rect.right - transition_width, 10, transition_width, 15)

        
        pygame.draw.rect(surface, (255, 0, 0), health_bar_rect)#health
        pygame.draw.rect(surface, transition_color, transition_bar_rect) #heal/damage animation
        pygame.draw.rect(surface, (255, 255, 255), (10, 10, self.health_bar_length, 15), 2) #white rect arround the health

######## level logic ######################################################################
    def level_up(self):
        self.current_level += 1 
        print("level up", self.current_level)
        self.experience = 0

    def experience_bar(self, surface):
        experience_rect = pygame.Rect(10, 50, self.experience, 15)
        pygame.draw.rect(surface, (0, 0, 255), experience_rect)
        pygame.draw.rect(surface, (255, 255, 255), (10, 50, self.experience_bar_lenght, 15), 2)
        
