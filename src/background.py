import pygame


class CollisionSprite(pygame.sprite.Sprite):
    """
    A sprite class to represent a game object with a collision area.
    
    Attributes:
        image (pygame.Surface): The surface representing the sprite's appearance.
        rect (pygame.Rect): The rectangular area defining the sprite's position and size.
    """

    def __init__(self, pos, size, *groups):
        """
        Initializes a CollisionSprite object.

        Args:
            pos (tuple): The (x, y) coordinates of the sprite's center.
            size (tuple): The (width, height) dimensions of the sprite.
            *groups: Additional sprite groups to which this sprite belongs.
        """
        super().__init__(*groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)




        