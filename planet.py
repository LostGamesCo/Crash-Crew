from settings import *
from sprites import *
from groups import *
from lighting import *

class Planet(pygame.sprite.Sprite):
    def __init__(self, seed, collision_sprites, all_sprites, lighting_groups, groups):
        # general setup
        super().__init__(groups)
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        
        # groups
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.lighting_sprites = lighting_groups
        
        # planet setup
        self.make_seed(seed)
        print(self.planet_color)
        print(self.seed)

        # load assets
        self.load_assets()

        # chunk setup
        self.current_chunk = [0, 0]
        self.current_chunk_pos = [WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]
        self.chunks = {}
        self.chunk_objects = {}
        self.chunk_x, self.chunk_y = 0, 0
        self.load = False
        for x in range(-1, 2):
            for y in range(-1, 2):
                self.load_chunks(x, y)    
        self.chunks  

    def make_seed(self, seed):

        # 0 = Temperature
        # 1 = Greenery Quantity
        # 2 = Water Quantity
        # 3 = Rock Quantity
        # 4 = Density
        # 5 = Object Size

        self.seed = [randint(1, i) for i in [10, 8, 10, 6, 4, 2]] if seed == 0 else seed
        self.planet_color = ((randint(0, 255), randint(0, 255), randint(0, 255)))
        self.brightness = 0.299 * self.planet_color[0] + 0.587 * self.planet_color[1] + 0.114 * self.planet_color[2]

    def update(self, dt, average_player_pos, obj_index):
        # check for chunk change
        if average_player_pos[0] > self.current_chunk_pos[0] + CHUNK_SIZE / 2:
            self.current_chunk_pos[0] += CHUNK_SIZE
            self.current_chunk[0] += 1
            self.chunk_x, self.chunk_y = -1, -1
            self.load = True
        elif average_player_pos[0] < self.current_chunk_pos[0] - CHUNK_SIZE / 2:
            self.current_chunk_pos[0] -= CHUNK_SIZE
            self.current_chunk[0] -= 1
            self.chunk_x, self.chunk_y = -1, -1
            self.load = True
        if average_player_pos[1] > self.current_chunk_pos[1] + CHUNK_SIZE / 2:
            self.current_chunk_pos[1] += CHUNK_SIZE
            self.current_chunk[1] += 1
            self.chunk_x, self.chunk_y = -1, -1
            self.load = True
        elif average_player_pos[1] < self.current_chunk_pos[1] - CHUNK_SIZE / 2:
            self.current_chunk_pos[1] -= CHUNK_SIZE
            self.current_chunk[1] -= 1
            self.chunk_x, self.chunk_y = -1, -1
            self.load = True
            
        # unload and load chunk
        if self.load:
            self.unload_chunk((self.chunk_x, self.chunk_y))
            self.load_chunks(self.chunk_x, self.chunk_y)
            self.chunk_x += 1
            if self.chunk_x == 2 and self.chunk_y == 1:
                self.load = False
            elif self.chunk_x > 1:
                self.chunk_x = -1
                self.chunk_y += 1
        
        self.unload_chunk(self.current_chunk)

    def load_chunks(self, chunk_x, chunk_y):
        # make new chunks
        if not (self.current_chunk[0] + chunk_x, self.current_chunk[1] + chunk_y) in self.chunks:
            self.create_chunk((self.current_chunk[0] + chunk_x, self.current_chunk[1] + chunk_y))

        # ground tiles
        self.load_ground(chunk_x, chunk_y)
        
        # load objects
        self.load_plants(chunk_x, chunk_y)
             
    def load_ground(self, chunk_x, chunk_y):
        for tile_x in range(0, CHUNK_SIZE // 256):
                    for tile_y in range(0, CHUNK_SIZE // 256):
                        chunk_group = self.chunks[self.current_chunk[0] + chunk_x, self.current_chunk[1] + chunk_y]

                        ChunkSprite(
                            (
                                ((CHUNK_SIZE - WINDOW_WIDTH) / -2) + (tile_x * 256) + ((self.current_chunk[0] + chunk_x) * CHUNK_SIZE),
                                ((CHUNK_SIZE - WINDOW_HEIGHT) / -2) + (tile_y * 256) + ((self.current_chunk[1] + chunk_y) * CHUNK_SIZE)
                            ), 
                            self.grass_tile,
                            True,
                            (chunk_group, self.all_sprites)
                            )
                        
    def load_plants(self, chunk_x, chunk_y):
        for object_pos in self.chunk_objects[self.current_chunk[0] + chunk_x, self.current_chunk[1] + chunk_y]:
                    plant_index = self.chunk_objects[self.current_chunk[0] + chunk_x, self.current_chunk[1] + chunk_y][object_pos]
                    if plant_index[0] == 'plant':
                        plant_surface = plant_index[1]
                        plant_surface = pygame.transform.smoothscale(plant_surface, (plant_surface.get_width() / (5 + plant_index[3] - self.seed[5]), plant_surface.get_height() / (5 + plant_index[3] - self.seed[5])))

                        plant_x = ((CHUNK_SIZE - WINDOW_WIDTH) / -2) + (object_pos[0]) + ((self.current_chunk[0] + chunk_x) * CHUNK_SIZE)
                        plant_y = ((CHUNK_SIZE - WINDOW_HEIGHT) / -2) + (object_pos[1]) + ((self.current_chunk[1] + chunk_y) * CHUNK_SIZE)
                        chunk_group = self.chunks[self.current_chunk[0] + chunk_x, self.current_chunk[1] + chunk_y]

                        ChunkSprite(
                            (plant_x, plant_y), 
                            self.tint_surface(plant_surface, plant_index[2], True, (plant_x, plant_y), chunk_x, chunk_y),
                            False,
                            (chunk_group, self.all_sprites)
                            )
                        
                        ChunkSprite(
                            (plant_x + plant_surface.get_width() / 6, plant_y + plant_surface.get_height() / 1.3), 
                            pygame.Surface((2 * plant_surface.get_width() / 3, plant_surface.get_height() / (8 - self.seed[5]))),
                            False,
                            (chunk_group, self.collision_sprites)
                            )
                        
    def create_chunk(self, chunk):
        self.chunks[chunk] = {pygame.sprite.Group()}
        self.chunk_objects[chunk] = {}
        for plant in range(0, randint(self.seed[1], self.seed[1] + self.seed[4]) * self.seed[4]):
            self.chunk_objects[chunk][randint(0, CHUNK_SIZE), randint(0, CHUNK_SIZE)] = (
                'plant', 
                self.plants[randint(0, 1)][randint(0, 2)], 
                (
                    self.planet_color[1] + 20 * randint(-2, 2), 
                    self.planet_color[2] + 20 * randint(-2, 2), 
                    self.planet_color[0] + 20 * randint(-2, 2)
                ),
                uniform(-1, 1)
                )
        for rock in range(0, randint(self.seed[1], self.seed[1] + self.seed[4])):
            self.chunk_objects[chunk][randint(0, CHUNK_SIZE), randint(0, CHUNK_SIZE)] = 'rock'

    def unload_chunk(self, chunk):
        print(self.chunks[chunk])
        try:
            for sprite in self.chunks[chunk]:
                if hasattr(sprite, 'light'):
                    lights_engine.lights.pop(sprite.light_num)
                sprite.kill()
        except:
            pass

    def tint_surface(self, surface, color, isglow, pos, chunk_x, chunk_y):
        # tint surface
        tinted_surface = surface.copy()
        tint = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        tint_color = [0, 0, 0]
        for i in range(0, 3):
            if color[i] > 255:
                tint_color[i] = 255
            elif color[i] < 0:
                tint_color[i] = 0
            else:
                tint_color[i] = color[i]
        tint.fill(tint_color)
        tinted_surface.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        if isglow and self.brightness < 100:
            chunk_group = self.chunks[self.current_chunk[0] + chunk_x, self.current_chunk[1] + chunk_y]
            Light(
                len(lights_engine.lights),
                (pos[0] + tinted_surface.get_width() / 2, pos[1] + tinted_surface.get_height() / 2), 
                0.5, 
                (tinted_surface.get_width() + max(40, min(180, 200 - self.brightness))), 
                tint_color,
                (chunk_group, self.lighting_sprites)
                )

        return tinted_surface

    def load_assets(self):
        self.grass_image = pygame.image.load(join("Crash Crew", "Graphics", "Planet", "Grass.png")).convert_alpha()
        self.grass_tile = self.tint_surface(self.grass_image, self.planet_color, False, (0, 0), None, None)

        self.plants = {0: [], 1: []}
        for plant_type in self.plants.keys():
                for folder_path, sub_folders, file_names in walk(join('Crash Crew', 'Graphics', 'Planet', 'Plants', str(plant_type))):
                    if file_names:
                        for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0]) if name.endswith('.png') or name.endswith('.PNG') else -1):
                            if file_name.endswith('.png') or file_name.endswith('.PNG'):
                                full_path = join(folder_path, file_name)
                                surface = pygame.image.load(full_path).convert_alpha()
                                self.plants[plant_type].append(surface)