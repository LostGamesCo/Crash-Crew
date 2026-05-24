from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, animal_num, controller, collision_sprites, groups):
        # general setup
        super().__init__(groups)
        self.animal_num = animal_num
        self.savepoint = True

        # animals
        self.animal = animals[self.animal_num]
        animals[self.animal_num] = ''
        self.load_assets(pos)

        # movement
        self.speed = 200
        self.direction = pygame.Vector2(0, 0)
        self.collision_sprites = collision_sprites
        self.controller = controller
        self.facing_direction = 1

        self.previous_buttons = [[self.controller.get_button(button)]for button in range(self.controller.get_numbuttons())]

    def load_assets(self, pos):
        self.frames = {'Down': [], 'Up': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('Crash Crew', 'Graphics', 'Players', self.animal, state)):
                if file_names:
                    for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0]) if name.endswith('.png') else -1):
                        if file_name.endswith('.png'):
                            full_path = join(folder_path, file_name)
                            surface = pygame.image.load(full_path).convert_alpha()
                            self.frames[state].append(surface)

        self.state, self.frame_index = 'Down', 0
        self.image = pygame.image.load(join('Crash Crew', 'Graphics', 'Players', str(self.animal), 'Down', '0.png')).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_width() // 4, self.image.get_height() // 4))
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect
        self.hitbox_rect = self.rect.inflate(-20, -40)
        
    def update(self, dt, average_player_pos, obj_index):
        self.input()
        self.move(dt)
        self.animate(dt)

    def animate(self, dt):
        # get state
        if self.direction.y < 0: self.state = 'Up'
        else: self.state = 'Down'

        # animate
        self.frame_index += 5 * dt
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_width() / 4, self.image.get_height() / 4))
        
        # sway
        self.rotation_increase = 1
        self.rotation_increase = 3 if self.direction.x else self.rotation_increase
        self.rotation_increase = 3 if self.direction.y else self.rotation_increase
        self.image = pygame.transform.rotozoom(self.image, sin(pygame.time.get_ticks() / 1000 * 2 * self.rotation_increase) * 2 * self.rotation_increase, 1)

        # facing direction
        if self.facing_direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)
        
    def input(self):
        # movement inputs
        self.direction.x = self.controller.get_axis(0) if abs(self.controller.get_axis(0)) > 0.2 else 0
        self.direction.y = self.controller.get_axis(1) if abs(self.controller.get_axis(1)) > 0.2 else 0
        self.direction = self.direction.normalize() if self.direction else self.direction

        self.current_buttons = [[self.controller.get_button(button)]for button in range(self.controller.get_numbuttons())]

        # switch character
        if self.savepoint:
            if self.current_buttons[9][0] == 1 and (self.previous_buttons[9][0] == 0):
                animals[self.animal_num] = self.animal
                self.animal_num -= 1
                if self.animal_num < 0:
                        self.animal_num += len(animals)
                while animals[self.animal_num] == '':
                    self.animal_num -= 1
                    if self.animal_num < 0:
                        self.animal_num += len(animals)
                self.animal = animals[self.animal_num]
                animals[self.animal_num] = ''   
                self.load_assets(self.rect.center)

            if self.current_buttons[10][0] == 1 and (self.previous_buttons[10][0] == 0):
                animals[self.animal_num] = self.animal
                self.animal_num += 1
                if self.animal_num >= len(animals):
                        self.animal_num = 0
                while animals[self.animal_num] == '':
                    self.animal_num += 1
                    if self.animal_num >= len(animals):
                        self.animal_num = 0
                self.animal = animals[self.animal_num]
                animals[self.animal_num] = ''   
                self.load_assets(self.rect.center)

        self.previous_buttons = self.current_buttons

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.facing_direction = 1 if self.direction.x > 0 else self.facing_direction
        self.facing_direction = -1 if self.direction.x < 0 else self.facing_direction

        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.centerx = self.hitbox_rect.centerx
        self.rect.centery = self.hitbox_rect.centery - 30

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom