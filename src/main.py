import pygame


from player import Player

#initial setup

pygame.init()
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))

clock = pygame.time.Clock()
running = True

player = Player(window_width/2, window_height/2, 100, 5)

player_group = pygame.sprite.GroupSingle(player)

while running:
    delta_time = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player_group.update(keys, display_surface.get_rect())


    display_surface.fill((30, 30, 30))
    player_group.draw(display_surface)

    pygame.display.flip()
    



pygame.quit()


