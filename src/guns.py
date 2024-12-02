"""
This module defines classes for implementing firearms and bullets in the game. It includes a base Gun class and a specialized MachineGun class, as well as a Bullet class for handling projectile behaviors. Guns can track player movements, shoot bullets towards the mouse cursor, and include cooldown mechanics. Each gun has unique features, such as different bullet bursts and sound effects.
"""

import pygame
import math
import random

import pygame

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, image, damage, cool_down, bullet, map_bounds):
        """
        Initialize the Gun class, which represents a weapon held by the player. The gun is positioned
        relative to the player and follows the player's movement. It can shoot bullets and has a cooldown 
        between shots.

        :param player: The player object that the gun will follow.
        :param image: The path to the image file of the gun.
        :param damage: The amount of damage the gun does with each shot.
        :param cool_down: The cooldown time in milliseconds between consecutive shots.
        :param bullet: The bullet class that will be used when the gun shoots.
        :param map_bounds: The bounds of the map for collision checks (not used directly in this code).
        """
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()  # Load gun image
        self.player = player  # Reference to the player
        self.z_index = 11

        # Format the image
        self.image_width, self.image_height = self.image.get_size()
        self.original_image = pygame.transform.scale(self.image, (self.image_width * 2, self.image_height * 2))

        self.position = self.player.rect.center  # Set initial gun position
        self.map_bounds = map_bounds

        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.player.rect.center)  # Get rect for the gun's position

        self.damage = damage  # Store gun damage value
        self.bullet_class = bullet  # Bullet class to use when shooting
        self.cool_down = cool_down  # Shooting cooldown in milliseconds
        self.last_shot_time = 0  # Time of the last shot

    def get_direction(self):
        """
        Get the direction from the gun to the mouse position, which is used to aim.

        :return: A Vector2 representing the direction to the mouse position.
        """
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())  # Get mouse position for aiming
        return mouse_position

    def update_position(self):
        """
        Update the gun's position to follow the player's position. This keeps the gun centered 
        relative to the player as they move.

        :return: None
        """
        self.position = self.player.rect.center

    def update(self):
        """
        Update the gun's position based on the player's movement. The gun's image is flipped
        depending on whether the player is facing left or right.

        :return: None
        """
        # Update gun's position based on player movement
        self.position = self.player.rect.center
        self.rect.center = (self.position[0]-10, self.position[1]+15)

        if self.player.facing_right:
            self.image = self.original_image
            self.rect.center = (self.position[0]-10, self.position[1]+15)
        else:
            self.image = pygame.transform.flip(self.original_image, True, False)  # Flip image if player is facing left
            self.rect.center = (self.position[0], self.position[1]+15)

class Bullet(pygame.sprite.Sprite): #standart bullet class
    """
    A class to represent a bullet fired from the gun. The bullet moves towards a target
    and deals damage on collision.

    Attributes:
    position (tuple): The initial position of the bullet (x, y).
    target_x (float): The x-coordinate of the target (e.g., mouse position).
    target_y (float): The y-coordinate of the target (e.g., mouse position).
    damage (int): The damage dealt by the bullet on impact.
    group (pygame.sprite.Group): The group to which the bullet belongs.
    """
    
    def __init__(self, position, target_x, target_y, damage, group):
        """
        Initialize the Bullet class. Sets the initial position, calculates the direction
        to the target, and prepares the bullet for movement.

        :param position: The initial position of the bullet (x, y).
        :param target_x: The x-coordinate of the target (e.g., mouse position).
        :param target_y: The y-coordinate of the target (e.g., mouse position).
        :param damage: The damage dealt by the bullet.
        :param group: The group to which the bullet belongs (used for sprite management).
        """
        super().__init__(group)
        self.pos = position
        self.image = pygame.Surface((10, 10))  # Create a bullet with a 10x10 surface
        self.rect = self.image.get_rect(center=position)  # Set bullet's initial position
        self.z_index = 8

        self.speed = 20  # Set the bullet's speed
        self.damage = damage

        # Calculate direction to the target (mouse position)
        self.dx = target_x - self.rect.centerx
        self.dy = target_y - self.rect.centery
        distance = math.sqrt(self.dx**2 + self.dy**2)

        # Normalize direction to unit vector
        if distance != 0:
            self.dx /= distance
            self.dy /= distance

    def update(self):
        """
        Update the bullet's position based on its speed. The bullet moves towards the target.
        If the speed reaches a threshold (1000), the bullet is removed from the group.

        :return: None
        """
        # Move the bullet towards the target based on its speed
        self.speed += 1
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        # Remove the bullet when its speed exceeds a threshold
        if self.speed >= 1000:
            self.kill()


