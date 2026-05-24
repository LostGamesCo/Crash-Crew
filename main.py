from settings import *
from groups import *
from player import *
from planet import *
from sprites import *

class Game():
    def __init__(self):

        # general setup
        pygame.display.set_caption('Crash Crew')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.lighting_sprites = LightingSprites()
        self.collision_sprites = pygame.sprite.Group()

        # players
        self.players = []

        for i in range(pygame.joystick.get_count()):
            controller = pygame.joystick.Joystick(i)
            pos = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
            player = Player(pos, i, controller, self.collision_sprites, self.all_sprites)
            self.players.append(player)

    def run(self):
        while self.running:
            # delta time
            dt = self.clock.tick() / 1000

            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # find average player position
            player_positions = [player.rect.center for player in self.players]
            self.average_x_pos, self.average_y_pos = 0, 0
            for x, y in player_positions:
                self.average_x_pos += x
                self.average_y_pos += y
            self.average_player_pos = (self.average_x_pos / len(player_positions), self.average_y_pos / len(player_positions))

            # update
            self.all_sprites.update(dt, self.average_player_pos, None)

            # draw
            lights_engine.clear(planet.planet_color)
            lights_engine.set_ambient(255, 255, 255, planet.brightness)
            self.all_sprites.draw(self.average_player_pos, pygame.display.get_surface())
            self.lighting_sprites.draw(self.average_player_pos)

            lights_engine.render()

            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    planet = Planet(0, game.collision_sprites, game.all_sprites, game.lighting_sprites, game.all_sprites)
    game.run()