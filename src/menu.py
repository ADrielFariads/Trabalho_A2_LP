import pygame
import config
import json 

from enemies import Enemy

class Button:
    def __init__(self, pos, text_input, base_color, hovering_color, scale):
        # Font setup
        self.font = pygame.font.Font("assets/images/Menu/font.ttf", 20)
        # Load images after pygame.init()
        self.normal_button = pygame.image.load("assets/images/Menu/button_normal.png").convert_alpha()
        self.selected_button = pygame.image.load("assets/images/Menu/button_pressed.png").convert_alpha()
        
        # Scale the images
        scaled_size = (int(self.normal_button.get_width() * scale), int(self.normal_button.get_height() * scale))
        self.button = pygame.transform.scale(self.normal_button, scaled_size)
        self.selected_button = pygame.transform.scale(self.selected_button, scaled_size)
        
        # Button position and text setup
        self.x_pos, self.y_pos = pos
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        
        # Rect setup for button and text positioning
        self.rect = self.button.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        # Audio setup
        self.select_audio = pygame.mixer.Sound("assets/audio/menu/Menu_Selection.wav")
        self.click_audio = pygame.mixer.Sound("assets/audio/menu/Menu_Click.wav")
        self.audio = False

    def update(self, screen):
        """
        Draw button on the screen.
        
        Parameters:
        screen: pygame.Surface - The screen to display the button on.
        """
        screen.blit(self.button, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForClick(self, event):
        """
        Check if the mouse button was pressed and if it's over the button.
        
        Parameters:
        event: pygame.event - Event to check mouse interaction.
        
        Returns:
        bool - True if clicked, False otherwise.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.click_audio.play()
                return True
        return False

    def changeColor(self):
        """
        Change button color and sound when hovered.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            if not self.audio:
                self.select_audio.play()
                self.audio = True
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            self.button = self.selected_button
        else:
            self.audio = False
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.button = pygame.transform.scale(self.normal_button, self.button.get_size())


class Menu():
    def __init__(self, screen, cyborg,blade,berseker, enemy, game_interface):
        '''
        Creates all button and text objects,
        and creates boolean variables to switch between the game and menus

        Parameters:
        -----------
        players and enemies who will have their attributes reset

        '''

        #Players
        self.characters_list = [cyborg, blade, berseker]
        self.player = self.characters_list[1]

        #Will be reseted
        self.enemy = enemy
        self.game_interface = game_interface

        #Screen/ Background
        self.screen = screen
        self.menu_background = pygame.image.load("assets\\images\\Menu\\marte_background.jpg").convert_alpha()

        # Load selectcharacters image 
        self.char_selection_background = pygame.image.load("assets\\images\\Menu\\selectcharacters.png").convert_alpha()
        
        #Buttons
        self.play_button = Button([600,400], "JOGAR", (255,255,255), (0,0,0), 1)
        self.controls_button = Button([600, 550], "CONTROLES", (255, 255, 255), (0, 0, 0), 1)
        self.play_again_button = Button([400,450], "NOVO JOGO",(255,255,255), (0,0,0), 1)
        self.back_options_button = Button([500,450], "VOLTAR",(255,255,255), (0,0,0), 1)
        self.back_paused_button = Button([400,450], "VOLTAR",(255,255,255), (0,0,0), 1)
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
        self.paused_text = Text(600,150,"Jogo Pausado", (255,255,255), 56)
        self.death_text = Text(600,150,"Você Perdeu!", (255,255,255), 56)
        self.char_selection_text = Text(600,150,"Personagens", (255,255,255), 56)
    

        #Game states
        self.initial_menu = True
        self.controls_menu = False
        self.death_menu = False
        self.pause_menu = False
        self.playing = False
        self.char_selection_state = False

    def reset_states(self):
        """Reset all game states to avoid overlap."""
        self.initial_menu = False
        self.controls_menu = False
        self.death_menu = False
        self.pause_menu = False
        self.char_selection_state = False
        self.playing = False

    def change_current_game_state(self, button, alow_heroe):
        '''
        Verify the button and change the current game state or start the game
        through user interaction with the buttons.
        '''
        button_actions = {
            self.play_button: self.start_character_selection,
            self.char1_selection_button: lambda: self.start_game(1, alow_heroe),
            self.char2_selection_button: lambda: self.start_game(2, alow_heroe),
            self.char3_selection_button: lambda: self.start_game(3, alow_heroe),
            self.controls_button: self.open_controls_screen,
            self.back_options_button: self.back_to_main_menu,
            self.back_char_back_button: self.back_to_main_menu,
            self.back_paused_button: self.resume_game,
            self.menu_button: self.return_to_main_menu,
            self.play_again_button: self.restart_game,
            
        }
        
        action = button_actions.get(button)
        if action:
            action()

    # Supporting methods
    def start_character_selection(self):
        self.reset_states()
        self.char_selection_state = True
    

    def start_game(self, character, alow_heroe):
        if(character == 1):
            self.reset_states()
            self.char_selection = character
            self.player = self.characters_list[character-1]
            self.playing = True
            self.game_interface.reset_game_status()
        elif (character == 2 and alow_heroe["Blade_master"] == True):
            self.reset_states()
            self.char_selection = character
            self.player = self.characters_list[character-1]
            self.playing = True
            self.game_interface.reset_game_status()
        elif (character == 3 and alow_heroe["Blade_master"] == True):
            self.reset_states()
            self.char_selection = character
            self.player = self.characters_list[character-1]
            self.playing = True
            self.game_interface.reset_game_status()
    
        

    def open_controls_screen(self):
        self.reset_states()
        self.controls_menu = True

    def back_to_main_menu(self):
        self.reset_states()
        self.initial_menu = True

    def resume_game(self):
        self.reset_states()
        self.playing = True
        self.game_interface.resume_game()

    def return_to_main_menu(self):
        self.reset_states()
        self.enemy.reset_enemies()
        self.player.reset_player()
        self.game_interface.reset_game_status()
        self.initial_menu = True

    def restart_game(self):
        self.reset_states()
        self.enemy.reset_enemies()
        self.player.reset_player()
        self.game_interface.reset_game_status()
        self.playing = True

    def draw(self, text, *button_args):
        '''
        Draws the screen and handles button events.

        Parameters:
        -----------
        text: The text object to display on the screen.
        *button_args: Button objects that will be displayed and interacted with.
        '''

        alow_heroe = {
            "Cyborg": True,
            "Blade_master": False,
            "Berserker": False
        }

        # If in character selection state, draw the character selection background on top of the existing background
        if self.char_selection_state:
            self.screen.blit(self.menu_background, (0, 0))  # Draw the menu background first
            self.screen.blit(self.char_selection_background, (0, 0))  # Draw the character selection background on top
        # Render the default background
        else:
            self.screen.blit(self.menu_background, (0, 0))

        # Capture all input events
        events = pygame.event.get()

        data = config.read_json("progress_game.json")          
        for obj in data:
            # Replace single quotes with double quotes to ensure the string is valid JSON
            json_correct = obj.replace("'", '"')
                
            # Parse the corrected JSON string into a dictionary
            obj_dic = json.loads(json_correct)
                
            # Iterate over the key-value pairs in the dictionary
            for key, value in obj_dic.items():
                if key == "Kills" and value >= 15:
                        # If the key is "Kills" and the value is 15 or more, enable "Blade_master"
                    alow_heroe["Blade_master"] = True
                if key == "Kills" and value >= 25:
                    # If the key is "Kills" and the value is 25 or more, enable "Berserker"
                    alow_heroe["Berserker"] = True

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
                    self.change_current_game_state(button, alow_heroe)

            if button == self.char2_selection_button and button.rect.collidepoint(pygame.mouse.get_pos()) and alow_heroe["Blade_master"] == False:
                    message = f"    -   -   -   Personagem Bloqueado!    -  -    -   \n Libere-o conseguindo 20 abates em uma partida."
                    text_surface = pygame.font.Font("assets\\images\\Fonts\\CyberpunkCraftpixPixel.otf", 14).render(message, True, (255, 255, 0))
                    width, height = text_surface.get_size()
                    width +=10
                    height += 10

                    tooltip_x = pygame.mouse.get_pos()[0] 
                    tooltip_y = pygame.mouse.get_pos()[1] - height - 100

                    pygame.draw.rect(self.screen, (0,0,0), (tooltip_x, tooltip_y, width + 10, height + 10))  # Background
                    pygame.draw.rect(self.screen, (255, 255, 255), (tooltip_x, tooltip_y, width + 10, height + 10), 2)  # Border

                    self.screen.blit(text_surface, (tooltip_x + 10, tooltip_y + 10))
            elif button == self.char3_selection_button and button.rect.collidepoint(pygame.mouse.get_pos()) and alow_heroe["Berserker"] == False: 
                    message = f"    -   -   -   Personagem Bloqueado!    -  -    -   \n Libere-o sobrevivendo 5 minutos em uma partida."
                    text_surface = pygame.font.Font("assets\\images\\Fonts\\CyberpunkCraftpixPixel.otf", 14).render(message, True, (255, 255, 0))
                    width, height = text_surface.get_size()
                    width +=10
                    height += 10

                    tooltip_x = pygame.mouse.get_pos()[0] - width - 20
                    tooltip_y = pygame.mouse.get_pos()[1] - height - 100

                    pygame.draw.rect(self.screen, (0,0,0), (tooltip_x, tooltip_y, width + 10, height + 10))  # Background
                    pygame.draw.rect(self.screen, (255, 255, 255), (tooltip_x, tooltip_y, width + 10, height + 10), 2)  # Border

                    self.screen.blit(text_surface, (tooltip_x + 10, tooltip_y + 10))


        # Draw the text on the screen
        text.draw(self.screen)

        # Update the display
        pygame.display.update()

    def draw_controls_screen(self):
        # Draw the background
        self.screen.blit(self.menu_background, (0, 0))

        # Load and prepare the image (mouse and keyboard)
        mousekeyboard_image = pygame.image.load("assets/images/Menu/mousekeyboard.png").convert_alpha()
        image_width, image_height = mousekeyboard_image.get_size()
        scaled_size = (int(image_width * 1), int(image_height * 1))  # Scale the image
        mousekeyboard_image = pygame.transform.scale(mousekeyboard_image, scaled_size)

        # Controls text
        controls_text = [
            "Cima: W",
            "Esquerda: A",
            "Baixo: S",
            "Direita: D",
            "Hablidade 1: Q",
            "Hablidade 2: E",
            "Pausa: Esc",
            "Atirar: Botão Esquerdo"
        ]

        # Text positions
        text_start_x = 20
        text_start_y = 150
        line_spacing = 50

        # Calculate maximum text width for alignment
        font = pygame.font.Font(None, 40)  # Default font
        max_text_width = max(font.size(line)[0] for line in controls_text)
        
        # Position the image beside the text
        image_x = 40
        image_y = -75

        # Draw each line of controls text
        for i, line in enumerate(controls_text):
            y_pos = text_start_y + i * line_spacing
            rendered_text = Text(text_start_x, y_pos, line, (255, 255, 255), 40)
            rendered_text.draw(self.screen, left_align=True)

        # Draw the image beside the text
        self.screen.blit(mousekeyboard_image, (image_x, image_y))

        # Update button position dynamically below the text or image
        button_center_x = self.screen.get_width() // 2
        button_y_offset = text_start_y + len(controls_text) * line_spacing + 50
        self.back_options_button.x_pos = button_center_x
        self.back_options_button.y_pos = button_y_offset

        # Update button rects for drawing and interaction
        self.back_options_button.rect = self.back_options_button.button.get_rect(center=(self.back_options_button.x_pos, self.back_options_button.y_pos))
        self.back_options_button.text_rect = self.back_options_button.text.get_rect(center=(self.back_options_button.x_pos, self.back_options_button.y_pos))

        # Draw and update the button
        self.back_options_button.update(self.screen)
        self.back_options_button.changeColor()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if self.back_options_button.checkForClick(event):
                self.back_to_main_menu()

        # Update the display
        pygame.display.update()



    def update(self):
        """
        Calls the appropriate draw function based on the current menu state.
        """
        if self.initial_menu:
            self.draw(self.menu_text, self.play_button, self.controls_button)
        elif self.controls_menu:
            self.draw_controls_screen()
        elif self.pause_menu:
            self.draw(self.paused_text, self.menu_button, self.back_paused_button)
        elif self.death_menu:
            self.draw(self.death_text, self.play_again_button, self.menu_button)
        elif self.char_selection_state:  # Fix typo here from char_selection to char_selection_state
            self.draw(self.char_selection_text, self.char1_selection_button, self.char2_selection_button, self.char3_selection_button, self.back_char_back_button)
    
        
        self.game_interface.score_running = self.playing

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

    def draw(self, screen, left_align=False):
        """
        Draw text on the screen.

        Parameters:
        -----------
        screen : pygame.Surface
            The screen to draw the text on.
        left_align : bool, optional
            Whether to align text to the left instead of centering it (default is False).
        """
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect()
        if left_align:
            text_rect.topleft = (self.pos_x, self.pos_y)
        else:
            text_rect.center = (self.pos_x, self.pos_y)
        screen.blit(text_surface, text_rect)
