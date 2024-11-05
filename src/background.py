import pygame
import sys
from pytmx.util_pygame import load_pygame

pygame.init()

class Background(pygame.sprite.Sprite):
    def __init__(self, tmx_file_path, *groups):
        super().__init__(*groups)
        






window_width, window_height = 940, 640
screen = pygame.display.set_mode((window_width, window_height))


tmx_data = load_pygame("assets\\background_files\\map001.tmx")

running = True



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30, 30, 30))
    pygame.display.update()