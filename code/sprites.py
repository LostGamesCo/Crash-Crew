from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, ground, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)
        if ground:
            self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface    
        self.rect = self.image.get_frect(topleft = pos)

class ChunkSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, ground, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)
        if ground:
            self.ground = True
