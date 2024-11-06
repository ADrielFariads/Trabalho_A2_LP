import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos_x, pos_y, sprite_sheet, health, speed, damage, attack_range,attack_speed, player):
        super().__init__()
        #loading image
        self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()

        frames_x_axis = 11
        frame_widht = self.sprite_sheet.get_width() // frames_x_axis
        frame_height = self.sprite_sheet.get_height()

        self.frames = []
        for each in range(frames_x_axis):
            frame = self.sprite_sheet.subsurface((each * frame_widht, 0, frame_widht, frame_height))
    
            redimentioned_frame = pygame.transform.scale(frame, (int(frame_widht), int(frame_height)))
            self.frames.append(redimentioned_frame)

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
        self.atack_range = attack_range

        #player interaction
        self.target = player

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
        if self.player_distance() > self.atack_range:
            self.track_player()
        else:
            self.atack(self.target)

        #animation logic
        self.animate()
