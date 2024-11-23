import pygame
import random

from player import Player
import guns
from background import CollisionSprite
from enemies import Goblin, generate_goblins, Andromaluis, Slime
from groups import AllSpritesgroup
from interface import GameInterface
import skills
import explosions

# initial setup
class Game:
    def __init__(self):
        # initial setup
        pygame.init()
        pygame.mixer.init()
        self.display_surface = pygame.display.set_mode((1080, 640))
        pygame.display.set_caption("Cosmic Survivor")
        self.running = True
        self.clock = pygame.time.Clock()

        

        # Initialize background
        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.image.load("assets\\background_files\\map007.png") 
        self.background.rect = self.background.image.get_rect(topleft=(0,0))
        #self.background_objects = Background("assets\\background_files\\map007.tmx", 16, self.display_surface)
        self.background_group = pygame.sprite.Group(self.background) 
        self.map_bounds = pygame.Rect(1020, 710, 6460, 3480) #rect for keep the player in the map

        #colliders
        colliders = []
        rect1 = CollisionSprite((1680, 1072), (250, 150))
        colliders.append(rect1)
        self.explosion_images = [f"assets\\images\\explosions\\Explosion_{i}.png" for i in range(1, 10)]

        #skills
        #machinegun_render = skills.MachineGunRender()
        #knife_render = skills.KnifeThrowerRender()
        #shotgun_render = skills.ShotgunRender()
        #heal = skills.Heal()
        #berserker = skills.Berserker()
        blood_lust = skills.Bloodlust()
        lethal_tempo = skills.LethalTempo()
        missile_rain = skills.HugeMissil()
        skill_list = [blood_lust, missile_rain]

        # sprites
        self.player = Player((1200, 1200), 1000, 12, self.map_bounds,skill_list, colliders)
        self.gun = guns.KnifeThrower(self.player, self.map_bounds)
        self.player.gun = self.gun
        
        
        # groups
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.gun_group = pygame.sprite.GroupSingle(self.gun)
        self.bullet_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()

        #enemies generation and interation
        self.enemies_group = pygame.sprite.Group()

        self.player.enemies = self.enemies_group
        self.player.explosion_group = self.enemies_group

        #interface

        self.interface = GameInterface(self.display_surface, self.player)

        #camera interaction
        self.all_sprites = AllSpritesgroup()
        self.all_sprites.add(self.background_group, self.enemies_group, self.player,self.gun_group, self.bullet_group) 


        ####testing enemies#####
        for i in range(10):
            miniboss = Andromaluis((random.randint(1000, 3000), random.randint(1000, 3000)), self.player, self.bullet_group, self.enemies_group)
            self.enemies_group.add(miniboss)
        self.all_sprites.add(self.enemies_group)
        self.player.offset = self.all_sprites.offset


    def run(self):

        while self.running:
            self.clock.tick(60)
            keys = pygame.key.get_pressed()
            

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.gun.shoot(self.bullet_group, self.all_sprites.offset, self.all_sprites)
                    mouse_pos = pygame.mouse.get_pos() - self.all_sprites.offset
                    #explosion = explosions.Explosion(mouse_pos, 150, 1000, self.enemies_group, self.explosion_images)
                    #self.explosion_group.add(explosion)
                    
                          
            self.all_sprites.add(self.enemies_group, self.explosion_group)
            
            # updates
            self.player.update(keys)
            self.enemies_group.update()
            self.gun.update()
            self.bullet_group.update()
            self.explosion_group.update()

            # drawings
            self.display_surface.fill((30, 30, 30))
            self.all_sprites.draw(self.player.rect.center)
        
            self.interface.draw()

            pygame.display.flip()


        pygame.quit()



if __name__ == "__main__":
    game = Game()
    game.run()