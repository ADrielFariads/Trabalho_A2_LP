"""
This module defines skills including their properties, behaviors, and interactions with the player. 
Implemented skills include healing, dashing, and attacks (e.g., Machine Gun), each with unique mechanics such as cooldowns 
and visual/sound effects.
"""

import pygame
import random
import math

import explosions
import config


class Skill:
    def __init__(self, name, cooldown, image):
        """
        Initializes the skill with a name, cooldown, image, and tracks the last used time.
        
        Args:
            name (str): The name of the skill.
            cooldown (int): The cooldown time in milliseconds.
            image (str): The path to the skill's image file.
        """
        self.name = name
        self.cool_down = cooldown
        self.image = pygame.image.load(image)
        self.last_used_time = 0
        self.is_on_cooldown = False
        self.unlock_level=0

    def use(self, player):
        """
        Executes the skill. This method should be overridden in subclasses for specific behavior.
        
        Args:
            player (Player): The player object who uses the skill.
        """
        pass

    def get_remaining_cooldown(self):
        """
        Returns the remaining cooldown time of the skill.
        
        Returns:
            int: The remaining cooldown time in milliseconds.
        """
        current_time = pygame.time.get_ticks()
        ellapsed_time = current_time - self.last_used_time
        return max(self.cool_down - ellapsed_time, 0)

    def update(self, player):
        """
        Updates the skill's cooldown status. If the skill is on cooldown, it checks if the cooldown is complete.
        
        Args:
            player (Player): The player object who owns the skill.
        """
        if self.is_on_cooldown:
            if self.get_remaining_cooldown() == 0:
                self.is_on_cooldown = False
                    

class Heal(Skill):

    def __init__(self):
        """
        Initializes the Heal skill with specific values for healing, cooldown, and image.

        This class inherits from the Skill class and represents a healing skill for the player.
        The skill heals the player by a specified value and has a cooldown.

        Attributes:
            key (str): The key assigned to use the skill.
            name (str): The name of the skill.
            cooldown (int): The cooldown time in milliseconds.
            heal_value (int): The amount of health restored by the skill.
            image (str): The file path for the skill's icon image.
            description (str): A brief description of the skill's effect.
        """
        self.key = "Q"
        self.name = "Heal"
        self.cooldown = 5000
        self.heal_value = 200
        self.image = "assets\\images\\icons\\heal_icon.png"
        self.description = f"Se cura em {self.heal_value} pontos de vida."
        super().__init__(self.name, self.cooldown, self.image)

    def use(self, player):
        """
        Uses the Heal skill to restore health to the player if they are not at full health 
        and the skill is not on cooldown.

        Args:
            player (Player): The player object who will be healed.
        """
        if player.current_health < player.max_health:
            if not self.is_on_cooldown:
                player.get_healed(self.heal_value)
                self.last_used_time = pygame.time.get_ticks()
                self.is_on_cooldown = True

