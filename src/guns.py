"""
This module defines classes for implementing firearms and bullets in the game. It includes a base Gun class and a specialized MachineGun class, as well as a Bullet class for handling projectile behaviors. Guns can track player movements, shoot bullets towards the mouse cursor, and include cooldown mechanics. Each gun has unique features, such as different bullet bursts and sound effects.
"""

import pygame
import math
import random

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, image, damage, cool_down, bullet, map_bounds):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()  # Load gun image
        self.player = player  # Reference to the player

        # Format the image
        self.image_width, self.image_height = self.image.get_size()
        self.original_image = pygame.transform.scale(self.image, (self.image_width * 2, self.image_height * 2))

        self.position = self.player.rect.center  # Set initial gun position
        self.map_bounds = map_bounds

        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.player.rect.center)  # Get rect for the gun's position

        self.base_damage = damage  # Store gun damage value
        self.bullet_class = bullet  # Bullet class to use when shooting
        self.cool_down = cool_down  # Shooting cooldown in milliseconds
        self.last_shot_time = 0  # Time of the last shot

    def get_direction(self):
        # Get the direction to the mouse position
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())  # Get mouse position for aiming
        return mouse_position

    def update_position(self):
        # Update the gun's position to follow the player's position
        self.position = self.player.rect.center
        

    def update(self):
        # Update gun's position based on player movement
        self.position = self.player.rect.center
        self.rect.center = (self.position[0]-10, self.position[1]+15)
        if self.player.facing_right:
            self.image = self.original_image
            self.rect.center = (self.position[0]-10, self.position[1]+15)
        else:
            self.image = pygame.transform.flip(self.original_image, True, False)  # Flip image if player is facing left
            self.rect.center = (self.position[0], self.position[1]+15)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, target_x, target_y,damage, group):
        super().__init__(group)
        self.pos = position
        self.image = pygame.Surface((10, 10))  # Create a bullet with a 10x10 surface
        self.rect = self.image.get_rect(center=position)  # Set bullet's initial position

        self.speed = 20 # Set the bullet's speed
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
        # Move the bullet towards the target based on its speed
        self.speed +=1
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if self.speed >= 1000:
            self.kill()


