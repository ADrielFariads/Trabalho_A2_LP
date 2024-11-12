import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos_x, pos_y, sprite_sheet, health, speed, damage, attack_range, attack_delay, player, bullets_group):
        super().__init__()
        #loading image
        self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()

        directions = 4
        frames_x_axis = 11
        frame_widht = self.sprite_sheet.get_width() // frames_x_axis
        frame_height = self.sprite_sheet.get_height() // directions

        self.frames = []
        for direction in range(directions):
            for each in range(frames_x_axis):
                frame = self.sprite_sheet.subsurface((each * frame_widht, direction * frame_height, frame_widht, frame_height))
        
                redimentioned_frame = pygame.transform.scale(frame, (int(frame_widht), int(frame_height)))
                self.frames.append(redimentioned_frame)

        self.divided_frames = [self.frames[i:i+11] for i in range(0, len(self.frames), 11)] #Dividing the list in subslists to each direction

        #initial frame setting
        self.current_frame_index = 0
        self.animation_speed = 10 #bigger values for a smothier animation
        self.frame_counter = 0 #counter of animation

        self.position = pygame.math.Vector2(pos_x, pos_y)
        self.image = self.frames[self.current_frame_index]
        self.rect = self.image.get_rect(center=(pos_x, pos_y))


        
        #atributes
        self.max_health = health
        self.health = health
        self.speed = speed
        self.damage = damage
        self.attack_range = attack_range
        self.attack_delay = attack_delay
        self.attack_counter = 0 #time between attacks

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
        
        if pygame.sprite.spritecollide(self, self.bullets, True):
            self.get_damaged(10)

        if self.player_distance() > self.attack_range:
            self.track_player()
        else:
            self.attack_counter += 1 
            if self.attack_counter >= self.attack_delay:
                self.attack(self.target)
                self.attack_counter = 0
            

        if self.direction.x > 0 and self.direction.x >= (self.direction.y **2) **(1/2):
            self.frames = self.divided_frames[1]

        elif self.direction.x < 0 and (self.direction.x**2) **(1/2) >= (self.direction.y**2) **(1/2):
            self.frames = self.divided_frames[3]

        elif self.direction.y < 0 and (self.direction.y**2) **(1/2) > (self.direction.x**2) **(1/2): 
            self.frames = self.divided_frames[2]

        elif self.direction.y > 0 and self.direction.y > (self.direction.x**2) **(1/2): 
            self.frames = self.divided_frames[0]




        #animation logic
        self.animate()