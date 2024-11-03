import pygame, sys
from button import Button
from player import Player
from guns import Gun

#initial setup
pygame.init()

window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))

BG = pygame.image.load("assets/images/Menu/Background.png")

def get_font(size): 
    return pygame.font.Font("assets/images/Menu/font.ttf", size)

clock = pygame.time.Clock()
running = True

#class instances

player = Player(window_width/2, window_height/2, 500, 5)

gun = Gun(player, "assets\\images\\Guns\\1_1.png", 10, 2, "bullet")

player_group = pygame.sprite.GroupSingle(player)
gun_group = pygame.sprite.GroupSingle(gun)


def play():
    global running
    global delta_time
    while running:
        delta_time = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #test health bar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player.get_damaged(50)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.get_healed(50)

        keys = pygame.key.get_pressed()
        
        
        #updating methods
        player_group.update(keys, display_surface.get_rect())
        gun_group.update()


        #drawning the objects in the screen
        display_surface.fill((30, 30, 30))
        player.health_bar(display_surface)
        player_group.draw(display_surface)
        gun_group.draw(display_surface)

        pygame.display.flip()

    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        display_surface.fill("white")

        OPTIONS_TEXT = get_font(40).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        display_surface.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(display_surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        display_surface.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        #shadows
        MENU_TEXT_SHADOW = get_font(80).render("COSMIC SURVIVOR", True, "black")
        MENU_RECT_SHADOW = MENU_TEXT_SHADOW.get_rect(center=(642, 102))
        display_surface.blit(MENU_TEXT_SHADOW, MENU_RECT_SHADOW)
        #main texts
        MENU_TEXT = get_font(80).render("COSMIC SURVIVOR", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/images/Menu/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/images/Menu/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/images/Menu/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        display_surface.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(display_surface)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()