import unittest
from unittest.mock import Mock
import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..' , 'src')))

import enemies 
class TestEnemy(unittest.TestCase):
    def setUp(self):
        pygame.display.set_mode((1, 1))  # Initializes a minimal mode

        # Parameters to initialize the Enemy object
        self.pos = (100, 150)
        self.sprite_sheet = "assets/images/enemies/goblins/goblin.png"
        self.frames_x = 11
        self.frames_y = 4
        self.health = 100
        self.speed = 5
        self.damage = 10
        self.attack_range = 50
        self.attack_delay = 30
        self.player = Mock()
        self.player.rect = pygame.Rect(200, 200, 50, 50)
        self.bullets_group = pygame.sprite.Group()
        self.enemy = enemies.Enemy(
            self.pos, self.sprite_sheet, self.frames_x, self.frames_y,
            self.health, self.speed, self.damage, self.attack_range,
            self.attack_delay, self.player, self.bullets_group
        )

    def test_enemy_initialization(self):
        # Create the Enemy object
        enemy = enemies.Enemy(self.pos, self.sprite_sheet, self.frames_x, self.frames_y, self.health, self.speed, self.damage, self.attack_range, self.attack_delay, self.player, self.bullets_group)

        # Assertions
        self.assertEqual(enemy.position.x, self.pos[0])  # Verify x position
        self.assertEqual(enemy.position.y, self.pos[1])  # Verify y position
        self.assertEqual(enemy.health, self.health)      # Verify health
        self.assertEqual(enemy.speed, self.speed)        # Verify speed

    def test_get_damaged(self):
        """Tests if the enemy receives damage correctly."""
        initial_health = self.enemy.health
        damage = 20
        self.enemy.get_damaged(damage)
        self.assertEqual(self.enemy.health, initial_health - damage)

    def test_get_healed(self):
        """Tests if the enemy is healed correctly."""
        self.enemy.get_damaged(50)  # Reduces health to 50
        heal_amount = 30
        self.enemy.get_healed(heal_amount)
        self.assertEqual(self.enemy.health, 80)  # 50 + 30

        # Tests if excess healing doesn't exceed the maximum
        self.enemy.get_healed(50)
        self.assertEqual(self.enemy.health, self.enemy.max_health)

    def test_attack(self):
        """Tests if the enemy attacks the player correctly."""
        initial_health = self.player.health = 100

        # Configures the mock behavior
        def mocked_get_damaged(damage):
            self.player.health -= damage

        self.player.get_damaged = Mock(side_effect=mocked_get_damaged)

        # Performs the attack
        self.enemy.attack(self.player)

        # Verifies if the method was called correctly
        self.player.get_damaged.assert_called_once_with(self.damage)

        # Verifies if the health was reduced
        self.assertEqual(self.player.health, initial_health - self.damage)


    def test_player_distance(self):
        """Tests if the distance to the player is calculated correctly."""
        expected_distance = pygame.math.Vector2(100, 150).distance_to(
            pygame.math.Vector2(225, 225)  # Center of the player's rectangle
        )
        self.assertAlmostEqual(self.enemy.player_distance(), expected_distance)

    def test_track_player(self):
        """Tests if the enemy moves towards the player."""
        # Sets the initial positions of the enemy and player
        self.enemy.rect.center = (100, 100)
        self.player.rect = pygame.Rect(200, 200, 50, 50)

        initial_position = self.enemy.rect.center
        initial_distance = self.enemy.player_distance()  # Initial distance

        # Moves the enemy towards the player
        self.enemy.track_player()

        new_position = self.enemy.rect.center
        new_distance = self.enemy.player_distance()  # Distance after movement

        # Verifies if the position has changed (the enemy should have moved)
        self.assertNotEqual(initial_position, new_position)

        # Verifies if the distance decreased
        self.assertTrue(new_distance < initial_distance, "The distance did not decrease correctly")       

    def test_update_on_bullet_collision(self):
        # Configures the mock behavior
        def mocked_get_damaged(damage):
            self.enemy.health -= damage

            # Creates the mock for the enemy
            self.enemy.get_damaged = Mock(side_effect=mocked_get_damaged)

            # Configures the mock for the bullet
            mock_bullet = Mock(spec=pygame.sprite.Sprite)
            mock_bullet.damage = 20
            mock_bullet.rect = pygame.Rect(0, 0, 10, 10)  # Defining a rectangle for the sprite

            # Adds the bullet to the bullets group
            self.enemy.bullets.add(mock_bullet)

            # Simulates the collision (using spritecollide)
            collided_bullets = pygame.sprite.spritecollide(self.enemy, self.enemy.bullets, True)

            # Calls the damage method if a collision occurs
            for bullet in collided_bullets:
                self.enemy.get_damaged(bullet.damage)

            # Verifies if the enemy lost health correctly after the collision
            self.assertEqual(self.enemy.health, 100 - mock_bullet.damage)  # Example health check



    def test_update_on_death(self):
        """Tests if the enemy dies and gives experience to the player."""
        self.enemy.health = 0
        initial_experience = self.player.experience = 50
        self.enemy.update()
        self.assertEqual(self.player.experience, initial_experience + self.enemy.damage)
        self.assertFalse(self.enemy.alive())

class TestGoblin(unittest.TestCase):
    def setUp(self):
        pygame.display.set_mode((1, 1))  # Initializes a minimal mode

        # Parameters to initialize the Goblin object
        self.pos = (100, 150)
        self.player = Mock()
        self.player.rect = pygame.Rect(200, 200, 50, 50)  # Player's position
        self.bullets_group = pygame.sprite.Group()
        self.goblin = enemies.Goblin(self.pos, self.player, self.bullets_group)
        # Parameters to initialize the Goblin object
        self.sprite_sheet = "assets/images/enemies/goblins/goblin.png"
        self.frames_x = 11
        self.frames_y = 4
        self.health = 100
        self.speed = 5
        self.damage = 10
        self.attack_range = 50
        self.attack_delay = 30

        

    def test_behavior_move_towards_player(self):
        """Test if the goblin moves towards the player when out of range."""

        # Set initial distance to be greater than attack range
        self.goblin.attack_range = 50
        self.goblin.player_distance = Mock(return_value=100)  # Distance > attack_range

        # Mock track_player behavior
        def mocked_track_player():
            self.goblin.rect.center = (self.goblin.rect.center[0] + 1, self.goblin.rect.center[1])

        # Replace the track_player method with the mocked version
        self.goblin.track_player = Mock(side_effect=mocked_track_player)

        # Call the behavior method
        self.goblin.behavior()

        # Verify that track_player was called once
        self.goblin.track_player.assert_called_once()


    def test_attack_delay_reset(self):
        ...

class TestAndromaluis(unittest.TestCase):

    def setUp(self):
        ...


    def test_generate_goblins(self):
        ...


    