class Adrenaline(Skill):
    def __init__(self):
        """
        Initializes the Adrenaline skill with specific values for speed boost, cooldown, duration, 
        and sound effect.

        This class inherits from the Skill class and represents a skill that temporarily increases 
        the player's movement speed. The skill has a cooldown and a duration for the speed boost.

        Attributes:
            key (str): The key assigned to use the skill.
            name (str): The name of the skill.
            cooldown (int): The cooldown time in milliseconds.
            duration (int): The duration of the speed boost in milliseconds.
            dash_end_time (int): The time when the speed boost should end.
            image (str): The file path for the skill's icon image.
            sound (pygame.mixer.Sound): The sound effect played when the skill is used.
            original_speed (int): The player's speed before the skill is used.
            description (str): A brief description of the skill's effect.
        """
        self.key = "E"
        self.name = "Adrenalina"
        self.cooldown = 5000
        self.duration = 3000
        self.dash_end_time = 0
        self.image = "assets\\images\\icons\\dash_icon.png"
        self.sound = pygame.mixer.Sound("assets\\audio\\skills\\dash_sound.wav")
        self.original_speed = 0
        self.description = f"Aumenta a velocidade de movimento durante {self.duration/1000} segundos."
        self.sound.set_volume(0.5)

        super().__init__(self.name, self.cooldown, self.image)

    def use(self, player):
        """
        Uses the Adrenaline skill to temporarily increase the player's movement speed 
        and starts the cooldown timer.

        Args:
            player (Player): The player object whose speed will be increased.
        """
        if not self.is_on_cooldown:
            self.original_speed = player.speed
            player.speed = self.original_speed + 5
            self.last_used_time = pygame.time.get_ticks()
            self.is_on_cooldown = True
            self.dash_end_time = pygame.time.get_ticks() + self.duration
            self.sound.play()

    def update(self, player):
        """
        Updates the Adrenaline skill status by checking if the speed boost duration has ended, 
        and if so, resets the player's speed to the original value.

        Args:
            player (Player): The player object whose speed is affected by the skill.
        
        Returns:
            None
        """
        if self.is_on_cooldown and pygame.time.get_ticks() >= self.dash_end_time:
            player.speed = self.original_speed
        return super().update(player)

    
class TimeManipulation(Skill):
    def __init__(self):
        """
        Initializes the Time Manipulation skill, which alters the space-time around the player,
        drastically slowing down enemy movement and animation speed for a short duration.

        This class inherits from the Skill class and represents a skill that affects enemies' 
        movement and animation speeds. The skill has a cooldown, duration, and a specific sound 
        effect when used.

        Attributes:
            key (str): The key assigned to use the skill.
            name (str): The name of the skill.
            description (str): A brief description of the skill's effect.
            cooldown (int): The cooldown time in milliseconds.
            image (str): The file path for the skill's icon image.
            duration (int): The duration of the skill's effect in milliseconds.
            end_time (int): The time when the skill's effect will end.
            sound (pygame.mixer.Sound): The sound effect played when the skill is used.
        """
        self.key = "E"
        self.name = "Manipulação temporal"
        self.description = "Altera o espaço-tempo ao seu redor, diminuindo drasticamente a velocidade dos inimigos. \nBladeMaster não é afetado pela lentidão."
        self.cooldown = 15000
        self.image = "assets\\images\\icons\\timemanipulation_icon.png"
        self.duration = 8000
        self.end_time = 0
        self.sound = pygame.mixer.Sound("assets\\audio\\skills\\heatbeating.wav")
        super().__init__(self.name, self.cooldown, self.image)
        self.unlock_level = 7

    def use(self, player):
        """
        Uses the Time Manipulation skill to slow down enemies by decreasing their movement and 
        animation speeds for a set duration.

        This method also starts the cooldown and plays the associated sound effect.

        Args:
            player (Player): The player object that uses the skill and affects nearby enemies.
        """
        if not self.is_on_cooldown:
            self.sound.play()
            for enemy in player.enemies:
                enemy.speed = max(enemy.speed/6, 2)  # Decreases enemy speed with a lower limit
                enemy.animation_speed = enemy.animation_speed * 2  # Increases animation speed
            self.last_used_time = pygame.time.get_ticks()
            self.is_on_cooldown = True
            self.end_time = pygame.time.get_ticks() + self.duration

    def update(self, player):
        """
        Updates the Time Manipulation skill status by checking if the effect duration has ended,
        and if so, resets the enemies' speed and animation speed to their original values.

        Args:
            player (Player): The player object whose enemies are affected by the skill.

        Returns:
            None
        """
        if self.is_on_cooldown and pygame.time.get_ticks() >= self.end_time:
            for enemy in player.enemies:
                enemy.speed = enemy.original_speed
                enemy.animation_speed = enemy.original_animation_speed
        return super().update(player)


