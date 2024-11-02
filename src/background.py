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

background_images = load_images("assets\\images\\background")

class Scenario(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.images = images
        self.image = pygame.image.load("assets\\images\\background\\left-bot-pixel.png")
        self.rect = self.image.get_rect()

    def draw(self, surface):
        width, height = self.image.get_size()

        surface.blit(self.image, (0,0))
        