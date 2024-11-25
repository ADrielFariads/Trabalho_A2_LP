import pygame
import random

import config
import config
from player import Player
import guns
from background import CollisionSprite
from enemies import Goblin, generate_goblins, Andromaluis, Slime
import guns
from background import CollisionSprite
from enemies import Goblin, generate_goblins, Andromaluis, Slime
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

        # Initialize background
        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.image.load(config.FilesPath.BACKGROUND.value) 
        self.background.rect = self.background.image.get_rect(topleft=(0,0))
        self.background.image = pygame.image.load(config.FilesPath.BACKGROUND.value) 
        self.background.rect = self.background.image.get_rect(topleft=(0,0))
        self.background_group = pygame.sprite.Group(self.background) 
        self.map_bounds = config.RectColiddersMap.MAPBOUNDS.value #rect for keep the player in the map
        self.map_bounds = config.RectColiddersMap.MAPBOUNDS.value #rect for keep the player in the map

        #colliders
        colliders = config.collisionSpritesGenerator()
        self.explosion_images = [f"assets\\images\\explosions\\Explosion_{i}.png" for i in range(1, 10)]

        #skills
        machinegun_render = skills.MachineGunRender()
        knife_render = skills.KnifeThrowerRender()
        shotgun_render = skills.ShotgunRender()
        heal = skills.Heal()
        dash = skills.Dash()
        berserker_wrath = skills.BerserkerWrath()
        blood_lust = skills.Bloodlust()
        lethal_tempo = skills.LethalTempo()
        missile_rain = skills.MissilRain()
        
        cyborg_skillset = [machinegun_render, lethal_tempo, missile_rain]
        blade_master_skillset = [knife_render, dash, blood_lust]
        berserker_skillset = [shotgun_render, heal, berserker_wrath]


        #players heroes

        #cyborg config
        self.cyborg = Player((1200, 1200), 1000, 8, self.map_bounds,cyborg_skillset, colliders)
        self.machinegun = guns.MachineGun(self.cyborg, self.map_bounds)
        self.cyborg.gun = self.machinegun

        #blade_master config
        self.blade_master = Player((1200, 3000), 1000, 10, self.map_bounds, blade_master_skillset, colliders)
        self.knifeThrower = guns.KnifeThrower(self.blade_master, self.map_bounds)
        self.blade_master.gun = self.knifeThrower

        #berserker
        self.berserker = Player((1200, 1200), 1500, 7, self.map_bounds, berserker_skillset, colliders)
        self.shotgun = guns.Shotgun(self.berserker, self.map_bounds)
        self.berserker.gun = self.shotgun

        #default character
        self.player = self.cyborg
        self.gun = self.player.gun
        
        #colliders
        colliders = config.collisionSpritesGenerator()
        self.explosion_images = [f"assets\\images\\explosions\\Explosion_{i}.png" for i in range(1, 10)]

        #skills
        machinegun_render = skills.MachineGunRender()
        knife_render = skills.KnifeThrowerRender()
        shotgun_render = skills.ShotgunRender()
        heal = skills.Heal()
        dash = skills.Dash()
        berserker_wrath = skills.BerserkerWrath()
        blood_lust = skills.Bloodlust()
        lethal_tempo = skills.LethalTempo()
        missile_rain = skills.MissilRain()
        cyborg_skillset = [machinegun_render, lethal_tempo, missile_rain]
        blade_master_skillset = [knife_render, dash, blood_lust]
        berserker_skillset = [shotgun_render, heal, berserker_wrath]

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


        ####testing enemies#####
        for i in range(10):
            miniboss = Andromaluis((random.randint(1000, 3000), random.randint(1000, 3000)), self.player, self.bullet_group, self.enemies_group)
            self.enemies_group.add(miniboss)
        self.all_sprites.add(self.enemies_group)
        self.player.offset = self.all_sprites.offset

        #Menu
        self.menu = Menu(self.display_surface, self.player, self.enemies_group)

                #menu player selection
        self.character_dictionary = {
            1: self.cyborg,
            2: self.blade_master,
            3: self.berserker
        }
        #select the character based on screen main characters
        self.player = self.character_dictionary[self.menu.char_selection]

    def run(self):
        self.auto_shoot = False

        while True:

            if pygame.event.get(pygame.QUIT):
                pygame.quit()
                quit()
        
            if self.menu.playing:
        
                self.clock.tick(60)
                keys = pygame.key.get_pressed()
                

                # event loop
                for event in pygame.event.get():
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:                  
                        mouse_pos = pygame.mouse.get_pos() - self.all_sprites.offset
                        self.gun.shoot(self.bullet_group, self.all_sprites.offset, self.all_sprites)

                        #explosion = explosions.Explosion(mouse_pos, 150, 1000, self.enemies_group, self.explosion_images)
                        #self.explosion_group.add(explosion)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_b:
                            if not self.auto_shoot:
                                self.auto_shoot = True

                            else: self.auto_shoot = False

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.menu.playing = False
                        self.menu.pause_menu = True
                        self.menu.options_menu = False
                    
                            
                self.all_sprites.add(self.enemies_group, self.explosion_group)

                if self.auto_shoot:
                    self.gun.shoot(self.bullet_group, self.all_sprites.offset, self.all_sprites)
                # updates
                self.player.update(keys)
                self.enemies_group.update()
                self.gun.update()
                self.bullet_group.update()
                self.explosion_group.update()

                # drawings
                self.display_surface.fill(("#4D64AA"))
                self.all_sprites.draw(self.player.rect.center)
            
                self.interface.draw()

                if self.player.current_health == 0:
                    self.menu.options_menu = False
                    self.menu.pause_menu = False
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