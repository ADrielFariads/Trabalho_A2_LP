import pygame
import random

import config
from player import Player
import guns
from background import CollisionSprite
import enemies
from groups import AllSpritesgroup
from interface import GameInterface
import skills
import explosions
from menu import Menu

# initial setup
class Game:
    def __init__(self):
        # initial setup
        pygame.init()
        pygame.mixer.init()
        self.display_surface = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
        self.display_surface = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
        pygame.display.set_caption("Cosmic Survivor")
        self.clock = pygame.time.Clock()

        # Define running attribute
        self.running = False  # Set default value

        #Soundtrack
        self.soundtrack = pygame.mixer.music.load("assets\\audio\\background2_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.25)

        # Initialize background
        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.image.load(config.FilesPath.BACKGROUND.value) 
        self.background.rect = self.background.image.get_rect(topleft=(0,0))
        self.background.image = pygame.image.load(config.FilesPath.BACKGROUND.value) 
        self.background.rect = self.background.image.get_rect(topleft=(0,0))
        self.background_group = pygame.sprite.Group(self.background) 
        self.map_bounds = config.RectColiddersMap.MAPBOUNDS.value #rect for keep the player in the map
        

        #colliders
        colliders_rects = config.collisionSpritesGenerator()

        #skills
        machinegun_render = skills.MachineGunRender()
        knife_render = skills.KnifeThrowerRender()
        shotgun_render = skills.ShotgunRender()
        time_manipulation = skills.TimeManipulation()
        heal = skills.Heal()
        dash = skills.Adrenaline()
        iron_will = skills.IronWill()
        vortex = skills.GravitionVortex()
        blood_lust = skills.Bloodlust()
        lethal_tempo = skills.LethalTempo()
        missile_rain = skills.MissilRain()
        
        cyborg_skillset = [machinegun_render, lethal_tempo, missile_rain]
        blade_master_skillset = [knife_render, blood_lust, time_manipulation]
        berserker_skillset = [shotgun_render, iron_will, vortex]


        #players heroes

        #cyborg config
        self.cyborg = Player((1200, 1200), 1000, 7, self.map_bounds,cyborg_skillset, colliders_rects)
        self.machinegun = guns.MachineGun(self.cyborg, self.map_bounds)
        self.cyborg.gun = self.machinegun

        #blade_master config
        self.blade_master = Player((1200, 3000), 1000, 10, self.map_bounds, blade_master_skillset, colliders_rects)
        self.knifeThrower = guns.KnifeThrower(self.blade_master, self.map_bounds)
        self.blade_master.gun = self.knifeThrower

        #berserker
        self.berserker = Player((1200, 1200), 2000, 7, self.map_bounds, berserker_skillset, colliders_rects)
        self.shotgun = guns.Shotgun(self.berserker, self.map_bounds)
        self.berserker.gun = self.shotgun

        # Menu player selection
        self.character_dictionary = {
            1: self.cyborg,
            2: self.blade_master,
            3: self.berserker
        }

        # default player
        self.player = self.cyborg
        self.gun = self.player.gun
        

        # groups
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.gun_group = pygame.sprite.GroupSingle(self.gun)
        self.bullet_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.player.enemies = self.enemies_group
        self.player.explosion_group = self.enemies_group

        #interface
        self.interface = GameInterface(self.display_surface, self.player)

        # Camera interaction
        self.all_sprites = AllSpritesgroup()
        self.all_sprites.add(self.background_group, self.enemies_group, self.player, self.gun_group, self.bullet_group)

        # Testing enemies
        for i in range(20):
            slime = enemies.Slime(config.random_pos(), self.player, self.bullet_group, 3, self.enemies_group)
            bat = enemies.AlienBat(config.random_pos(), self.player, self.bullet_group, self.enemies_group)
            slime.colliders = colliders_rects
            
            

        self.all_sprites.add(self.enemies_group)
        self.player.offset = self.all_sprites.offset

        self.menu = Menu(self.display_surface, self.player, self.enemies_group, self.interface)

        # Update all enemies to track the new player
        for enemy in self.enemies_group:
            if isinstance(enemy, enemies.Enemy):  # Check to ensure it's an enemy object
                enemy.update_target(self.player)

    def initialize_player(self):
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
                # event loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # Handle window close
                        print("Closing game")
                        self.running = False

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:                  
                        mouse_pos = pygame.mouse.get_pos() - self.all_sprites.offset
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
                # updates
                self.explosion_group.update()
                self.player.update(keys)
                self.enemies_group.update()
                self.gun.update()
                self.bullet_group.update()
                

                # drawings
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

        pygame.quit()  # Ensure pygame resources are cleaned up after the loop end
        exit()  # Ensure the program terminates


if __name__ == "__main__":
    game = Game()
    game.run()