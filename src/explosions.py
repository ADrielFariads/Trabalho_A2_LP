import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, radius, damage, target_group,sprite_sheet, *groups):
        super().__init__(*groups)
        self.pos = pos
        self.radius = radius
        self.damage = damage
        self.target_group = target_group
        self.sprite_sheet = [pygame.image.load(image).convert_alpha() for image in sprite_sheet]
        self.frames = len(self.sprite_sheet)
        self.current_frame = 0
        self.animation_delay = 50
        self.last_frame_time = pygame.time.get_ticks()

        self.sprite_sheet = [pygame.transform.scale(img, (int(radius*2), int(radius*2))) for img in self.sprite_sheet]

        self.image = self.sprite_sheet[self.current_frame]
        self.rect = self.image.get_rect(center=self.pos)

    def animate(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_frame_time >= self.animation_delay:
            self.current_frame += 1
            self.last_frame_time = current_time

            if self.current_frame < self.frames:
                self.image = self.sprite_sheet[self.current_frame]

            else:
                self.kill()
            
    def update(self):
        self.animate()
                

        
