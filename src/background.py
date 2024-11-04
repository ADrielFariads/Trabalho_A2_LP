import pygame
import sys
from pytmx.util_pygame import load_pygame

pygame.init()




screen = pygame.display.set_mode((1280, 720))
running = True



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30, 30, 30))
    pygame.display.update()