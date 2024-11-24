import pygame
from unittest.mock import Mock
import unittest
import sys 
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..' , 'src')))

import background

class TestTile(unittest.TestCase):
    def test_tile_initialization(self):
        # Set up a mock for the image
        mock_image = Mock()
        mock_image.get_rect.return_value = pygame.Rect(20, 30, 50, 50)  # Mock the rect

        # Simulated groups
        groups = pygame.sprite.Group()

        # Create the Tile object
        tile = background.Tile(pos=(20, 30), image=mock_image, groups=groups)

        # Verify that the attributes were correctly initialized
        self.assertEqual(tile.image, mock_image)  # The image was correctly assigned
        self.assertEqual(tile.rect.topleft, (20, 30))  # The position is correct
        self.assertIn(tile, groups)  # The sprite was added to the group


class TestCollisionSprite(unittest.TestCase):
    def test_collision_sprite_initialization(self):


        # Define test parameters
        pos = (100, 150)  # Position (center of the rect)
        size = (50, 50)   # Width and height
        groups = pygame.sprite.Group()  # Simulated sprite group

        # Create the CollisionSprite instance
        sprite = background.CollisionSprite(pos, size, groups)

        # Assertions to verify initialization
        self.assertEqual(sprite.image.get_size(), size)  # Check if the size of the surface is correct
        self.assertEqual(sprite.rect.center, pos)  # Check if the rect's center matches the given position
        self.assertIn(sprite, groups)  # Verify that the sprite was added to the group

class TestPlantSprite(unittest.TestCase):
    def test_plant_sprite_initialization(self):

        # Test parameters
        mock_image = Mock()  # Mock the image object
        pos = (100, 150)  # Initial position of the sprite
        width, height = 200, 200  # Width and height of the rectangle
        groups = pygame.sprite.Group()  # Simulated sprite groups

        # Create the PlantSprite object
        # Pass groups as a positional argument, not keyword
        plant_sprite = background.PlantSprite(mock_image, pos, width, height, groups)

        # Check if the image was correctly assigned
        self.assertEqual(plant_sprite.image, mock_image)

        # Check if the rect size was correctly inflated (adjusted size)
        expected_rect = pygame.Rect(pos[0], pos[1], width, height).inflate(-80, -80)
        self.assertEqual(plant_sprite.rect.size, expected_rect.size)

        # Check if the rect center was correctly adjusted
        self.assertEqual(plant_sprite.rect.center, pos)

        # Check if the sprite was added to the group
        # Now groups should contain the sprite
        self.assertIn(plant_sprite, groups)

class TestBackground(unittest.TestCase):
    ...