class LethalTempo(Skill):
    """
    Represents the Lethal Tempo skill, where the cyborg energizes its gun, increasing the 
    firing rate and damage of each projectile for a short duration.

    This skill temporarily modifies the player's gun attributes, enhancing the damage and 
    reducing the cooldown between shots. The skill has a cooldown period and a specific 
    duration during which the effects are active.

    Attributes:
        key (str): The key assigned to use the skill.
        name (str): The name of the skill.
        description (str): A brief description of the skill's effect.
        cooldown (int): The cooldown time in milliseconds.
        image (str): The file path for the skill's icon image.
        duration (int): The duration of the skill's effect in milliseconds.
        end_time (int): The time when the skill's effect will end.
        original_damage (int): The original damage value of the player's gun before the skill is used.
        original_cooldown (int): The original cooldown value of the player's gun before the skill is used.
    """
    def __init__(self):
        self.key = "Q"
        self.name = "Ritmo letal"
        self.description = "Cyborg energiza sua metralhadora, aumentando a frequência de disparos e o dano de cada projétil."
        self.cooldown = 8000
        self.image = "assets\\images\\icons\\lethaltempo_icon.png"
        self.duration = 3500
        self.end_time = 0
        self.original_damage = 0
        self.original_cooldown = 0
        super().__init__(self.name, self.cooldown, self.image)
        self.unlock_level = 3

    def use(self, player):
        """
        Activates the Lethal Tempo skill, temporarily increasing the gun's damage and 
        decreasing the cooldown between shots for a set duration.

        This method modifies the player's gun attributes and starts the cooldown timer.

        Args:
            player (Player): The player object who activates the skill, affecting their gun.
        """
        if not self.is_on_cooldown:
            self.original_damage = player.gun.damage
            self.original_cooldown = player.gun.cool_down
            player.gun.cool_down = 500  # Reduces the cooldown between shots
            player.gun.damage += 25  # Increases the damage of each shot
            
            self.last_used_time = pygame.time.get_ticks()
            self.is_on_cooldown = True
            self.end_time = pygame.time.get_ticks() + self.duration

    def update(self, player):
        """
        Updates the Lethal Tempo skill status by checking if the effect duration has ended, 
        and if so, restores the gun's original damage and cooldown values.

        Args:
            player (Player): The player object whose gun attributes are affected by the skill.

        Returns:
            None
        """
        if self.is_on_cooldown and pygame.time.get_ticks() >= self.end_time:
            player.gun.damage = self.original_damage
            player.gun.cool_down = self.original_cooldown
        
        return super().update(player)


class IronWill(Skill):
    """
    Represents the Iron Will skill, where the Berserker enters a state of fury, drastically 
    reducing the damage taken from all sources for a short duration.

    This skill temporarily alters the player's armor attribute, reducing damage taken by 
    a significant percentage. The skill has a cooldown period and a specific duration during 
    which the effect is active.

    Attributes:
        key (str): The key assigned to use the skill.
        name (str): The name of the skill.
        description (str): A brief description of the skill's effect.
        cooldown (int): The cooldown time in milliseconds.
        image (str): The file path for the skill's icon image.
        duration (int): The duration of the skill's effect in milliseconds.
        end_time (int): The time when the skill's effect will end.
    """
    def __init__(self):
        self.key = "Q"
        self.name = "Vontade de Ferro"
        self.description = "O Berserker entra em um estado de fúria, reduzindo drasticamente o dano recebido de todas as fontes."
        self.cooldown = 15000
        self.image = "assets\\images\\icons\\berserker_icon.png"
        self.duration = 5000
        self.end_time = 0
        super().__init__(self.name, self.cooldown, self.image)
        self.unlock_level = 3

    def use(self, player):
        """
        Activates the Iron Will skill, reducing the player's damage taken from all sources 
        by a significant percentage for a short duration.

        This method modifies the player's armor attribute and starts the cooldown timer.

        Args:
            player (Player): The player object who activates the skill, affecting their armor.
        """
        if not self.is_on_cooldown:
            player.armor = 0.95  # Reduces damage taken by 95%
            self.last_used_time = pygame.time.get_ticks()
            self.is_on_cooldown = True
            self.end_time = pygame.time.get_ticks() + self.duration

    def update(self, player):
        """
        Updates the Iron Will skill status by checking if the effect duration has ended, 
        and if so, restores the player's original armor value.

        Args:
            player (Player): The player object whose armor is affected by the skill.

        Returns:
            None
        """
        if self.is_on_cooldown and pygame.time.get_ticks() >= self.end_time:
            player.armor = 0  # Resets the armor to its original state
        
        return super().update(player)
    

