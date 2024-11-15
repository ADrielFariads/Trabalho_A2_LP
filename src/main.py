import pygame
from pytmx.util_pygame import load_pygame
import random
import cProfile

from player import Player
from guns import Gun, Bullet
from camera import Camera
from background import Background
from enemies import Goblin, generate_goblins
from groups import AllSpritesgroup

# initial setup
class Game:
    def __init__(self):
        # initial setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((1080, 640))
        pygame.display.set_caption("Cosmic Survivor")
        self.running = True
        self.clock = pygame.time.Clock()

        # camera settings
        self.camera = Camera(self.display_surface.get_width(), self.display_surface.get_height())

        # Initialize background
        self.background = Background("assets\\background_files\\map006.tmx", 16, self.display_surface)  
        self.map_bounds = pygame.Rect(620, 380, 2780, 1600) #rect for keep the player in the map

        # sprites
        self.player = Player((1000, 1000), 1000, 10,self.map_bounds, self.background.collision_group)
        self.gun = Gun(self.player, "assets\\images\\Guns\\2_1.png", 10, 100, Bullet, self.map_bounds)

        # groups
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.gun_group = pygame.sprite.GroupSingle(self.gun)
        self.bullet_group = pygame.sprite.Group()

        #enemies generation
        self.enemies_group = pygame.sprite.Group()
        generate_goblins(1, 4000, 3000, self.player, self.bullet_group, self.enemies_group)

        #camera interaction
        self.all_sprites = AllSpritesgroup()
        self.all_sprites.add(self.background.ground_group, self.background.collision_group, self.enemies_group, self.player,self.gun_group, self.bullet_group)

        

    def run(self):

        while self.running:
            self.clock.tick(60)
            keys = pygame.key.get_pressed()
            

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.all_sprites.add(self.gun.shoot(self.bullet_group, self.all_sprites.offset))
                    print(self.player.position, self.gun.position)
                    
                
                

                    


            #if len(self.enemies_group) == 0:
            #    generate_goblins(15, 4000, 3000, self.player, self.bullet_group, self.enemies_group)
            #    self.all_sprites.add(self.enemies_group)

            # updates
            self.player.update(keys, self.gun)
            self.enemies_group.update()
            self.gun.update()
            self.bullet_group.update()

            self.camera.update(self.player_group) #not working yet
            self.display_surface.fill((30, 30, 30))

            # drawings
            self.all_sprites.draw(self.player.rect.center)
        
            self.player.health_bar(self.display_surface)

            pygame.display.flip()


        pygame.quit()



if __name__ == "__main__":
    game = Game()
    game.run()