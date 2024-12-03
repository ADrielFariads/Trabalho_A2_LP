import pygame

class AllSpritesgroup(pygame.sprite.Group):
    def __init__(self):
        """
        Initialize the AllSpritesgroup class, which is a custom sprite group that inherits from 
        pygame.sprite.Group. It also sets up the display surface and initializes the offset vector.

        The offset vector is used to adjust the drawing position of sprites.
        """
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        """
        Draw all the sprites in the group, adjusting their positions based on the target position 
        and applying an offset. The sprites are drawn in the correct order based on their z_index.

        :param target_pos: The target position (usually the camera's position or player position)
                            used to adjust the offset for each sprite.
        """
        # Update the offset based on the target position
        self.offset.update(-(target_pos[0] - 600), -(target_pos[1] - 350))
        
        # Loop through all sprites, sorting them based on z_index to ensure correct drawing order
        for sprite in sorted(self, key=lambda s: getattr(s, 'z_index', 0)):
            if hasattr(sprite, "image"):
                # Draw the sprite on the screen, adjusted by the offset
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
