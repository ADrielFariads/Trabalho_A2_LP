import pygame
from pytmx.util_pygame import load_pygame 

from player import Player
from guns import Gun
from camera import Camera
from world import World


#initial setup
class Game:
    def __init__(self):
        #initial setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Cosmic Survivor")
        self.running = True
        self.clock = pygame.time.Clock()

        #camera settings
        self.camera = Camera(self.display_surface.get_width(), self.display_surface.get_height())

        #world config
        self.world = World(3000, 3000, num_rectangles=100)

        #sprites
        self.player = Player(640, 360, 100, 3)
        self.gun = Gun(self.player, "assets\\images\\Guns\\2_1.png", 10, 2, "bullet")
        
        #groups
        self.all_sprites = pygame.sprite.Group(self.player)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.gun_group = pygame.sprite.GroupSingle(self.gun)

        

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60)

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            # updates
            self.player.update(keys, self.display_surface.get_rect())
            self.gun.update()

            self.camera.update(self.player_group)

            
            self.display_surface.fill((30, 30, 30))
            #drawnings
            self.world.draw(self.display_surface, self.camera)

            self.player_group.draw(self.display_surface)
            self.gun_group.draw(self.display_surface)
            

            

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
        



# pygame.init()
# window_width, window_height = 1280, 720
# world_width, world_height = 3000, 3000 
# display_surface = pygame.display.set_mode((window_width, window_height))

# clock = pygame.time.Clock()
# running = True

# #class instances
# camera = Camera(window_width, window_height)
# world = World(world_width, world_height, num_rectangles=100)

# player = Player(window_width/2, window_height/2, 500, 5)

# gun = Gun(player, "assets\\images\\Guns\\2_1.png", 10, 2, "bullet")

# player_group = pygame.sprite.GroupSingle(player)
# gun_group = pygame.sprite.GroupSingle(gun)


# #game loop
# while running:
#     delta_time = clock.tick(60)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#         #test health bar
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_DOWN:
#                 player.get_damaged(50)
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP:
#                 player.get_healed(50)

#     keys = pygame.key.get_pressed()
    
#     #updating methods
#     player_group.update(keys, display_surface.get_rect())
#     gun_group.update()


#     camera.update(player_group)
#     camera.update(gun_group)

    

#     #drawning the objects in the screen
#     display_surface.fill((30, 30, 30))
#     player.health_bar(display_surface)

#     world.draw(display_surface, camera)

#     for sprite in player_group:
#         display_surface.blit(sprite.image, camera.apply(sprite))
#     for sprite in gun_group:
#         display_surface.blit(sprite.image, camera.apply(sprite))


#     pygame.display.flip()
    


  
# pygame.quit()