############ cyborg's machine gun logic ########################
class MachineGun(Gun):
    """
    A class to represent a machine gun, which fires multiple bullets in rapid succession.

    Inherits from the Gun class and extends its functionality to allow rapid fire.
    Plays a sound when shooting and handles bullet creation.

    Attributes:
    player (Player): The player object that the gun belongs to.
    map_bounds (pygame.Rect): The bounds of the map to constrain gun movement.
    sound (pygame.mixer.Sound): Sound to be played when shooting.
    bullets (int): The number of bullets fired in a single shot.
    """
    
    def __init__(self, player, map_bounds):
        """
        Initialize the MachineGun class with specific attributes like damage, cooldown, 
        bullet class, and sound.

        :param player: The player object that the gun belongs to.
        :param map_bounds: The bounds of the map to constrain gun movement.
        """
        texture = "assets\\images\\Guns\\machinegun.png"
        damage = 50
        self.cool_down = 1000  # Cooldown between shots in milliseconds
        self.bullets = 5  # Number of bullets fired in a single shot
        
        bullet_class = Bullet  # Bullet class to be used
        self.sound = pygame.mixer.Sound("assets\\audio\\gun\\machine_gun.wav")
        self.sound.set_volume(0.5)
        
        super().__init__(player, texture, damage, self.cool_down, bullet_class, map_bounds)

    def shoot_single_bullet(self, bullet_group, camera_offset):
        """
        Creates a single bullet to be fired.

        :param bullet_group: The group to which the bullet will be added.
        :param camera_offset: The camera offset used to adjust mouse position.
        :return: A Bullet object.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Adjust the mouse position considering the camera offset
        mouse_x -= camera_offset.x
        mouse_y -= camera_offset.y

        # Create and return a single bullet
        bullet = self.bullet_class(self.position, mouse_x, mouse_y, self.damage, bullet_group)
        return bullet  

    def shoot(self, bullet_group, offset, all_sprites_group):
        """
        Fires a burst of bullets. Multiple bullets are fired with a slight delay between each shot.

        :param bullet_group: The group to which the bullets will be added.
        :param offset: The offset of the camera used to adjust mouse position.
        :param all_sprites_group: The group to which all sprites belong.
        """
        current_time = pygame.time.get_ticks()
        mouse_x, mouse_y = pygame.mouse.get_pos() - offset
        dx = mouse_x - self.position[0]
        dy = mouse_y - self.position[1]
        
        # Update player's facing direction based on the mouse position
        if dx > 0: 
            self.player.facing_right = True
        elif dx < 0: 
            self.player.facing_right = False

        if current_time - self.last_shot_time >= self.cool_down:
            self.last_shot_time = current_time
            num_bullets = self.bullets  # Number of bullets fired in one burst
            self.sound.play()  # Play shooting sound

            for i in range(num_bullets):
                bullet = self.shoot_single_bullet(bullet_group, offset)
                
                # Load and scale the bullet's image
                image = pygame.image.load("assets\\images\\Bullets\\7.png")
                width = image.get_width()
                height = image.get_height()

                bullet.image = pygame.transform.scale(image, ((int(width * 2)), (int(height * 2))))
                bullet.speed -= i  # Adjust speed for each bullet in the burst
                all_sprites_group.add(bullet)  # Add the bullet to the group


########### Knife thrower logic ###########################
class Knife(Bullet):
    """
    A class representing a knife as a bullet, which has a specific angle of travel
    and decreases in speed until it is destroyed.

    Inherits from the Bullet class, adding functionality specific to the knife's behavior.
    
    Attributes:
    angle (float): The angle at which the knife is shot.
    speed (int): The speed of the knife, which decreases over time.
    initial_position (tuple): The starting position of the knife.
    """
    
    def __init__(self, position, target_x, target_y, damage, group):
        """
        Initializes the Knife with a specific position, target, damage, and group.

        :param position: The initial position of the knife.
        :param target_x: The target x-coordinate.
        :param target_y: The target y-coordinate.
        :param damage: The damage dealt by the knife.
        :param group: The group to which the knife belongs (for sprite management).
        """
        super().__init__(position, target_x, target_y, damage, group)

        # Calculate the angle at which the knife is shot
        self.angle = math.degrees(math.atan2(-self.dy, self.dx))  # Converts radian to degree
        self.speed = 25  # Initial speed of the knife
        self.initial_position = position  # Store the initial position of the knife

    def update(self):
        """
        Updates the knife's position, reducing its speed over time.
        The knife is destroyed if its speed falls below or equal to 10.

        :return: Calls the parent class's update method to move the knife.
        """
        self.speed -= 1  # Decrease speed over time
        if self.speed <= 10:
            self.kill()  # Destroy the knife if speed is too low

        return super().update()  # Call the update method from Bullet class to move the knife
        
class KnifeThrower(Gun):
    """
    A class representing the Knife Thrower, a weapon that shoots knives towards the mouse cursor.
    
    Inherits from the Gun class, with specific functionality for throwing knives.
    
    Attributes:
    cool_down (int): The cooldown time between each shot in milliseconds.
    original_image (Surface): The original image of the Knife Thrower, rotated and resized.
    sound (Sound): The sound effect played when a knife is thrown.
    """
    
    def __init__(self, player, map_bounds):
        """
        Initializes the Knife Thrower with a specific player, texture, damage, speed, 
        and map bounds. Also prepares the sound effect and image for the weapon.

        :param player: The player object, which this weapon belongs to.
        :param map_bounds: The bounds of the map, used to limit the weapon's range.
        """
        texture = "assets\\images\\Guns\\Knifeicon.png"
        damage = 200
        speed = 750
        self.bullets = 1
         
        bullet_class = Knife  
        super().__init__(player, texture, damage, speed, bullet_class, map_bounds)
        
        self.cool_down = 750  # Cooldown time between shots (milliseconds)
        
        # Load and prepare the weapon's image
        self.original_image = pygame.transform.scale(self.image, (30, 30))
        self.original_image = pygame.transform.rotate(self.original_image, -60)
        self.image = self.original_image
        
        # Load and configure the sound for the knife throw
        self.sound = pygame.mixer.Sound("assets\\audio\\gun\\knife_sound.wav")
    
    def shoot_a_knife(self, bullet_group, camera_offset):
        """
        Creates and returns a knife object that is thrown towards the mouse cursor.

        :param bullet_group: The group of bullets to which the knife will be added.
        :param camera_offset: The offset of the camera, used to adjust the position of the mouse.
        :return: The created Knife object.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Adjust the mouse position considering the camera offset
        mouse_x -= camera_offset.x
        mouse_y -= camera_offset.y

        # Create a new knife and return it
        bullet = self.bullet_class(self.position, mouse_x, mouse_y, self.damage, bullet_group)
        return bullet  
    
    def shoot(self, bullet_group, offset, all_sprites_group):
        """
        Shoots a knife towards the mouse cursor, if the cooldown has passed.
        Plays the shooting sound and updates the position and rotation of the knife.

        :param bullet_group: The group of bullets to which the knife will be added.
        :param offset: The camera offset used to adjust the mouse position.
        :param all_sprites_group: The group containing all sprites for the game.
        """
        current_time = pygame.time.get_ticks()
        mouse_x, mouse_y = pygame.mouse.get_pos() - offset
        dx = mouse_x - self.position[0]
        dy = mouse_y - self.position[1]
        
        # Update the player's facing direction based on mouse position
        if dx > 0: 
            self.player.facing_right = True
        elif dx < 0: 
            self.player.facing_right = False
        
        if current_time - self.last_shot_time >= self.cool_down:
            self.last_shot_time = current_time
            
            # Create and configure the knife
            bullet = self.shoot_a_knife(bullet_group, offset)
            image = pygame.image.load("assets\\images\\Guns\\Knifeicon.png")
            image = pygame.transform.scale(image, (20, 20))

            # Adjust the image, position, and rotation of the knife
            bullet.image = pygame.transform.scale(image, (30, 30))
            bullet.image = pygame.transform.rotate(bullet.image, bullet.angle - 45)
            bullet.rect = bullet.image.get_rect(center=bullet.initial_position)
            
            # Add the knife to the all sprites group and play the sound
            all_sprites_group.add(bullet)
            self.sound.play()

    def update(self):
        """
        Updates the Knife Thrower's position based on the player's movement. 
        Flips the image if the player is facing left.

        The position of the gun follows the player's position, and the image 
        is adjusted accordingly.
        """
        # Update the gun's position based on the player's position
        self.position = self.player.rect.center
        self.rect.center = (self.position[0] - 10, self.position[1] + 30)

        # If the player is facing right, show the original image
        if self.player.facing_right:
            self.image = self.original_image
            self.rect.center = (self.position[0] - 10, self.position[1] + 30)
        else:
            # If the player is facing left, flip the image
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.rect.center = (self.position[0] + 15, self.position[1] + 30)



