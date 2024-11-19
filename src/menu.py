import pygame

class Button():

    def __init__(self, normal_button, selected_button, pos, text_input, font, base_color, hovering_color, scale):
        #Check if the image is not None
        if normal_button is None:
            raise ValueError("Button image cannot be None.")
        
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
