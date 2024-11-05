
class Camera:
    def __init__(self, width, height):
        self.camera_x = 0
        self.camera_y = 0
        self.width = width
        self.height = height

    def apply(self, entity):
         # Checks if the entity has a 'rect' attribute
        if hasattr(entity, 'rect'):
            return entity.rect.move(self.camera_x, self.camera_y)
        # If not, treat as a pygame.Rect object
        return entity.move(self.camera_x, self.camera_y)

    def update(self, target):
        # Camera follows the target (e.g. player)
        self.camera_x = -target.sprite.rect.centerx + self.width // 2
        self.camera_y = -target.sprite.rect.centery + self.height // 2