############ Shot Gun logic ###############################
class Shotgun_bullets(Bullet):
    """
    A class representing a shotgun bullet, which behaves differently than regular bullets
    by gradually slowing down and decreasing damage over time.

    Inherits from the Bullet class and modifies the speed and damage mechanics for shotgun-style bullets.

    Attributes:
    speed (int): The initial speed of the shotgun bullet, which decreases over time.
    """
    
    def __init__(self, position, target_x, target_y, damage, group):
        """
        Initializes the Shotgun_bullets with a specific position, target, damage, and group.

        :param position: The starting position of the bullet (where it is fired).
        :param target_x: The x-coordinate of the target (mouse position).
        :param target_y: The y-coordinate of the target (mouse position).
        :param damage: The damage dealt by the shotgun bullet.
        :param group: The sprite group to which the bullet will be added.
        """
        super().__init__(position, target_x, target_y, damage, group)
        self.speed = 50  # Initial speed of the shotgun bullet
        
    def update(self):
        """
        Updates the shotgun bullet's position based on its speed and gradually decreases its speed and damage.
        If the speed of the bullet becomes too slow (below a threshold), it is removed from the game.

        This method also decreases the bullet's damage as it travels.

        :return: None
        """
        # Move the bullet towards the target based on its speed
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        # Gradually decrease the bullet's damage and speed
        self.damage -= self.speed
        self.speed -= 3

        # If speed is too low, remove the bullet from the group (kill it)
        if self.speed <= 5:
            self.kill()


