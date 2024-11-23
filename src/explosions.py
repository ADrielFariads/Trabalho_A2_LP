import pygame
import math


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, radius, damage, target_group, sprite_sheet):
        super().__init__()
        self.pos = pos
        self.radius = radius
        self.damage = damage
        self.target_group = target_group
        self.sprite_sheet = [pygame.image.load(image).convert_alpha() for image in sprite_sheet]
        self.frames = len(self.sprite_sheet)
        self.current_frame = 0
        self.animation_delay = 50
        self.last_frame_time = pygame.time.get_ticks()

        self.sprite_sheet = [pygame.transform.scale(img, (int(radius*2), int(radius*2))) for img in self.sprite_sheet]

        self.image = self.sprite_sheet[self.current_frame]
        self.rect = self.image.get_rect(center=self.pos)
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
    def __init__(self, start_pos, target_pos, speed, target_group, radius, damage, explosion_spritesheet, explosion_group, *groups):
        super().__init__(*groups)
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.speed = speed
        self.explosion_group = explosion_group
        self.target_group = target_group
        self.radius = radius
        self.damage = damage

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
            bomb = Explosion(self.rect.center, self.radius, self.damage, self.target_group, self.explosion_sprite_sheet)
            self.explosion_group.add(bomb)
            self.kill()



