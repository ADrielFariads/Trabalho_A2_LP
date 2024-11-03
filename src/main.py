import pygame
from pytmx.util_pygame import load_pygame 

from player import Player
from guns import Gun

#initial setup

pygame.init()
window_width, window_height = 940, 640
display_surface = pygame.display.set_mode((window_width, window_height))

### testing background
background_group = pygame.sprite.Group()
rock_group = pygame.sprite.Group()

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos, surface, *groups):
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)

tmx_data = load_pygame("assets\\tmx\\test_map.tmx")

layer = tmx_data.get_layer_by_name("background")


for layer in tmx_data.visible_layers:
    if hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            pos = (x*32, y*32)
            Tile(pos, surf, background_group)
for obj in tmx_data.objects:
    pos = (obj.x, obj.y)
    rock_tile = Tile(pos, obj.image, background_group)
    rock_group.add(rock_tile)


clock = pygame.time.Clock()
running = True

#class instances

rock_group = pygame.sprite.Group()

player = Player(window_width/2, window_height/2, 500, 3, rock_group)

gun = Gun(player, "assets\\images\\Guns\\2_1.png", 10, 2, "bullet")

player_group = pygame.sprite.GroupSingle(player)

gun_group = pygame.sprite.GroupSingle(gun)



#game loop
while running:
    delta_time = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #test health bar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.get_damaged(50)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.get_healed(50)
    

    keys = pygame.key.get_pressed()
    
    #updating methods
    player_group.update(keys, display_surface.get_rect())
    gun_group.update()

    if pygame.sprite.spritecollide(player, rock_group, False):
        pass

    #drawning the objects in the screen
    display_surface.fill((30, 30, 30))
    background_group.draw(display_surface)
    player.health_bar(display_surface)
    player_group.draw(display_surface)
    gun_group.draw(display_surface)

    pygame.display.flip()
    


  
pygame.quit()


