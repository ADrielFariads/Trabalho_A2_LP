import pygame
import math
import random

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, damage, target_group, sprite_sheet, radius=100, muted=True):
        super().__init__()
        self.pos = pos
        self.radius = radius
        self.damage = damage
        self.target_group = target_group
        self.sprite_sheet = sprite_sheet
        self.frames = len(self.sprite_sheet)
        self.current_frame = 0
        self.animation_delay = 35
        self.last_frame_time = pygame.time.get_ticks()
        self.z_index = 12

        if self.radius != 100:
            self.sprite_sheet = [pygame.transform.scale(img, (int(radius*2), int(radius*2))) for img in self.sprite_sheet]

        self.image = self.sprite_sheet[self.current_frame]
        self.rect = self.image.get_rect(center=self.pos)
        if not muted:
            self.sound = pygame.mixer.Sound("assets\\audio\\skills\\explosion_sound_1.wav")
            self.sound.set_volume(0.5)
            self.sound.play()

        self.hit_targets = set()  #to not cause damage in the same enemy multiple times

    def animate(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_frame_time >= self.animation_delay:
            self.current_frame += 1
            self.last_frame_time = current_time

            if self.current_frame < self.frames:
                self.image = self.sprite_sheet[self.current_frame]

            else:
                self.kill()
            
    def check_collisions(self):
        for target in self.target_group:
            if hasattr(target, "get_damaged"):
                distance = math.hypot(target.rect.centerx - self.pos[0], target.rect.centery - self.pos[1])
                if distance <= self.radius and target not in self.hit_targets:
                    target.get_damaged(self.damage)
                    self.hit_targets.add(target)
    
    def update(self):
        self.animate()
        self.check_collisions()
                

class Missile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, speed, target_group, radius, damage, explosion_spritesheet, explosion_group, muted=True):
        super().__init__()
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.speed = speed
        self.explosion_group = explosion_group
        self.target_group = target_group
        self.radius = radius
        self.damage = damage
        self.muted = muted
        self.z_index = 12

        self.image = pygame.image.load("assets\\images\\Bullets\\missile1.png")
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect(center=start_pos)
        self.direction = pygame.math.Vector2(target_pos) - pygame.math.Vector2(start_pos)
        self.direction = self.direction.normalize()

        self.explosion_sprite_sheet = explosion_spritesheet

    def update(self):
        vector = self.direction * self.speed
        self.speed += 1
        self.rect.x += vector.x
        self.rect.y += vector.y

        #checks if its on the destination
        if pygame.math.Vector2(self.rect.center).distance_to(self.target_pos) <= self.speed:
            bomb = Explosion(self.rect.center, self.damage, self.target_group, self.explosion_sprite_sheet, self.radius, self.muted)
            self.explosion_group.add(bomb)
            self.kill()



class Vortex(pygame.sprite.Sprite):
    def __init__(self, pos, radius, target_group, damage, duration):
        super().__init__()
        self.radius = radius
        self.damage = damage
        self.pos = pos
        self.target_group = target_group
        self.image = pygame.image.load("assets\\images\\explosions\\vortex\\vortex.png")
        self.original_image = self.image
        self.current_frame = 0
        self.duration = duration
        self.scale_factor = 0.1
        self.start_time = pygame.time.get_ticks() 
        self.last_displacement_time = self.start_time
        self.particles = pygame.sprite.Group()
        self.z_index = 1
        self.sound = pygame.mixer.Sound("assets\\audio\\skills\\vortex_sound.wav")
        self.kill_sound = pygame.mixer.Sound("assets\\audio\\skills\\vortex_kill_sound.wav")
        self.sound.play()
    
    def animate(self):
        if self.scale_factor < 1: 
            self.scale_factor += 0.1  

        new_width = int(self.original_image.get_width() * self.scale_factor)
        new_height = int(self.original_image.get_height() * self.scale_factor)

        
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
        self.rect = self.image.get_rect(center=self.pos)
        
    def check_collisions(self):
        for target in self.target_group:
            if hasattr(target, "rect"):
                distance = math.hypot(target.rect.centerx - self.pos[0], target.rect.centery - self.pos[1])
                
                # If the target is within the Vortex's radius and hasn't been processed yet
                if distance <= self.radius:
                    # Calculate the direction vector from the Vortex's center to the target's center
                    direction = pygame.math.Vector2(target.rect.center) - pygame.math.Vector2(self.pos)
                    
                    # Normalize the direction vector to ensure uniform movement
                    if direction.length() > 0:
                        direction = direction.normalize()

                    # Apply a small displacement in the opposite direction of the Vortex's center
                    target.rect.x += int(direction.x * -5)  # Move along the x-axis
                    target.rect.y += int(direction.y * -5)

                    if distance <= 15:  # Threshold for "death"  # Remove target from the group
                        if hasattr(target, "kill"):
                            self.kill_sound.play()
                            target.kill()
    def update(self):
        for each in self.particles:
            each.update()
        self.check_collisions()
        self.animate()
