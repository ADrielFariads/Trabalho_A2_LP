"""
This module provides the GameInterface class, responsible for rendering the player's health and experience bars, 
skill icons, and related interface elements. It includes logic for displaying health transitions, 
skill cooldowns, and tooltips with skill descriptions.
"""


import pygame

class GameInterface:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        self.experience_bar_lenght, self.health_bar_length = 500, 500
        self.health_change_speed = 2
        self.health_ratio = self.player.current_health/self.health_bar_length

        self.back_icon = pygame.image.load("assets\\images\\icons\\back_icon.png")
        self.back_icon = pygame.transform.scale(self.back_icon, (50,50))
        self.font = pygame.font.Font(None, 24)
        self.current_time = pygame.time.get_ticks()
        self.score_running = False
        self.time_paused = 0

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


    def experience_bar(self): #experience bar 
        experience_rect = pygame.Rect(10, 50, self.player.experience, 15)
        pygame.draw.rect(self.screen, (0, 0, 255), experience_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 50, self.experience_bar_lenght, 15), 2)
        
    def skills_interface(self): #skills interface

        icon_size = 44

        for i, skill in enumerate(self.player.skills):
            x_pos = 50 + (i * (icon_size + 10))
            y_pos = self.screen.get_height() - icon_size - 50

            skill_icon = pygame.transform.scale(skill.image, (icon_size, icon_size))
            self.screen.blit(self.back_icon, (x_pos, y_pos))
            self.screen.blit(skill_icon, (x_pos+3, y_pos+3))
            skill_icon_rect = pygame.Rect(x_pos, y_pos, icon_size, icon_size)

            if skill.is_on_cooldown: # cooldown animation
                surface = pygame.Surface((50, 50))
                surface.fill((30, 30, 30))
                surface.set_alpha(200)
                self.screen.blit(surface, (x_pos, y_pos))

            mouse_pos = pygame.mouse.get_pos()
            if skill_icon_rect.collidepoint(mouse_pos):
                self.render_tooltip(skill, mouse_pos)


    def render_tooltip(self, skill, mouse_pos): 
        text = f"[{skill.key}]:{skill.name} - tempo de recarga: {skill.cooldown/1000} segundos. \n {skill.description}"
        text_surface = self.font.render(text, True, (255, 255, 255))
        width, height = text_surface.get_size()
        height += 10

        tooltip_x = mouse_pos[0] + 10
        tooltip_y = mouse_pos[1] - height - 100

        
        pygame.draw.rect(self.screen, (0, 0, 0), (tooltip_x, tooltip_y, width + 10, height + 10))
        pygame.draw.rect(self.screen, (255, 255, 255), (tooltip_x, tooltip_y, width + 10, height + 10), 2)

        self.screen.blit(text_surface, (tooltip_x + 10, tooltip_y + 10))


    def status_render(self):
        pass
    
    def score_render(self):
        # Display the player's score (number of enemies killed)
        killed_enemies = self.player.killed_enemies
        score_text = f"Abates: {killed_enemies}"
        score_surface = self.font.render(score_text, True, (255, 255, 255))

        # Position the score at the top-right corner of the screen
        score_rect = score_surface.get_rect(topright=(self.screen.get_width() - 10, 10))
        self.screen.blit(score_surface, score_rect)

        # Timer - time survived since the game started
        if self.score_running:  # Only run the timer if 'score_running' is True
            time_survived = (pygame.time.get_ticks() - self.current_time + self.time_paused) / 1000  # Convert to seconds
        else:
            # Timer freezes when 'score_running' is False
            time_survived = self.time_paused / 1000  # Use the last recorded time when paused

        time_text = f"Tempo: {int(time_survived)}s"
        time_surface = self.font.render(time_text, True, (255, 255, 255))

        # Position the timer at the top-right corner of the screen, next to the score
        time_rect = time_surface.get_rect(topright=(self.screen.get_width() - 100, 10))
        self.screen.blit(time_surface, time_rect)

    def reset_game_status(self):
        # Reset game status such as score
        self.player.killed_enemies = 0
        self.current_time = pygame.time.get_ticks()  # Reset the starting time to current time
        self.time_paused = 0  # Reset the paused time when restarting the game
        self.score_running = True  # Ensure the timer starts running again when the game is restarted

    def pause_game(self):
        # Pauses the game and stores the current time
        self.score_running = False
        self.time_paused += pygame.time.get_ticks() - self.current_time  # Store the time that has passed until the pause

    def resume_game(self):
        # Resumes the game and restarts the timer
        self.score_running = True
        self.current_time = pygame.time.get_ticks()  

    def draw(self):
        self.experience_bar()
        self.health_bar()
        self.skills_interface()
        self.status_render()
        self.score_render()