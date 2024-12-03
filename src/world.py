import random
import pygame

# Class to generate the world
class World:
    """
    A class to represent the world in which the game takes place. It generates a set of rectangles
    within a defined width and height, and provides functionality to draw them on a given surface.
    """
    def __init__(self, width, height, num_rectangles):
        """
        Initializes the world with given dimensions and generates rectangles within it.
        
        Args:
            width (int): The width of the world.
            height (int): The height of the world.
            num_rectangles (int): The number of rectangles to generate in the world.
        """
        self.width = width
        self.height = height
        self.rectangles = []
        self.generate_world(num_rectangles)

    def generate_world(self, num_rectangles):
        """
        Generates a set of random rectangles within the world.
        
        Args:
            num_rectangles (int): The number of rectangles to generate.
        """
        for _ in range(num_rectangles):
            rect_x = random.randint(0, self.width - 50)  # Random x position
            rect_y = random.randint(0, self.height - 50)  # Random y position
            self.rectangles.append(pygame.Rect(rect_x, rect_y, 50, 50))  # Add rectangle to list

    def draw(self, surface, camera):
        """
        Draws the rectangles onto the given surface, applying the camera's transformations to their positions.
        
        Args:
            surface (pygame.Surface): The surface to draw the rectangles on.
            camera (Camera): The camera used to apply transformations (e.g., scaling or translating) to the rectangles.
        """
        for rect in self.rectangles:
            pygame.draw.rect(surface, (0, 0, 0), camera.apply(rect))  # Draw each rectangle
