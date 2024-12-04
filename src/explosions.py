import pygame
import math

class Explosion(pygame.sprite.Sprite):
    """
    Represents an explosion effect in the game.

    Attributes:
        pos (tuple): The (x, y) position of the explosion's center.
        radius (int): The radius of the explosion's area of effect.
        damage (int): The damage dealt to targets within the radius.
        target_group (pygame.sprite.Group): The group of potential targets affected by the explosion.
        sprite_sheet (list): A list of surfaces representing the explosion's animation frames.
        muted (bool): Whether the explosion sound is muted.
        hit_targets (set): A set of targets already damaged to prevent duplicate damage.
        z_index (int): The rendering order of the explosion.
    """

    def __init__(self, pos, damage, target_group, sprite_sheet, radius=100, muted=True):
        """
        Initializes an Explosion object.

        Args:
            pos (tuple): The position of the explosion's center.
            damage (int): The damage dealt by the explosion.
            target_group (pygame.sprite.Group): The group of targets to be affected.
            sprite_sheet (list): Animation frames for the explosion.
            radius (int, optional): The radius of the explosion. Defaults to 100.
            muted (bool, optional): Whether the sound is muted. Defaults to True.
        """
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


        self.image = self.sprite_sheet[self.current_frame]
        self.rect = self.image.get_rect(center=self.pos)
        if not muted:
            self.sound = pygame.mixer.Sound("assets\\audio\\skills\\explosion_sound_1.wav")
            self.sound.set_volume(0.5)
            self.sound.play()

        self.hit_targets = set() #to not cause damage in the same enemy multiple times

    def animate(self):
        """
        Updates the explosion animation by switching to the next frame.

        Kills the sprite if the animation is complete.
        """
        current_time = pygame.time.get_ticks()

        if current_time - self.last_frame_time >= self.animation_delay:
            self.current_frame += 1
            self.last_frame_time = current_time

            if self.current_frame < self.frames:
                self.image = self.sprite_sheet[self.current_frame]
            else:
                self.kill()

    def check_collisions(self):
        """
        Checks for collisions with targets within the explosion radius.
        Deals damage to affected targets.
        """
        for target in self.target_group:
            if hasattr(target, "get_damaged"):
                distance = math.hypot(
                    target.rect.centerx - self.pos[0],
                    target.rect.centery - self.pos[1]
                )
                if distance <= self.radius and target not in self.hit_targets:
                    target.get_damaged(self.damage)
                    self.hit_targets.add(target)

    def update(self):
        """
        Updates the explosion's animation and checks for collisions.
        """
        self.animate()
        self.check_collisions()


class Missile(pygame.sprite.Sprite):
    """
    Represents a missile that moves toward a target position and explodes upon impact.

    Attributes:
        start_pos (tuple): The starting position of the missile.
        target_pos (tuple): The target position the missile is aiming for.
        speed (float): The speed of the missile's movement.
        target_group (pygame.sprite.Group): The group of targets potentially affected by the missile.
        radius (int): The radius of the explosion caused by the missile.
        damage (int): The damage dealt by the missile's explosion.
        explosion_sprite_sheet (list): The animation frames for the explosion.
        muted (bool): Whether the missile and explosion sounds are muted.
        z_index (int): The rendering order of the missile.
    """

    def __init__(self, start_pos, target_pos, speed, target_group, radius, damage, explosion_spritesheet, explosion_group, muted=True):
        """
        Initializes a Missile object.

        Args:
            start_pos (tuple): The starting position of the missile.
            target_pos (tuple): The target position for the missile.
            speed (float): The speed of the missile.
            target_group (pygame.sprite.Group): Targets affected by the missile explosion.
            radius (int): The radius of the explosion.
            damage (int): The damage dealt by the explosion.
            explosion_spritesheet (list): Animation frames for the explosion.
            explosion_group (pygame.sprite.Group): Group to hold explosion effects.
            muted (bool, optional): Whether sounds are muted. Defaults to True.
        """
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
        """
        Updates the missile's position and triggers an explosion upon reaching the target.
        """
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
    """
    Represents a vortex effect that pulls in and damages nearby targets.

    Attributes:
        pos (tuple): The (x, y) position of the vortex's center.
        radius (int): The radius of the vortex's effect.
        damage (int): The damage dealt to targets within the radius.
        target_group (pygame.sprite.Group): The group of targets affected by the vortex.
        duration (int): The duration of the vortex's effect in milliseconds.
        particles (pygame.sprite.Group): A group for additional visual effects.
        z_index (int): The rendering order of the vortex.
    """

    def __init__(self, pos, radius, target_group, damage, duration):
        """
        Initializes a Vortex object.

        Args:
            pos (tuple): The position of the vortex.
            radius (int): The radius of the vortex.
            target_group (pygame.sprite.Group): Targets affected by the vortex.
            damage (int): The damage dealt by the vortex.
            duration (int): Duration of the vortex in milliseconds.
        """
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
        """
        Animates the vortex by gradually increasing its size.
        """
        if self.scale_factor < 1: 
            self.scale_factor += 0.1  

        new_width = int(self.original_image.get_width() * self.scale_factor)
        new_height = int(self.original_image.get_height() * self.scale_factor)

        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
        self.rect = self.image.get_rect(center=self.pos)
        
    def check_collisions(self):
        """
        Checks for collisions with targets within the vortex's radius.
        Pulls targets toward the vortex's center and damages them.
        """
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
                    target.rect.x += int(direction.x * -5)
                    target.rect.y += int(direction.y * -5)

                    if distance <= 15 and hasattr(target, "kill"): # Threshold for "death"  # Remove target from the group
                        self.kill_sound.play()
                        target.kill()

    def update(self):
        for each in self.particles:
            each.update()
        self.check_collisions()
        self.animate()
