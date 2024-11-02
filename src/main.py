import pygame 

from player import Player
from background import Scenario

#initial setup

pygame.init()
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))

clock = pygame.time.Clock()
running = True

#class instances

background = Scenario("assets\\images\\background")

player = Player(window_width/2, window_height/2, 500, 5)

player_group = pygame.sprite.GroupSingle(player)



#game loop
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
    
    player_group.update(keys, display_surface.get_rect())


    background.draw(display_surface)
    player.health_bar(display_surface)
    player_group.draw(display_surface)

    pygame.display.flip()
    


  
pygame.quit()


