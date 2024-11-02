import pygame
import os

import pygame.locals

# loading the images
def load_images(folder):
    images = []
    for each in os.listdir(folder):
        image_path = os.path.join(folder, each)
        image = pygame.image.load(image_path)
        images.append(image)
    return images



class Scenario(pygame.sprite.Sprite):
   pass
        