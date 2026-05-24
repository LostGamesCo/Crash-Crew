from settings import *

class Light(pygame.sprite.Sprite):
    def __init__(self, light_num, pos, power, radius, color, groups):
        super().__init__(groups)

        self.rect = pygame.FRect(pos[0], pos[1], 1, 1)
        self.pos = pos
        self.power = power
        self.radius = radius
        self.light_num = light_num

        
        self.light = PointLight(
            position = self.pos,
            power = self.power,
            radius = self.radius
        )

        self.light.set_color(tuple(color))

        lights_engine.lights.append(self.light)

    def update(self):
        self.light = PointLight(
            position = self.pos,
            power = self.power,
            radius = self.radius + sin(pygame.time.get_ticks()) * 20
        )