import pygame

import config
import player
import guns
import enemies
from groups import AllSpritesgroup
from interface import GameInterface
import skills
from menu import Menu

class Game:
    """
    The Game class initializes and runs the game loop for the Cosmic Survivor game.
    It handles game setup, player initialization, enemy updates, and interactions between game components.
    """

    def __init__(self):
        """
        Initialize the game, including setup for display, sounds, players, enemies, and skills.
        """
        # Initial setup
        pygame.init()
        pygame.mixer.init()
        self.display_surface = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
        pygame.display.set_caption("Cosmic Survivor")
        self.clock = pygame.time.Clock()

        # Define running attribute
        self.running = False  # Set default value

        # Soundtrack
        self.soundtrack = pygame.mixer.music.load("assets\\audio\\background2_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.25)

        # Initialize background
        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.image.load(config.FilesPath.BACKGROUND.value) 
        self.background.rect = self.background.image.get_rect(topleft=(0, 0))
        self.background_group = pygame.sprite.Group(self.background)
        self.map_bounds = config.RectColiddersMap.MAPBOUNDS.value  # Rect for keeping the player in the map

        # Colliders
        colliders_rects = config.collisionSpritesGenerator()

        # Players (heroes)
        self.cyborg = player.Cyborg((1200, 1200), self.map_bounds, colliders_rects)
        self.machinegun = guns.MachineGun(self.cyborg, self.map_bounds)
        self.cyborg.gun = self.machinegun

        self.blade_master = player.BladeMaster((1200, 1200), self.map_bounds, colliders_rects)
        self.knifeThrower = guns.KnifeThrower(self.blade_master, self.map_bounds)
        self.blade_master.gun = self.knifeThrower

        self.berserker = player.Berserker((1200, 1200), self.map_bounds, colliders_rects)
        self.shotgun = guns.Shotgun(self.berserker, self.map_bounds)
        self.berserker.gun = self.shotgun

        # Menu player selection
        self.character_dictionary = {
            1: self.cyborg,
            2: self.blade_master,
            3: self.berserker
        }

        # Default player
        self.player = self.cyborg
        self.gun = self.player.gun

        # Groups
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.gun_group = pygame.sprite.GroupSingle(self.gun)
        self.bullet_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.player.enemies = self.enemies_group
        self.player.explosion_group = self.explosion_group

        # Interface
        self.interface = GameInterface(self.display_surface, self.player)

        # Camera interaction
        self.all_sprites = AllSpritesgroup()
        self.all_sprites.add(self.background_group, self.enemies_group, self.player, self.gun_group, self.bullet_group)

        # Testing enemies
        # for i in range(20):
        #     bat = enemies.AlienBat(config.random_pos(), self.player, self.bullet_group, self.enemies_group)

        self.all_sprites.add(self.enemies_group)
        self.player.offset = self.all_sprites.offset

        self.menu = Menu(self.display_surface, self.player, self.enemies_group, self.interface)

        # Update all enemies to track the new player
        for enemy in self.enemies_group:
            if isinstance(enemy, enemies.Enemy):  # Check to ensure it's an enemy object
                enemy.update_target(self.player)

    def initialize_player(self):
        """
        Initializes the player by updating attributes, resetting sprite groups, 
        and re-adding key elements like the player and enemies to the sprite groups.
        """
        # Update player-specific attributes
        self.gun = self.player.gun
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.gun_group = pygame.sprite.GroupSingle(self.gun)
        self.player.enemies = self.enemies_group
        self.player.explosion_group = self.explosion_group
        self.interface = GameInterface(self.display_surface, self.player)

        # Reset all_sprites and re-add key elements
        self.all_sprites.empty()
        self.all_sprites.add(self.background_group, self.player, self.gun_group, self.enemies_group)
        self.player.offset = self.all_sprites.offset

        # Update all enemies to track the new player
        for enemy in self.enemies_group:
            if isinstance(enemy, enemies.Enemy):  # Check to ensure it's an enemy object
                enemy.update_target(self.player)

    def run(self):
        """
        Runs the main game loop, processing events, updating the game state, 
        and rendering the screen.
        """
        self.running = True  # Start the game loop
        while self.running:
            # Update the player dynamically if menu selection changes
            if self.player != self.character_dictionary[self.menu.char_selection]:
                self.player = self.character_dictionary[self.menu.char_selection]
                self.initialize_player()

            if self.menu.playing:
                self.clock.tick(60)
                self.interface.running = True
                keys = pygame.key.get_pressed()
                # Event loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # Handle window close
                        print("Closing game")
                        self.running = False

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:                   
                        self.gun.shoot(self.bullet_group, self.all_sprites.offset, self.all_sprites)
                        
                    if event.type == pygame.KEYDOWN:
                        pass

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.menu.playing = False
                        self.menu.pause_menu = True
                        self.menu.options_menu = False
                        self.interface.pause_game()

                self.all_sprites.add(self.enemies_group, self.explosion_group)

                self.gun.shoot(self.bullet_group, self.all_sprites.offset, self.all_sprites)
                # Updates
                self.explosion_group.update()
                self.player.update(keys)
                self.enemies_group.update()
                self.gun.update()
                self.bullet_group.update()

                # Drawings
                self.display_surface.fill(("#4D64AA"))
                self.all_sprites.draw(self.player.rect.center)

                self.interface.draw()

                if self.player.target_health == 0:
                    self.menu.options_menu = False
                    self.menu.pause_menu = False
                    self.menu.death_menu = True
                    self.menu.playing = False

            else:
                self.menu.update()

            pygame.display.update()

        pygame.quit()  # Ensure pygame resources are cleaned up after the loop ends
        exit()  # Ensure the program terminates


if __name__ == "__main__":
    game = Game()
    game.run()
