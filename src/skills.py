"""
This module defines skills including their properties, behaviors, and interactions with the player. 
Implemented skills include healing, dashing, and attacks (e.g., Machine Gun), each with unique mechanics such as cooldowns 
and visual/sound effects.
"""

import pygame

class Skill:
    def __init__(self, name, cooldown, image):
        self.name = name
        self.cool_down = cooldown
        self.image = pygame.image.load(image)
        self.last_used_time = 0
        self.is_on_cooldown = False

    def use(self, player):
        pass

    def get_remaining_cooldown(self):
        current_time = pygame.time.get_ticks()
        ellapsed_time = current_time - self.last_used_time
        return max(self.cool_down-ellapsed_time, 0)
    
    def update(self, player):
        if self.is_on_cooldown:
            if self.get_remaining_cooldown() == 0:
                self.is_on_cooldown = False
            
        

class Heal(Skill):
    def __init__(self):
        self.key = "Q"
        self.name = "Heal"
        self.cooldown = 5000
        self.heal_value = 200
        self.image = "assets\\images\\icons\\heal_icon.png"
        self.description = f"Se cura em {self.heal_value} pontos de vida."
        super().__init__(self.name, self.cooldown, self.image)

    def use(self, player):
        if player.current_health < player.max_health:
            if not self.is_on_cooldown:
                player.get_healed(self.heal_value)
                self.last_used_time = pygame.time.get_ticks()
                self.is_on_cooldown = True


class Dash(Skill):
    def __init__(self):
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
        if not self.is_on_cooldown:
            self.original_speed = player.speed
            player.speed = self.original_speed + 5
            self.last_used_time = pygame.time.get_ticks()
            self.is_on_cooldown = True
            self.dash_end_time = pygame.time.get_ticks() + self.duration
            self.sound.play()
            
    def update(self, player):
        if self.is_on_cooldown and pygame.time.get_ticks() >= self.dash_end_time:
            player.speed = self.original_speed
        return super().update(player)
    

class LethalTempo(Skill):
    def __init__(self):
        self.key = "Q"
        self.name = "Ritmo letal"
        self.description = "[personagem] energiza sua metralhadora, aumentando a quantidade de disparos."
        self.cooldown = 8000
        self.image = "assets\\images\\icons\\lethaltempo_icon.png"
        self.duration = 3500
        self.end_time = 0
        self.original_bullets = 0
        super().__init__(self.name, self.cooldown, self.image)        

    def use(self, player):
        if not self.is_on_cooldown:
            self.original_speed = player.gun.bullets
            player.gun.bullets = self.original_bullets + 10
            self.last_used_time = pygame.time.get_ticks()
            self.is_on_cooldown = True
            self.end_time = pygame.time.get_ticks() + self.duration

    def update(self, player):
        if self.is_on_cooldown and pygame.time.get_ticks() >= self.end_time:
            player.gun.bullets = self.original_speed
        return super().update(player)


class MachineGunRender(Skill):
    def __init__(self):
        self.key = "Botão Esquerdo"
        self.name = "Metralhadora"
        self.cooldown = 500
        self.image = "assets\\images\\icons\\machinegun_icon.png"
        self.description = f"Dispara uma saraivada de balas no local alvo."
        super().__init__(self.name, self.cooldown, self.image)

class KnifeThrowerRender(Skill):
    def __init__(self):
        self.key = "Botão Esquerdo"
        self.name = "Arremesso de facas"
        self.cooldown = 1000
        self.image = "assets\\images\\Guns\\Knifeicon.png"
        self.description = f"Arremessa uma faca no alvo, causando grande quantidade de dano."
        super().__init__(self.name, self.cooldown, self.image)

