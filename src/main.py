import pygame
from pytmx.util_pygame import load_pygame
import random

from player import Player
from guns import Gun, Bullet
from camera import Camera
from background import Background, Tile, CollisionSprite
from enemies import Enemy
from groups import AllSpritesgroup
from menu import Menu

# initial setup
class Game:
    def __init__(self):
        # initial setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((1080, 640))
        pygame.display.set_caption("Cosmic Survivor")
        self.clock = pygame.time.Clock()

        # Menu
        self.menu = Menu(self.display_surface)

        # camera settings
        self.camera = Camera(self.display_surface.get_width(), self.display_surface.get_height())

        # Initialize background
        self.background = Background("assets\\background_files\\map002.tmx", 16, self.display_surface)  

        # sprites
        self.player = Player((640, 360), 1000, 5, self.background.collision_group)
        self.gun = Gun(self.player, "assets\\images\\Guns\\2_1.png", 10, 500, Bullet)

        # groups
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.gun_group = pygame.sprite.GroupSingle(self.gun)
        self.bullet_group = pygame.sprite.Group()

        #enemies generation
        self.enemy1 = Enemy(800, 800, "assets\\images\\enemies\\goblins\\goblin.png", 50, 2, 10000, 10, 100, self.player, self.bullet_group)
        self.enemies_group = pygame.sprite.Group(self.enemy1)

        #camera interaction
        self.all_sprites = AllSpritesgroup()
        self.all_sprites.add(self.background.ground_group, self.background.collision_group, self.enemies_group, self.player, self.gun_group, self.enemies_group, self.bullet_group)

        
    
    def run(self):

        while True:

            if pygame.event.get(pygame.QUIT):
                pygame.quit()
                quit()

            
            if self.menu.playing:

                delta_time = self.clock.tick(60)
                # event loop
                for event in pygame.event.get():
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.gun.shoot(self.bullet_group)
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.menu.playing = False
                        self.menu.initial_menu =  False
                        self.menu.pause_menu = True

                keys = pygame.key.get_pressed()

                # updates
                self.player.update(keys, self.display_surface.get_rect())
                self.enemies_group.update()
                self.gun.update()
                self.bullet_group.update()

                #self.camera.update(self.player_group) #not working yet
                self.display_surface.fill((30, 30, 30))

                # drawings
                self.all_sprites.draw(self.player.rect.center)
                self.bullet_group.draw(self.display_surface)
            
                self.player.health_bar(self.display_surface)
                
                if self.player.current_health == 0:
                    self.menu.death_menu = True
                    self.menu.initial_menu = False
                    self.menu.playing = False                     
            else:
                self.menu.update()
            pygame.display.update()
            pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    game = Game()
    game.run()