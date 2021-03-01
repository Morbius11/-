import pygame
import sys
import os

pygame.init()
size = width, height = 1900, 1060
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()


class Fon(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('fon.png')
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()


start_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    Fon(start_group)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        start_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
    'winstar': load_image('winstar.png')
}
player_image = load_image('mar2.png', -2)

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall':
            walls_group.add(self)
        if tile_type == 'winstar':
            win_group.add(self)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, event):
        if event.key == pygame.K_RIGHT:
            self.rect.x += 50
        if event.key == pygame.K_LEFT:
            self.rect.x -= 50
        if event.key == pygame.K_UP:
            self.rect.y -= 50
        if event.key == pygame.K_DOWN:
            self.rect.y += 50
        if pygame.sprite.spritecollideany(self, walls_group):
            if event.key == pygame.K_RIGHT:
                self.rect.x -= 50
            if event.key == pygame.K_LEFT:
                self.rect.x += 50
            if event.key == pygame.K_UP:
                self.rect.y += 50
            if event.key == pygame.K_DOWN:
                self.rect.y -= 50
        if self.rect.x in range(finish[0] - 50, finish[0] + 50) and \
                self.rect.y in range(finish[1] - 50, finish[1] + 50):
            terminate()

class Finish(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = self.image.get_rect()

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
win_group = pygame.sprite.Group()


def generate_level(level):
    global finish
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '*':
                Tile('winstar', x, y)
                finish = tile_width * x, tile_height * y
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


start_screen()
player, level_x, level_y = generate_level(load_level('map.txt'))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player_group.update(event)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()

terminate()
