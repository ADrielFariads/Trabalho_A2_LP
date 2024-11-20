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
    
    def update(self):
        if self.is_on_cooldown:
            if self.get_remaining_cooldown() == 0:
                self.is_on_cooldown = False
            
        

class Heal(Skill):
    def __init__(self):
        self.name = "Heal"
        self.cool_down = 5000
        self.image = "assets\\images\\icons\\heal_icon.png"
        super().__init__(self.name, self.cool_down, self.image)

    def use(self, player):
        if player.current_health < player.max_health:
            if not self.is_on_cooldown:
                player.get_healed(200)
                self.last_used_time = pygame.time.get_ticks()
                self.is_on_cooldown = True