class Shotgun(Gun):
    """
    A class representing a shotgun, which fires multiple bullets in a spread pattern,
    with a cooldown time between shots and a reload sound.

    Inherits from the Gun class and modifies the shooting behavior to fire multiple bullets 
    in a spread, with adjustments to the bullet's angle and speed.

    Attributes:
    shoot_sound (pygame.mixer.Sound): The sound effect for shooting the shotgun.
    reload_sound (pygame.mixer.Sound): The sound effect for reloading the shotgun.
    reload_muted (bool): Flag to prevent the reload sound from playing too frequently.
    sound_delay (int): The delay time before the reload sound can be played.
    """
    
    def __init__(self, player, map_bounds):
        """
        Initializes the Shotgun with specific properties such as damage, bullet class, and sound effects.

        :param player: The player object who is using the shotgun.
        :param map_bounds: The boundaries of the map, which may affect the shooting area.
        """
        texture = "assets\\images\\Guns\\Shotgun_icon.png"
        damage = 350
        self.cool_down = 1500  # Cooldown time between shots in milliseconds
        self.bullets = 25  # Number of bullets fired per shot
        self.shoot_sound = pygame.mixer.Sound("assets\\audio\\gun\\shotgun_sound.wav")
        self.reload_sound = pygame.mixer.Sound("assets\\audio\\gun\\shotgun_reload.wav")
        self.reload_sound.set_volume(0.5)
        self.reload_muted = True
        bullet_class = Shotgun_bullets  
        self.sound_delay = (self.shoot_sound.get_length() * 1000) / 2  # Half of the shoot sound duration
        super().__init__(player, texture, damage, self.cool_down, bullet_class, map_bounds)

        self.original_image = pygame.transform.rotate(self.image, -45)
        self.original_image = pygame.transform.scale_by(self.original_image, 0.8)  # Scale the shotgun image

    def shoot_single_bullet(self, bullet_group, camera_offset):
        """
        Creates a single bullet for the shotgun.

        :param bullet_group: The group to which the bullet will be added.
        :param camera_offset: The offset to adjust the mouse position based on the camera view.
        :return: A shotgun bullet object.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Adjust the mouse position considering the camera offset
        mouse_x -= camera_offset.x
        mouse_y -= camera_offset.y

        # Creates a single bullet 
        bullet = self.bullet_class(self.position, mouse_x, mouse_y, self.damage, bullet_group)
        return bullet 

    def shoot(self, bullet_group, offset, all_sprites_group):
        """
        Shoots a spread of bullets from the shotgun, adjusting their angles and speeds.
        Plays shooting and reloading sounds at appropriate times.

        :param bullet_group: The group to which the bullets will be added.
        :param offset: The offset of the camera in relation to the player's position.
        :param all_sprites_group: The group that contains all sprites for rendering.
        """
        current_time = pygame.time.get_ticks()
        mouse_x, mouse_y = pygame.mouse.get_pos() - offset
        dx = mouse_x - self.position[0]
        dy = mouse_y - self.position[1]
        
        if dx > 0: 
            self.player.facing_right = True
        elif dx < 0: 
            self.player.facing_right = False
        
        # Play reload sound if the delay is reached
        if current_time - self.last_shot_time >= self.sound_delay and not self.reload_muted:
            self.reload_sound.play()
            self.reload_muted = True
        
        # Check if enough time has passed for the next shot
        if current_time - self.last_shot_time >= self.cool_down:
            self.last_shot_time = current_time
            num_bullets = self.bullets
            self.shoot_sound.play()

            angle = math.degrees(math.atan2(dy, dx))  # Calculate the base angle of the shot

            for i in range(num_bullets):
                # Add random spread to the bullet's angle
                angle_variation = random.randint(-10, 10)
                new_angle = angle + angle_variation

                # Calculate the new direction for the bullet
                new_dx = math.cos(math.radians(new_angle))
                new_dy = math.sin(math.radians(new_angle))

                bullet = self.shoot_single_bullet(bullet_group, offset)
                bullet.dx = new_dx
                bullet.dy = new_dy
                image = pygame.image.load("assets\\images\\Bullets\\7.png")

                # Resize the bullet image and add to the sprites group
                width = image.get_width()
                height = image.get_height()
                bullet.image = pygame.transform.scale(image, ((int(width*2)), (int(height*2))))
                all_sprites_group.add(bullet)

                # Add a random speed variation for each bullet
                bullet.speed += random.randint(1, 5)
            
            self.reload_muted = False  # Allow reload sound to play again for next shot

    def update(self):
        """
        Updates the shotgun's position and orientation based on the player's movement.
        Flips the shotgun's image when the player faces the opposite direction.

        :return: None
        """
        # Update gun's position based on player movement
        self.position = self.player.rect.center
        self.rect.center = (self.position[0], self.position[1])

        # Adjust the image of the shotgun depending on the player's direction
        if self.player.facing_right:
            self.image = self.original_image
            self.rect.center = (self.position[0]-10, self.position[1]+10)
        else:
            self.image = pygame.transform.flip(self.original_image, True, False)  # Flip image if player is facing left
            self.rect.center = (self.position[0], self.position[1]+10)
