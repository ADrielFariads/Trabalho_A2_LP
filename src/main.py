import pygame
from pytmx.util_pygame import load_pygame
import random

from player import Player
from guns import Gun, Bullet
from camera import Camera
from background import Background, Tile, CollisionSprite
from enemies import Enemy
from groups import AllSpritesgroup
from menu import Button, Text

# initial setup
class Game:
    def __init__(self):
        # initial setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((1080, 640))
        pygame.display.set_caption("Cosmic Survivor")
        self.playing = False
        self.running = True
        self.clock = pygame.time.Clock()

        # Menu
        self.menu_background = pygame.image.load("assets\\images\\Menu\\test_background.jpg").convert_alpha()
        self.play_button = Button([540,300], "PLAY", (255,255,255), (0,0,0), 0.7)
        self.menu_text = Text(540,150,"Cosmic Survivor", (255,255,255), 56)
        self.options_button = Button([540,400], "OPTIONS",(255,255,255), (0,0,0), 0.7)
        self.play_again_button = Button([300,350], "PLAY AGAIN",(255,255,255), (0,0,0), 1)

        self.back_button = Button([300,350], "BACK",(255,255,255), (0,0,0), 1)
        self.menu_button = Button([750,350], "MENU", (255,255,255), (0,0,0), 1)
        self.paused_text = Text(540,150,"Game Paused", (255,255,255), 56)
        self.options_text = Text(540,250, "Press Esc to pause", (255,255,255), 50)
        self.death_text = Text(540,150,"Game Over!", (255,255,255), 56)
        self.death = False

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

        while self.running:
            
            if self.playing:

                delta_time = self.clock.tick(60)
                # event loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.gun.shoot(self.bullet_group)
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.paused = True

                        while self.paused:

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:                                  
                                    self.running = False
                                    self.paused = False
                                if self.back_button.checkForInput():
                                    self.paused = False
                                if self.menu_button.checkForInput():
                                    self.playing = False
                                    self.paused = False


                            self.display_surface.blit(self.menu_background, (0,0))
                            self.back_button.update(self.display_surface)
                            self.back_button.changeColor()


                            self.menu_button.update(self.display_surface)
                            self.menu_button.changeColor()
                            self.paused_text.draw(self.display_surface)
                            pygame.display.update()
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
                    self.death = True
                    self.playing = False
                        
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if self.play_button.checkForInput():
                        self.playing = True
                    if self.options_button.checkForInput():
                        self.options = True
                        while self.options:
                            self.display_surface.blit(self.menu_background, (0,0))
                            self.back_button.update(self.display_surface)
                            self.back_button.changeColor()
                            self.options_text.draw(self.display_surface)

                            pygame.display.update()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT: 
                                    self.options = False
                                    self.running = False
                                if self.back_button.checkForInput():
                                    self.options = False
                
                self.display_surface.blit(self.menu_background, (0,0))
                self.play_button.update(self.display_surface)
                self.play_button.changeColor()
                self.options_button.update(self.display_surface)
                self.options_button.changeColor()
                self.menu_text.draw(self.display_surface)
                
                pygame.display.update()

                while self.death:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.death = False
                            self.running = False
                        if self.play_again_button.checkForInput():
                            #To work you must return the game to the initial position, try to make it with a func in player and enemy class
                            self.player.current_health = self.player.max_health
                            self.death = False
                            self.playing = True
                        if self.menu_button.checkForInput():
                            self.player.current_health = self.player.max_health
                            self.death = False                      
                
                    self.display_surface.blit(self.menu_background, (0,0))
                    self.play_again_button.update(self.display_surface)
                    self.play_again_button.changeColor()
                    self.menu_button.update(self.display_surface)
                    self.menu_button.changeColor()
                    self.death_text.draw(self.display_surface)

                    pygame.display.update()


            pygame.display.flip()



    pygame.quit()



if __name__ == "__main__":
    game = Game()
    game.run()