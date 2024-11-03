import pygame
import os
from pytmx.util_pygame import load_pygame


tmx_data = load_pygame("assets\\tmx\\test_map.tmx")
print(dir(tmx_data))
class Scenario(pygame.sprite.Sprite):
   pass
        