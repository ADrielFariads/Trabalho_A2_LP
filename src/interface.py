import pygame

class GameInterface:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        self.experience_bar_lenght, self.health_bar_length = 500, 500
        self.health_change_speed = 2
        self.health_ratio = self.player.current_health/self.health_bar_length

        self.back_icon = pygame.image.load("assets\\images\\icons\\back_icon.png")
        self.back_icon = pygame.transform.scale(self.back_icon, (50, 50))

        self.current_time = pygame.time.get_ticks()

    def health_bar(self): #health bar 
        transition_width = 0
        transition_color = (255, 255, 255)
        health_bar_rect = pygame.Rect(10, 10, self.player.current_health/self.health_ratio, 15)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, 10, transition_width, 15)

        if self.player.current_health < self.player.target_health:
            self.player.current_health += self.health_change_speed
            transition_width = int((self.player.target_health-self.player.current_health)/self.health_ratio)
            transition_color = (0, 255, 0)
            transition_bar_rect = pygame.Rect(health_bar_rect.right, 10, transition_width, 15)

        if self.player.current_health > self.player.target_health:
            self.player.current_health -= self.health_change_speed
            transition_width = int(abs((self.player.target_health-self.player.current_health)/self.health_ratio))
            transition_color = (255, 255, 0) 
            transition_bar_rect = pygame.Rect(health_bar_rect.right - transition_width, 10, transition_width, 15)

        
        pygame.draw.rect(self.screen, (255, 0, 0), health_bar_rect)#health
        pygame.draw.rect(self.screen, transition_color, transition_bar_rect) #heal/damage animation
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 10, self.health_bar_length, 15), 2) #white rect arround the health


    def experience_bar(self):
        experience_rect = pygame.Rect(10, 50, self.player.experience, 15)
        pygame.draw.rect(self.screen, (0, 0, 255), experience_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 50, self.experience_bar_lenght, 15), 2)
        

    def skill_icon(self):
        icon_size = 50
        x_pos = 50
        y_pos = self.screen.get_height() - 75

        icon = pygame.transform.scale(self.player.skill_1_icon, (icon_size, icon_size))
        self.screen.blit(self.back_icon, (x_pos, y_pos))
        self.screen.blit(icon, (x_pos, y_pos))

        if self.player.skill_1_cooldown > 0:
            surface = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
            cooldown_rect = pygame.Rect(0,0, icon_size, icon_size)
            pygame.draw.rect(surface, (30, 30, 30), cooldown_rect)
            surface.set_alpha(200)

            self.screen.blit(surface, (x_pos, y_pos))