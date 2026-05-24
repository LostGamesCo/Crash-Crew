from settings import *
from groups import *
from player import *
from planet import *
from sprites import *

class Game():
    def __init__(self):

        # general setup
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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

    async def run(self):
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
            self.display_surface.fill(planet.planet_color)
            self.all_sprites.draw(self.average_player_pos)
            self.lighting_sprites.draw(self.average_player_pos)

            pygame.display.update()

            await asyncio.sleep(0)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    planet = Planet(0, game.collision_sprites, game.all_sprites, game.lighting_sprites, game.all_sprites)
    asyncio.run(game.run())