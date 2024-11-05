import random
import pygame

# Class to generate the world
class World:
    def __init__(self, width, height, num_rectangles):
        self.width = width
        self.height = height
        self.rectangles = []
        self.generate_world(num_rectangles)

    def generate_world(self, num_rectangles):
        for _ in range(num_rectangles):
            rect_x = random.randint(0, self.width - 50)
            rect_y = random.randint(0, self.height - 50)
            self.rectangles.append(pygame.Rect(rect_x, rect_y, 50, 50)) 

    def draw(self, surface, camera):
        for rect in self.rectangles:
            pygame.draw.rect(surface, (0, 0, 0), camera.apply(rect))