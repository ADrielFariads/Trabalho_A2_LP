import pygame
import math

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, image, damage, cool_down, bullet, map_bounds, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(image).convert_alpha()  # Load gun image
        self.player = player  # Reference to the player

        # Format the image
        self.image_width, self.image_height = self.image.get_size()
        self.original_image = pygame.transform.scale(self.image, (self.image_width * 2, self.image_height * 2))

        self.position = self.player.get_position()  # Set initial gun position
        self.map_bounds = map_bounds

        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.player.get_position())  # Get rect for the gun's position

        self.base_damage = damage  # Store gun damage value
        self.bullet_class = bullet  # Bullet class to use when shooting
        self.cool_down = cool_down  # Shooting cooldown in milliseconds
        self.last_shot_time = 0  # Time of the last shot
        self.sound = pygame.mixer.Sound("assets\\audio\\machine_gun.wav")
        self.sound.set_volume(0.5)

    def get_direction(self):
        # Get the direction to the mouse position
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())  # Get mouse position for aiming
        return mouse_position

    def update_position(self):
        # Update the gun's position to follow the player's position
        pass
        

    def update(self):
        # Update gun's position based on player movement
        self.position = self.player.get_position()
        self.rect.center = (self.position[0]-10, self.position[1]+15)

        if self.player.facing_right:
            self.image = self.original_image
            self.rect.center = (self.position[0]-10, self.position[1]+15)
        else:
            self.image = pygame.transform.flip(self.original_image, True, False)  # Flip image if player is facing left
            self.rect.center = (self.position[0], self.position[1]+15)

    def shoot(self, bullet_group, camera_offset):
        # Shoot a bullet if enough time has passed since last shot
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.cool_down:
            self.last_shot_time = current_time
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Adjust mouse position based on camera offset
            mouse_x -= camera_offset.x
            mouse_y -= camera_offset.y

            # Create and return a new bullet from the player's position
            bullet = self.bullet_class(self.player.get_position(), mouse_x, mouse_y, bullet_group)
            self.sound.play()
            return bullet



class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, target_x, target_y, group):
        super().__init__(group)
        self.pos = position
        self.image = pygame.Surface((10, 10))  # Create a bullet with a 10x10 surface
        self.image.fill((255, 0, 0))  # Set bullet color to red
        self.rect = self.image.get_rect(center=position)  # Set bullet's initial position

        self.speed = 25  # Set the bullet's speed

        # Calculate direction to the target (mouse position)
        self.dx = target_x - self.rect.centerx
        self.dy = target_y - self.rect.centery
        distance = math.sqrt(self.dx**2 + self.dy**2)

        # Normalize direction to unit vector
        if distance != 0:
            self.dx /= distance
            self.dy /= distance

    def update(self):
        # Move the bullet towards the target based on its speed
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        

