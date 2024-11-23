import pygame
from enum import Enum

pygame.init()

# info = pygame.display.get_window_size()
# ScreenWidth = info[0]
# ScreenHeight = info[1]
# print(ScreenWidth, ScreenHeight)

class FilesPath(Enum):
    EXPLOSION1 = [f"assets\\images\\explosions\\explosion1\\Explosion_{i}.png" for i in range(1, 10)]
    BACKGROUND = "assets\\background_files\\map007.png"



def load_explosion_images():
    sprite_sheet = [pygame.image.load(image) for image in FilesPath.EXPLOSION1.value]
    return sprite_sheet

