import pygame
import sys
from pytmx.util_pygame import load_pygame

pygame.init()

class Background(pygame.sprite.Sprite):
    def __init__(self, tmx_file_path, *groups):
        super().__init__(*groups)
        
tmx_data = load_pygame("assets\\tmx\\map001.tmx")




screen = pygame.display.set_mode((1280, 720))
running = True



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30, 30, 30))
    pygame.display.update()