import pygame


from player import Player

#initial setup

pygame.init()
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))

clock = pygame.time.Clock()
running = True

player = Player(window_width/2, window_height/2, 500, 5)

player_group = pygame.sprite.GroupSingle(player)

while running:
    delta_time = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.get_damaged(10)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.get_healed(10)

    keys = pygame.key.get_pressed()
    player_group.update(keys, display_surface.get_rect())


    
    display_surface.fill((30, 30, 30))
    player.health_bar(display_surface)
    player_group.draw(display_surface)

    pygame.display.flip()
    



pygame.quit()