############ cyborg's machine gun logic ########################
class MachineGun(Gun):
    def __init__(self, player, map_bounds):
        texture = "assets\\images\\Guns\\machinegun.png"
        damage = 50
        self.cool_down = 500
        self.bullets = 5
         
        bullet_class = Bullet  
        self.sound = pygame.mixer.Sound("assets\\audio\\gun\\machine_gun.wav")
        self.sound.set_volume(0.5)
        super().__init__(player, texture, damage, self.cool_down, bullet_class, map_bounds)
        
    def shoot_single_bullet(self, bullet_group, camera_offset):
        """
        creates a single shoot
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Ajusts the mouse position considering the camera offset
        mouse_x -= camera_offset.x
        mouse_y -= camera_offset.y

        # Creates a single bullet 
        bullet = self.bullet_class(self.position, mouse_x, mouse_y, self.base_damage, bullet_group)
        return bullet  
    
    def shoot(self, bullet_group, offset, all_sprites_group):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_shot_time >= self.cool_down:
            self.last_shot_time = current_time
            num_bullets = self.bullets
            self.sound.play()

            for i in range(num_bullets):
                bullet = self.shoot_single_bullet(bullet_group, offset)
                image = pygame.image.load("assets\\images\\Bullets\\7.png")

                width = image.get_width()
                height = image.get_height()

                bullet.image = pygame.transform.scale(image, ((int(width*2)), (int(height*2))))
                bullet.speed -= i*2
                all_sprites_group.add(bullet)


########### Knife thrower logic ###########################
class Knife(Bullet):
    def __init__(self, position, target_x, target_y, damage, group):
        super().__init__(position, target_x, target_y, damage, group)

        self.angle = math.degrees(math.atan2(-self.dy, self.dx)) ##calculates the angle for knife shooting
        self.speed = 5
        self.initial_position = position
        
class KnifeThrower(Gun):

    def __init__(self, player, map_bounds):
        texture = "assets\\images\\Guns\\Knifeicon.png"
        damage = 100
        speed = 1000
        self.bullets = 1
         
        bullet_class = Knife  
        super().__init__(player, texture, damage, speed, bullet_class, map_bounds)
        
        self.cool_down = 500
        self.original_image = pygame.transform.scale(self.image, (30,30))
        self.original_image = pygame.transform.rotate(self.original_image, -60)
        self.image = self.original_image


    def shoot_a_knife(self, bullet_group, camera_offset):

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Ajusts the mouse position considering the camera offset
        mouse_x -= camera_offset.x
        mouse_y -= camera_offset.y

        # Creates a single knife 
        bullet = self.bullet_class(self.position, mouse_x, mouse_y, self.base_damage, bullet_group)
        return bullet  
    
    def shoot(self, bullet_group, offset, all_sprites_group):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_shot_time >= self.cool_down:
            self.last_shot_time = current_time
            bullet = self.shoot_a_knife(bullet_group, offset)
            image = pygame.image.load("assets\\images\\Guns\\Knifeicon.png")
            image = pygame.transform.scale(image, (20, 20))

            bullet.image = pygame.transform.scale(image, (30, 30))
            bullet.image = pygame.transform.rotate(bullet.image, bullet.angle - 45)
            bullet.rect = bullet.image.get_rect(center=bullet.initial_position)
            all_sprites_group.add(bullet)

    def update(self):
        # Update gun's position based on player movement
        self.position = self.player.rect.center
        self.rect.center = (self.position[0]-10, self.position[1]+30)
        if self.player.facing_right:
            self.image = self.original_image
            self.rect.center = (self.position[0]-10, self.position[1]+30)
        else:
            self.image = pygame.transform.flip(self.original_image, True, False)  # Flip image if player is facing left
            self.rect.center = (self.position[0]+15, self.position[1]+30)



############ Shot Gun logic ###############################
class Shotgun_bullets(Bullet):
    def __init__(self, position, target_x, target_y, damage, group):
        super().__init__(position, target_x, target_y, damage, group)
        self.speed = 50
        
    def update(self):
        # Move the bullet towards the target based on its speed
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        self.speed -=3
        if self.speed <= 5:
            self.kill()


class Shotgun(Gun):
    def __init__(self, player, map_bounds):
        texture = "assets\\images\\Guns\\Shotgun.png"
        damage = 10
        speed = 2000
        self.bullets = 10
        self.sound = pygame.mixer.Sound("assets\\audio\\gun\\shotgun_sound.wav")
        bullet_class = Shotgun_bullets  
        super().__init__(player, texture, damage, speed, bullet_class, map_bounds)

    def shoot_single_bullet(self, bullet_group, camera_offset):
        """
        creates a single shoot
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Ajusts the mouse position considering the camera offset
        mouse_x -= camera_offset.x
        mouse_y -= camera_offset.y

        # Creates a single bullet 
        bullet = self.bullet_class(self.position, mouse_x, mouse_y, self.base_damage, bullet_group)
        return bullet 

    def shoot(self, bullet_group, offset, all_sprites_group):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_shot_time >= self.cool_down:
            self.last_shot_time = current_time
            num_bullets = self.bullets
            self.sound.play()

            mouse_x, mouse_y = pygame.mouse.get_pos() - offset
            dx = mouse_x - self.position[0]
            dy = mouse_y - self.position[1]
            angle = math.degrees(math.atan2(dy, dx))

            for i in range(num_bullets):

                angle_variation = random.randint(-10, 10)
                new_angle = angle + angle_variation

                new_dx = math.cos(math.radians(new_angle))
                new_dy = math.sin(math.radians(new_angle))


                bullet = self.shoot_single_bullet(bullet_group, offset)
                bullet.dx = new_dx
                bullet.dy = new_dy
                image = pygame.image.load("assets\\images\\Bullets\\7.png")

                width = image.get_width()
                height = image.get_height()
                bullet.image = pygame.transform.scale(image, ((int(width*2)), (int(height*2))))
                all_sprites_group.add(bullet)
                bullet.speed += random.randint(1, 3)

    