class Bloodlust(Skill):
    """
    Represents the Bloodlust skill, where the BladeMaster gains increased damage, 
    life steal from kills, but suffers increased damage from all sources for a short 
    duration.

    During the skill's effect, the player can deal more damage, heal by killing enemies, 
    but also receives increased damage from enemies. After the effect ends, the player's 
    attributes are restored to their original values.

    Attributes:
        key (str): The key assigned to use the skill.
        name (str): The name of the skill.
        description (str): A brief description of the skill's effect.
        cooldown (int): The cooldown time in milliseconds.
        image (str): The file path for the skill's icon image.
        duration (int): The duration of the skill's effect in milliseconds.
        end_time (int): The time when the skill's effect will end.
        original_damage (int): The player's original damage value before the skill is used.
        original_gun_cooldown (int): The original cooldown of the player's gun before the skill is used.
    """
    def __init__(self):
        self.key = "Q"
        self.name = "Sede de Sangue"
        self.description = "Por um breve período, BladeMaster causa mais dano, ataca com maior freqência e \n abater inimigos restaura vida, mas ele sofre dano aumentado de todas as fontes."
        self.cooldown = 12000
        self.image = "assets\\images\\icons\\bloodlust_icon.png"
        self.duration = 3500
        self.end_time = 0
        self.original_damage = 0
        self.original_gun_cooldown = 0
        super().__init__(self.name, self.cooldown, self.image)
        self.unlock_level = 3

    def use(self, player):
        """
        Activates the Bloodlust skill, increasing the player's damage, life steal, 
        and reducing the gun cooldown, while applying increased damage taken.

        Args:
            player (Player): The player object who activates the skill. The player's attributes
                             such as damage, gun cooldown, armor, and life steal are modified during the skill's effect.
        """
        if not self.is_on_cooldown:
            self.original_damage = player.gun.damage
            self.original_gun_cooldown = player.gun.cool_down
            player.life_steal = 50  # Increased life steal
            player.gun.damage *= 2  # Increased damage
            player.gun.cool_down = 200  # Reduced gun cooldown
            player.armor = -1  # Increased damage taken
            self.last_used_time = pygame.time.get_ticks()
            self.is_on_cooldown = True
            self.end_time = pygame.time.get_ticks() + self.duration

    def update(self, player):
        """
        Updates the Bloodlust skill status by checking if the effect duration has ended, 
        and if so, restores the player's original values for damage, gun cooldown, armor, and life steal.

        Args:
            player (Player): The player object whose attributes are affected by the skill.

        Returns:
            None
        """
        if self.is_on_cooldown and pygame.time.get_ticks() >= self.end_time:
            player.life_steal = 0  # Reset life steal
            player.armor = 0  # Reset armor
            player.gun.damage = self.original_damage  # Restore original damage
            player.gun.cool_down = self.original_gun_cooldown  # Restore original gun cooldown
        return super().update(player)

explosion_spritesheet = config.load_explosion_images()

