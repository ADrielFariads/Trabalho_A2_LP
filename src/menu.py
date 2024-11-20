import pygame

class Button():

    def __init__(self, pos, text_input, base_color, hovering_color, scale):
        #Define commom atributes
        font = pygame.font.Font("assets\\images\\Menu\\font.ttf", 20)
        normal_button = pygame.image.load("assets\\images\\Menu\\button_normal.png").convert_alpha()
        selected_button = pygame.image.load("assets\\images\\Menu\\button_pressed.png").convert_alpha()
        
        # Get the width and height of the image
        width = normal_button.get_width()
        height = normal_button.get_height()

        # Scale the image according to the provided scale factor
        self.button = pygame.transform.scale(normal_button, (int(width * scale), int(height * scale)))
        self.selected_button = pygame.transform.scale(selected_button, (int(width * scale), int(height * scale)))

        #Variable to return the button animation to normal
        self.unselected_button = pygame.transform.scale(normal_button, (int(width * scale), int(height * scale)))
        
        # Button position (x and y)
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        
        # Font and colors
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        
        # If the image is None, use the text as the image (fallback)
        if self.button is None:
            self.button = self.text
        
        # Create the rectangle for the button's collision area (for detecting clicks)
        self.rect = self.button.get_rect(center=(self.x_pos, self.y_pos))
        
        # Create the rectangle for the text's collision area
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.button is not None:
            screen.blit(self.button, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:

                return True
        return False    

    def changeColor(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_x, mouse_y):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            self.button = self.selected_button
        else:
            self.button = self.unselected_button
            self.text = self.font.render(self.text_input, True, self.base_color)
class Menu():

    def __init__(self, screen):
        self.screen = screen
        self.menu_background = pygame.image.load("assets\\images\\Menu\\test_background.jpg").convert_alpha()
        self.play_button = Button([540,300], "PLAY", (255,255,255), (0,0,0), 0.7)
        self.menu_text = Text(540,150,"Cosmic Survivor", (255,255,255), 56)
        self.options_button = Button([540,400], "OPTIONS",(255,255,255), (0,0,0), 0.7)
        self.play_again_button = Button([300,350], "PLAY AGAIN",(255,255,255), (0,0,0), 1)

        self.back_options_button = Button([300,350], "BACK",(255,255,255), (0,0,0), 1)
        self.back_paused_button = Button([300,350], "BACK",(255,255,255), (0,0,0), 1)
        
        self.menu_button = Button([750,350], "MENU", (255,255,255), (0,0,0), 1)
        self.paused_text = Text(540,150,"Game Paused", (255,255,255), 56)
        self.options_text = Text(540,250, "Press Esc to pause", (255,255,255), 50)
        self.death_text = Text(540,150,"Game Over!", (255,255,255), 56)
        self.initial_menu = True
        self.options_menu = False
        self.death_menu = False
        self.pause_menu = False
        self.playing = False

    def change_current_action(self, button):
        if button == self.play_button:
            self.playing = True
        elif button == self.options_button:
            self.initial_menu = False
            self.options_menu = True
        elif button == self.back_options_button:
            self.options_menu = False
            self.initial_menu = True
        elif button == self.back_paused_button:
            self.playing = True
        elif button == self.menu_button:
            self.pause_menu = False
            self.death_menu = False
            self.initial_menu = True
        elif button == self.play_again_button:
            self.playing = True


    def draw(self,text, *button_args):
        self.screen.blit(self.menu_background, (0,0))
        for button in button_args:
            button.update(self.screen)
            button.changeColor()
            if button.checkForInput():
                self.change_current_action(button)

        text.draw(self.screen)
        pygame.display.update()

    def update(self):
        if self.initial_menu:
            self.draw(self.menu_text, self.play_button, self.options_button)
        elif self.options_menu:
            self.draw(self.options_text,self.back_options_button)
        elif self.pause_menu:
            self.draw(self.paused_text, self.menu_button,self.back_paused_button)
        elif self.death_menu:
            self.draw(self.death_text,self.play_again_button,self.menu_button)

class Text():

    def __init__(self, pos_x, pos_y, text, color, font_size):
        font = pygame.font.Font("assets/images/Menu/font.ttf", font_size)
        self.font = font
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        self.color = color

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(self.pos_x, self.pos_y))
        screen.blit(text_surface, text_rect)
