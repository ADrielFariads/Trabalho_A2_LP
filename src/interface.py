"""
    This module provides the GameInterface class, responsible for rendering the player's health and experience bars, 
    skill icons, and related interface elements. It includes logic for displaying health transitions, 
    skill cooldowns, and tooltips with skill descriptions.
"""

import pygame 

playing_status = False # Global variable to facilitate control of match status

class GameInterface:
    def __init__(self, screen, player):
        """
        Initializes the GameInterface object with necessary parameters for rendering.

        Args:
            screen (pygame.Surface): The pygame surface representing the game screen.
            player (Player): The player object whose stats will be displayed.
        """
        self.screen = screen
        self.player = player

        self.experience_bar_lenght, self.health_bar_length = 400, 500
        self.health_change_speed = 2
        self.health_ratio = self.player.current_health / self.health_bar_length
        self.experience_ratio = self.player.experience_needed / self.experience_bar_lenght
        
        self.back_icon = pygame.image.load("assets\\images\\icons\\back_icon.png")
        self.back_icon = pygame.transform.scale(self.back_icon, (50, 50))
        self.font = pygame.font.Font(None, 24)
        self.current_time = pygame.time.get_ticks()
        self.score_running = False
        self.time_paused = 0

    def health_bar(self):
        """
        Renders the player's health bar on the screen with dynamic health changes.

        The health bar is updated based on the player's current health and target health.
        It also includes animations for healing or damage transitions.
        """
        transition_width = 0
        transition_color = (255, 255, 255)
        health_bar_rect = pygame.Rect(10, 10, self.player.current_health / self.health_ratio, 15)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, 10, transition_width, 15)

        if self.player.current_health < self.player.target_health:
            self.player.current_health += self.health_change_speed
            transition_width = int((self.player.target_health - self.player.current_health) / self.health_ratio)
            transition_color = (0, 255, 0)
            transition_bar_rect = pygame.Rect(health_bar_rect.right, 10, transition_width, 15)

        if self.player.current_health > self.player.target_health:
            self.player.current_health -= self.health_change_speed
            transition_width = int(abs((self.player.target_health - self.player.current_health) / self.health_ratio))
            transition_color = (255, 255, 0) 
            transition_bar_rect = pygame.Rect(health_bar_rect.right - transition_width, 10, transition_width, 15)

        pygame.draw.rect(self.screen, (255, 0, 0), health_bar_rect)  # Health bar
        pygame.draw.rect(self.screen, transition_color, transition_bar_rect)  # Heal/damage animation
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 10, self.health_bar_length, 15), 2)  # Border around the health bar

    def experience_bar(self):
        """
        Renders the player's experience bar on the screen.

        The experience bar's length is determined by the player's experience.
        """
        experience_rect = pygame.Rect(10, 50, self.player.experience/self.experience_ratio, 15)
        border_rect = pygame.Rect(10, 50, self.experience_bar_lenght, 15)

        font = pygame.font.Font("assets\\images\\Fonts\\CyberpunkCraftpixPixel.otf", 20)

        if self.player.current_level < 10:
            level_text = f"nivel {self.player.current_level}"
        else:
            level_text = f"nivel maximo"
            experience_rect = pygame.Rect(10, 50, self.experience_bar_lenght, 15)
        text_surface = font.render(level_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(midleft=(border_rect.right + 10, border_rect.centery))
        
        pygame.draw.rect(self.screen, (0, 0, 255), experience_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 50, self.experience_bar_lenght, 15), 2)
        self.screen.blit(text_surface, text_rect)

    def skills_interface(self):
        """
        Renders the player's skills interface on the screen.

        Displays skill icons and shows cooldowns and tooltips when the player hovers over the icons.
        """
        icon_size = 44

        for i, skill in enumerate(self.player.skills):
            x_pos = 50 + (i * (icon_size + 10))
            y_pos = self.screen.get_height() - icon_size - 50

            skill_icon = pygame.transform.scale(skill.image, (icon_size, icon_size))
            self.screen.blit(self.back_icon, (x_pos, y_pos))
            self.screen.blit(skill_icon, (x_pos + 3, y_pos + 3))
            skill_icon_rect = pygame.Rect(x_pos, y_pos, icon_size, icon_size)

            if self.player.current_level < skill.unlock_level:
                surface = pygame.Surface((50, 50))
                surface.fill((30, 30, 30))
                surface.set_alpha(200)
                self.screen.blit(surface, (x_pos, y_pos))

            if skill.is_on_cooldown:  # Cooldown animation
                surface = pygame.Surface((50, 50))
                surface.fill((30, 30, 30))
                surface.set_alpha(200)
                self.screen.blit(surface, (x_pos, y_pos))

            mouse_pos = pygame.mouse.get_pos()
            if skill_icon_rect.collidepoint(mouse_pos):
                self.render_tooltip(skill, mouse_pos)

    def render_tooltip(self, skill, mouse_pos):
        """
        Renders a tooltip for the skill when the player hovers over its icon.

        Args:
            skill (Skill): The skill object to display information about.
            mouse_pos (tuple): The mouse cursor's position on the screen.
        """
        text_font = pygame.font.Font("assets\\images\\Fonts\\ShareTech-Regular.ttf", 16)
        render_font = pygame.font.Font("assets\\images\\Fonts\\CyberpunkCraftpixPixel.otf", 14)

        locked_text = f"HABILIDADE DESBLOQUEIA NO NIVEL {skill.unlock_level}!"
        unlocked_text = "HABILIDADE DESBLOQUEADA"

        skill_text = f"[{skill.key}]: {skill.name} - tempo de recarga: {skill.cooldown / 1000} segundos.\n{skill.description}"

        if self.player.current_level < skill.unlock_level:
            skill_status_surface = render_font.render(locked_text, True, (255, 255, 0))
        else:
            skill_status_surface = render_font.render(unlocked_text, True, (50, 255, 50))

        text_surface = text_font.render(skill_text, True, (255, 255, 255))

        width = max(skill_status_surface.get_width(), text_surface.get_width())
        height = skill_status_surface.get_height() + text_surface.get_height() + 10

        tooltip_x = mouse_pos[0] + 10
        tooltip_y = mouse_pos[1] - height - 100


        pygame.draw.rect(self.screen, (0, 0, 0), (tooltip_x, tooltip_y, width + 15, height + 10))  # Background
        pygame.draw.rect(self.screen, (255, 255, 255), (tooltip_x, tooltip_y, width + 15, height + 10), 2)  # Border

        self.screen.blit(skill_status_surface, (tooltip_x + 10, tooltip_y + 10))
        self.screen.blit(text_surface, (tooltip_x + 10, tooltip_y + 10 + skill_status_surface.get_height()))

    def status_render(self):
        """
        Renders the player's status on the screen.

        This method can be used to display additional information about the player's state.
        Currently, it is not implemented.
        """
        pass

    def score_render(self):
        """
        Renders the player's score and survival time on the screen.

        The score is the number of enemies killed, and the survival time is the duration the player has survived.
        """
        killed_enemies = self.player.killed_enemies
        score_text = f"Abates: {killed_enemies}"
        score_surface = self.font.render(score_text, True, (255, 255, 255))

        # Position the score at the top-right corner of the screen
        score_rect = score_surface.get_rect(topright=(self.screen.get_width() - 10, 10))
        self.screen.blit(score_surface, score_rect)

        # Timer - time survived since the game started
        if self.score_running or playing_status:  # Only run the timer if 'score_running' is True or playing_status
            time_survived = (pygame.time.get_ticks() - self.current_time + self.time_paused) / 1000  # Convert to seconds
        else:
            time_survived = self.time_paused / 1000  # Use the last recorded time when paused

        self.player.time_of_playing = time_survived
        
        time_text = f"Tempo: {int(time_survived)}s"
        time_surface = self.font.render(time_text, True, (255, 255, 255))

        # Position the timer at the top-right corner of the screen, next to the score
        time_rect = time_surface.get_rect(topright=(self.screen.get_width() - 100, 10))
        self.screen.blit(time_surface, time_rect)


    def reset_game_status(self):
        """
        Resets the game status such as score and time.

        This includes resetting the player's kill count, the starting time, and the paused time.
        """
        self.player.killed_enemies = 0
        self.current_time = pygame.time.get_ticks()  # Reset the starting time to current time
        self.time_paused = 0  # Reset the paused time when restarting the game
        self.score_running = True  # Ensure the timer starts running again when the game is restarted

    def pause_game(self):
        """
        Pauses the game and stores the current time.

        The game timer is paused, and the elapsed time is stored.
        """
        self.score_running = False
        self.time_paused += pygame.time.get_ticks() - self.current_time  # Store the time that has passed until the pause

    def resume_game(self):
        """
        Resumes the game and restarts the timer.

        The game timer is resumed from the last recorded time.
        """
        self.score_running = True
        self.current_time = pygame.time.get_ticks()  

    def draw(self):
        """
        Draws all the game interface elements on the screen.

        This includes the experience bar, health bar, skill interface, status, and score.
        """
        self.experience_bar()
        self.health_bar()
        self.skills_interface()
        self.status_render()
        self.score_render()

    def change_playing_status(self, boolean):
        global playing_status
        playing_status = boolean
