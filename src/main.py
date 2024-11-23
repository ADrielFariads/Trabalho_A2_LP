import pygame
from pytmx.util_pygame import load_pygame
import random
import sys
import os

from player import Player
from guns import MachineGun
from background import Background
from enemies import Andromaluis, Centipede
from groups import AllSpritesgroup
from menu import Menu

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..' , 'assets', "audio")))

# initial setup
class Game:
    def __init__(self):
        # initial setup
        pygame.init()
        pygame.mixer.init()
        self.running = True
        self.display_surface = pygame.display.set_mode((1080, 640))
        pygame.display.set_caption("Cosmic Survivor")
        self.clock = pygame.time.Clock()

        # Initialize background
        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.image.load("assets\\background_files\\map007.png") 
        self.background.rect = self.background.image.get_rect(center=(1000, 1000))
        self.background_objects = Background("assets\\background_files\\map006.tmx", 16, self.display_surface)
        self.background_group = pygame.sprite.Group(self.background) 
        self.map_bounds = pygame.Rect(690, 420, 2650, 1500) #rect for keep the player in the map

        # sprites
        self.player = Player((1000, 1000), 1000, 8, self.map_bounds, self.background_objects.collision_group)
        self.gun = MachineGun(self.player, self.map_bounds)

        # groups
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.gun_group = pygame.sprite.GroupSingle(self.gun)
        self.bullet_group = pygame.sprite.Group()

        #enemies generation
        self.centipede = Centipede((4000, 1000), self.player, self.bullet_group)
        self.enemies_group = pygame.sprite.Group(self.centipede)

         # Menu
        self.menu = Menu(self.display_surface, self.player, self.centipede)

        #camera interaction
        self.all_sprites = AllSpritesgroup()
        self.all_sprites.add(self.background_group, self.enemies_group, self.player,self.gun_group, self.bullet_group) 

    def run(self):
        
        while True:
            if pygame.event.get(pygame.QUIT):
                pygame.quit()
                quit()

            
            if self.menu.playing:

                 self.clock.tick(60)
            keys = pygame.key.get_pressed()
            

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.gun.shoot(self.bullet_group, self.all_sprites.offset, self.all_sprites)
                    print(self.all_sprites)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.menu.playing = False
                    self.menu.pause_menu = True
                          
            self.all_sprites.add(self.enemies_group)

            if len(self.enemies_group) <= 1:
                miniboss = Andromaluis(((random.randint(620, 2780), random.randint(380, 1600))), self.player, self.bullet_group, self.enemies_group)
                self.enemies_group.add(miniboss)
                self.all_sprites.add(self.enemies_group)

            
            self.player.health_bar(self.display_surface)
            if self.player.current_health == 0:
                    self.menu.death_menu = True
                    self.menu.playing = False                     
            else:
                self.menu.update()

            pygame.display.update()
            pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    game = Game()
    game.run()