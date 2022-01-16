import os
import sys

import pygame
from procgen import generate_dungeon
from random import randint

def load_image(name, colorkey=None):
    fullname = os.path.join('Assets/frames/', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('wall_corner_front_left.png'),
    'empty': {1: load_image('floor_1.png'), 2: load_image('floor_2.png'), 3: load_image('floor_3.png'),
              4: load_image('floor_4.png'), 5: load_image('floor_5.png'), 6: load_image('floor_6.png'),
              7: load_image('floor_7.png'), 8: load_image('floor_8.png')}
}

tile_width = tile_height = 16
# основной персонаж
player = None
player_image = load_image('big_demon_idle_anim_f0.png')
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ':' or level[y][x] == '=':
                Tile(tile_images['empty'][randint(1, 8)], x, y)
            elif level[y][x] == '#' or level[y][x] == '.':
                Tile(tile_images['wall'], x, y)
            elif level[y][x] == '@':
                Tile(tile_images['empty'][randint(1, 8)], x, y)
                new_player = Player(x, y)
            elif level[y][x] == ' ':
                continue
        print(level[y])
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.healt_init()

    def healt_init(self):
        self.current_health = 500
        self.target_health = 1000
        self.max_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 5

    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def get_health(self, amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health

    def update(self):
        self.health()

    def health(self):
        transition_width = 0
        transition_color = (255, 0, 0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (0, 255, 0)

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255, 255, 0)

        health_bar_width = int(self.current_health / self.health_ratio)
        health_bar = pygame.Rect(5, 10, health_bar_width, 15)
        transition_bar = pygame.Rect(health_bar.right, 10, transition_width, 15)

        pygame.draw.rect(screen, (255, 0, 0), health_bar)
        pygame.draw.rect(screen, transition_color, transition_bar)
        pygame.draw.rect(screen, (255, 255, 255), (5, 10, self.health_bar_length, 15), 4)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Deep Dark Dungeon (DDD)')
    generate_dungeon('map.txt', 70, 40, 110, 50, 60)
    player, level_x, level_y = generate_level(load_level('example_map.txt'))
    size = width, height = level_x * tile_width, level_y * tile_height
    screen = pygame.display.set_mode(size)
    running = True
    fps = 60
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == ord('a'):
                    pass
                if event.key == pygame.K_UP:
                    player.get_health(200)
                if event.key == pygame.K_DOWN:
                    player.get_damage(200)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
    pygame.quit()
