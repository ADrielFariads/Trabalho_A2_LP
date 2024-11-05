import pygame
from pytmx.util_pygame import load_pygame

from player import Player
from guns import Gun
from camera import Camera
from background import Background  # Importando a classe Background

# initial setup
class Game:
    def __init__(self):
        # initial setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Cosmic Survivor")
        self.running = True
        self.clock = pygame.time.Clock()

        # camera settings
        self.camera = Camera(self.display_surface.get_width(), self.display_surface.get_height())

        # Initialize background
        self.background = Background("assets\\background_files\\map001.tmx", 16, self.display_surface)  

        # sprites
        self.player = Player(640, 360, 100, 10)
        self.gun = Gun(self.player, "assets\\images\\Guns\\2_1.png", 10, 2, "bullet")
        
        # groups
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.gun_group = pygame.sprite.GroupSingle(self.gun)


    def run(self):
        while self.running:
            delta_time = self.clock.tick(60)

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            # updates
            self.player.update(keys, self.display_surface.get_rect())
            self.gun.update()

            #self.camera.update(self.player_group)
            self.display_surface.fill((30, 30, 30))

            # drawings
            self.background.draw(self.camera)
            self.player_group.draw(self.display_surface)
            self.gun_group.draw(self.display_surface)

            pygame.display.flip()

        pygame.quit()



if __name__ == "__main__":
    game = Game()
    game.run()
