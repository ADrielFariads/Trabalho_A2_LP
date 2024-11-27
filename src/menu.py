import pygame
from enemies import Enemy
from player import Player

class Button():

    def __init__(self, pos, text_input, base_color, hovering_color, scale):
        #Define commom atributes
        font = pygame.font.Font("assets\\images\\Menu\\font.ttf", 20)
        normal_button = pygame.image.load("assets\\images\\Menu\\button_normal.png").convert_alpha()
        selected_button = pygame.image.load("assets\\images\\Menu\\button_pressed.png").convert_alpha()

        #Buttons audios
        self.select_audio = pygame.mixer.Sound("assets\\audio\\menu\\Menu_Selection.wav")
        self.click_audio = pygame.mixer.Sound("assets\\audio\\menu\\Menu_Click.wav")
        self.audio = False
        
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
        '''
        Draw button on the screen

        Parameters:
        -----------
        screen where the button will be shown
        '''
        if self.button is not None:
            screen.blit(self.button, self.rect)
        #If the button image doesn't exist draw only the text
        screen.blit(self.text, self.text_rect)

    def checkForClick(self, event):
        '''
        Check if the mouse was pressed once (using pygame event)

        Parameters:
        ------------
        event: pygame event (to detect MOUSEBUTTONDOWN)

        Return:
        --------
        True: if the mouse was pressed
        False: otherwise
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 corresponds to the left mouse button
                if self.rect.collidepoint(event.pos):
                    #self.click_audio.play(0)
                    self.click_audio.play()
                    return True
        return False


    def changeColor(self):
        '''
        Change the text color and the button animation if you overlay them with the mouse
        '''
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        #check if they are overlapped by the mouse
        if self.rect.collidepoint(mouse_x, mouse_y):
            #Plays the selected button sound effect
            if not self.audio:
                self.select_audio.play()
                self.audio = True
            #Change the text color and the button animation 
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            self.button = self.selected_button
        else:
            #Back to normal
            self.audio = False
            self.button = self.unselected_button
            self.text = self.font.render(self.text_input, True, self.base_color)

class Menu():
    def __init__(self, screen, player, enemy):
        '''
        Creates all button and text objects,
        and creates boolean variables to switch between the game and menus

        Parameters:
        -----------
        players and enemies who will have their attributes reset

        '''

        #Will be reseted
        self.player = player
        self.enemy = enemy

        #Screen/ Background
        self.screen = screen
        self.menu_background = pygame.image.load("assets\\images\\Menu\\marte_background.jpg").convert_alpha()

        # Load selectcharacters image 
        self.char_selection_background = pygame.image.load("assets\\images\\Menu\\selectcharacters.png").convert_alpha()
        
        #Buttons
        self.play_button = Button([600,400], "PLAY", (255,255,255), (0,0,0), 1)
        self.options_button = Button([600,550], "OPTIONS",(255,255,255), (0,0,0), 1)
        self.play_again_button = Button([400,450], "PLAY AGAIN",(255,255,255), (0,0,0), 1)
        self.back_options_button = Button([500,450], "BACK",(255,255,255), (0,0,0), 1)
        self.back_paused_button = Button([400,450], "BACK",(255,255,255), (0,0,0), 1)
        self.menu_button = Button([800,450], "MENU", (255,255,255), (0,0,0), 1)
        #Selection Characters
        self.char1_selection_button = Button([300, 600], "Cyborg", (255, 255, 255), (0, 0, 0), 1)
        self.char2_selection_button = Button([600, 600], "Blade Master", (255, 255, 255), (0, 0, 0), 1)
        self.char3_selection_button = Button([900, 600], "Berserk", (255, 255, 255), (0, 0, 0), 1)
        self.back_char_back_button = Button([600, 700], "Menu", (255, 255, 255), (0, 0, 0), 1)
        #character default selected
        self.char_selection = 1


        #Texts
        self.menu_text = Text(600,150,"Cosmic Survivor", (255,255,255), 56)
        self.paused_text = Text(600,150,"Game Paused", (255,255,255), 56)
        self.options_text = Text(600,250, "Press Esc to pause", (255,255,255), 50)
        self.death_text = Text(600,150,"Game Over!", (255,255,255), 56)
        self.char_selection_text = Text(600,150,"Main Characters", (255,255,255), 56)

        #Game states
        self.initial_menu = True
        self.options_menu = False
        self.death_menu = False
        self.pause_menu = False
        self.playing = False
        self.char_selection_state = False

    def change_current_game_state(self, button):
        '''
        Verify the button and change the current game state or start the game
        through user interaction with the buttons.

        Parameters:
        ------------
        Button that was pressed
        '''

        if button == self.play_button:
            self.initial_menu = False
            self.char_selection_state = True
        elif button == self.char1_selection_button:
            self.char_selection = 1
            self.char_selection_state = False
            self.playing = True
        elif button == self.char2_selection_button:
            self.char_selection = 2
            self.char_selection_state = False
            self.playing = True
        elif button == self.char3_selection_button:
            self.char_selection = 3
            self.char_selection_state = False
            self.playing = True
        elif button == self.options_button:
            self.initial_menu = False
            self.options_menu = True
        elif button == self.back_options_button:
            self.options_menu = False
            self.playing = False
            self.initial_menu = True
        elif button == self.back_char_back_button:
            # Reset all states to go back to the initial menu
            self.char_selection_state = False  # Reset the character selection state
            self.options_menu = False
            self.playing = False
            self.initial_menu = True
        elif button == self.back_paused_button:
            self.playing = True
        elif button == self.menu_button:
            #Reset the game when return to initial menu
            Enemy.reset_enemies(self,self.enemy)
            self.player.reset_player()
            self.pause_menu = False
            self.death_menu = False
            self.initial_menu = True
        elif button == self.play_again_button:
            #Reset the game to play again
            Enemy.reset_enemies(self,self.enemy)
            self.player.reset_player()
            self.playing = True


    def draw(self, text, *button_args):
        '''
        Draws the screen and handles button events.

        Parameters:
        -----------
        text: The text object to display on the screen.
        *button_args: Button objects that will be displayed and interacted with.
        '''
        # If in character selection state, draw the character selection background on top of the existing background
        if self.char_selection_state:
            self.screen.blit(self.menu_background, (0, 0))  # Draw the menu background first
            self.screen.blit(self.char_selection_background, (0, 0))  # Draw the character selection background on top
        # Render the default background
        else:
            self.screen.blit(self.menu_background, (0, 0))

        # Capture all input events
        events = pygame.event.get()

        # Handle global quit event
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Ensure the program terminates

        # Process each button
        for button in button_args:
            # Draw the button and update its hover state
            button.update(self.screen)
            button.changeColor()

            # Check for mouse click events on the button
            for event in events:
                if button.checkForClick(event):
                    # Perform the action assigned to the clicked button
                    self.change_current_game_state(button)

        # Draw the text on the screen
        text.draw(self.screen)

        # Update the display
        pygame.display.update()



    def update(self):
        '''
        Calls the draw function to the current menu
        '''
        if self.initial_menu:
            self.draw(self.menu_text, self.play_button, self.options_button)
        elif self.options_menu:
            self.draw(self.options_text,self.back_options_button)
        elif self.pause_menu:
            self.draw(self.paused_text, self.menu_button,self.back_paused_button)
        elif self.death_menu:
            self.draw(self.death_text,self.play_again_button,self.menu_button)
        elif self.char_selection:
            self.draw(self.char_selection_text,self.char1_selection_button, self.char2_selection_button, self.char3_selection_button, self.back_char_back_button)

class Text():

    def __init__(self, pos_x, pos_y, text, color, font_size):
        '''
        Defines the font design, what and where will be written

        Parameters:
        ------------
        pos_x and pos_y: position on the x and y axis
        text: what will be written
        color and font_size
        '''
        #Select the font
        font = pygame.font.Font("assets/images/Menu/font.ttf", font_size)
        self.font = font
        self.color = color
        self.text = text
        
        #Text position
        self.pos_x = pos_x
        self.pos_y = pos_y

    def draw(self, screen):
        '''
        Draw text on the screen
        '''
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(self.pos_x, self.pos_y))
        screen.blit(text_surface, text_rect)