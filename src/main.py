import pygame
from pytmx.util_pygame import load_pygame
import random

from player import Player
from guns import Gun, Bullet
from camera import Camera
from background import Background, Tile, CollisionSprite
from enemies import Enemy

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
        self.background = Background("assets\\background_files\\map002.tmx", 16, self.display_surface)  

        # sprites
        self.player = Player(640, 360, 1000, 5, self.background.collision_group)
        self.gun = Gun(self.player, "assets\\images\\Guns\\2_1.png", 10, 500, Bullet)

        # groups
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.gun_group = pygame.sprite.GroupSingle(self.gun)
        self.bullet_group = pygame.sprite.Group()

        # enemies generation
        self.enemy1 = Enemy(300, 300, "assets\\images\\enemies\\goblins\\goblin_front_view.png", 50, 2, 100, 10, 100, self.player, self.bullet_group)
        self.enemies_group = pygame.sprite.Group(self.enemy1)

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60)

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.gun.shoot(self.bullet_group)

            keys = pygame.key.get_pressed()

            # updates
            self.player.update(keys, self.display_surface.get_rect())
            self.gun.update()
            self.bullet_group.update()
            self.enemies_group.update()

            self.display_surface.fill((30, 30, 30))

            # drawings
            self.background.draw(self.camera)

            self.player_group.draw(self.display_surface)
            self.gun_group.draw(self.display_surface)
            self.bullet_group.draw(self.display_surface)
            self.enemies_group.draw(self.display_surface)
            self.player.health_bar(self.display_surface)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