class MissilRain(Skill):
    """
    Represents the Missile Rain skill, where the Cyborg commands multiple missiles to 
    rain down upon enemies, causing massive area damage upon impact.

    The skill launches a set number of missiles that spread in random directions. 
    Each missile creates an explosion that damages enemies within its range. The skill 
    has a cooldown period and cannot be used again until it has passed.

    Attributes:
        key (str): The key assigned to use the skill.
        name (str): The name of the skill.
        description (str): A brief description of the skill's effect.
        cooldown (int): The cooldown time in milliseconds.
        image (str): The file path for the skill's icon image.
        missile_number (int): The number of missiles launched during the skill's activation.
        explosion_damage (int): The damage dealt by each missile's explosion.
        last_used_time (int): The time when the skill was last used, used to track the cooldown.
    """
    def __init__(self):
        self.key = "E"
        self.name = "Chuva de Mísseis"
        self.description = "Comanda que limpem a área, lançando vários mísseis que exterminam os inimigos atingidos.    \nA quantidade de mísseis aumenta de acordo com a quantidade de inimigos abatidos."
        self.cooldown = 5000
        self.image = "assets\\images\\icons\\missiles_icon.png"
        super().__init__(self.name, self.cooldown, self.image) 
        # Explosion configuration
        self.killed_enemies = 0
        self.missile_number = 3
        self.explosion_damage = 5000
        self.last_used_time -= self.cooldown  # Ensures the skill is ready to use immediately
        self.unlock_level = 7

    def use(self, player):
        """
        Activates the Missile Rain skill, launching a series of missiles in random directions 
        and causing explosive damage to any enemies they hit.

        The skill launches a specified number of missiles that spread in the X and Y direction. 
        Each missile deals damage upon impact and triggers an explosion effect.

        Args:
            player (Player): The player object who activates the skill. The player's position 
                             and enemies are used to determine missile trajectory and target.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_used_time >= self.cooldown: 
            for i in range(self.missile_number):
                spread_value_x = random.randint(-500, 500)  # Random horizontal spread
                spread_value_y = random.randint(100, 500)  # Random vertical spread  
                pos = player.position
                # Create and launch missile with explosion parameters
                missile = explosions.Missile(
                    (pos.x + spread_value_x, -spread_value_y), 
                    (pos.x + spread_value_x, pos.y + spread_value_y), 
                    1, player.enemies, 300, self.explosion_damage, explosion_spritesheet, player.explosion_group
                )
                if i % 5 == 0:  
                    missile.muted = False
                    
                player.explosion_group.add(missile)  # Add missile to the explosion group
            
            self.last_used_time = current_time
            self.is_on_cooldown = True

    def update(self, player):
        """
        Updates the status of the Missile Rain skill. This method checks for cooldown 
        expiration and handles the cooldown reset when necessary.

        Args:
            player (Player): The player object using the skill. No specific update behavior 
                             is needed for the player, but this method is needed for consistency.

        Returns:
            None
        """
        self.killed_enemies = player.killed_enemies
        self.missile_number = 3 + math.floor(self.killed_enemies / 5)
        return super().update(player)

    
class GravitionVortex(Skill):
    """
    Represents the Gravition Vortex skill, which creates an area of increased gravity 
    that attracts enemies and enemy projectiles. Enemies within the explosion's center 
    are instantly obliterated. The Berserker is unaffected by the vortex.

    The skill launches a vortex at the mouse position, pulling enemies and projectiles 
    into the center and causing instant destruction of enemies in the core area. The vortex 
    lasts for a limited duration before it dissipates.

    Attributes:
        key (str): The key assigned to use the skill.
        name (str): The name of the skill.
        description (str): A brief description of the skill's effect.
        image (str): The file path for the skill's icon image.
        cooldown (int): The cooldown time in milliseconds.
        duration (int): The duration of the vortex effect in milliseconds.
        vortex (Vortex): The Vortex object representing the gravitational area.
    """
    def __init__(self):
        self.key = "E"
        self.name = "Campo Gravitacional"
        self.description = "Cria uma área de gravidade aumentada, atraindo inimigos e projeteis inimigos. Inimigos no centro da explosão são \n imediatamente obliterados. O Berserker não é afetado pelo Vortex."
        self.image = "assets\\images\\explosions\\vortex\\vortex.png"
        self.cooldown = 25000
        self.duration = 11000
        super().__init__(self.name, self.cooldown, self.image)
        self.last_used_time -= self.cooldown  # Ensures the skill is ready to use immediately
        self.unlock_level = 7

    def use(self, player):
        """
        Activates the Gravition Vortex skill, creating a gravitational field at the 
        mouse position that pulls enemies and projectiles into the vortex. Enemies 
        at the center of the vortex are instantly destroyed.

        Args:
            player (Player): The player object who activates the skill. The player's 
                             position and enemies are used to determine vortex placement 
                             and the affected targets.
        """
        current_time = pygame.time.get_ticks()  
        if current_time - self.last_used_time >= self.cooldown:  
            mouse_pos = pygame.mouse.get_pos()
            # Create the vortex and add it to the explosion group
            self.vortex = explosions.Vortex((mouse_pos - player.offset), 500, player.enemies, 500, self.duration)
            player.explosion_group.add(self.vortex)
            self.last_used_time = current_time
            # Add the particles of the vortex to the explosion group
            player.explosion_group.add(self.vortex.particles)
            self.is_on_cooldown = True

    def update(self, player):
        """
        Updates the status of the Gravition Vortex skill. This method checks the 
        cooldown and handles vortex destruction when its duration expires.

        Args:
            player (Player): The player object using the skill. The player's 
                             explosion group and vortex are updated here.

        Returns:
            None
        """
        if self.is_on_cooldown and pygame.time.get_ticks() - self.last_used_time > self.duration:
            self.vortex.kill()  # Remove the vortex when its duration ends
        return super().update(player)


########################## Guns' renders #####################################################################################################################################

class MachineGunRender(Skill):
    """
    Represents the Machine Gun skill, allowing the user to fire a rapid burst of bullets 
    at the target location.

    The skill has a cooldown and fires bullets when activated, typically used for 
    continuous damage in a short period.

    Attributes:
        key (str): The key assigned to use the skill.
        name (str): The name of the skill.
        cooldown (int): The cooldown time in milliseconds.
        image (str): The file path for the skill's icon image.
        description (str): A brief description of the skill's effect.
    """
    def __init__(self):
        self.key = "Ataque básico"
        self.name = "Metralhadora"
        self.cooldown = 500
        self.image = "assets\\images\\Guns\\machinegun1.png"
        self.description = f"Dispara uma saraivada de balas no local alvo."
        super().__init__(self.name, self.cooldown, self.image)


class KnifeThrowerRender(Skill):
    """
    Represents the Knife Thrower skill, which allows the user to throw a knife 
    at a target, causing significant damage.

    This skill has a cooldown and is designed for high-damage, single-target strikes.

    Attributes:
        key (str): The key assigned to use the skill.
        name (str): The name of the skill.
        cooldown (int): The cooldown time in milliseconds.
        image (str): The file path for the skill's icon image.
        description (str): A brief description of the skill's effect.
    """
    def __init__(self):
        self.key = "Ataque básico"
        self.name = "Arremesso de facas"
        self.cooldown = 750
        self.image = "assets\\images\\Guns\\Knifeicon.png"
        self.description = f"Arremessa uma adaga no alvo, causando grande quantidade de dano a um único alvo"
        super().__init__(self.name, self.cooldown, self.image)


class ShotgunRender(Skill):
    """
    Represents the Shotgun skill, which allows the user to fire a burst of pellets 
    in a cone shape. This skill causes significantly more damage to enemies at close range.

    The skill has a cooldown and is particularly effective at short distances.

    Attributes:
        key (str): The key assigned to use the skill.
        name (str): The name of the skill.
        cooldown (int): The cooldown time in milliseconds.
        image (str): The file path for the skill's icon image.
        description (str): A brief description of the skill's effect.
    """
    def __init__(self):
        self.key = "Ataque básico"
        self.name = "Espingarda"
        self.cooldown = 1500
        self.image = "assets\\images\\Guns\\Shotgun_icon.png"
        self.description = f"Dispara uma rajada de balas em cone. Causa MUITO mais dano em alvos próximos."
        super().__init__(self.name, self.cooldown, self.image)
        self.image = pygame.transform.scale(self.image, (50, 25))  # Resizing the image for the shotgun icon

